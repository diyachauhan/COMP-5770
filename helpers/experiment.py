"""Resumable experiments with raw outputs and configuration fingerprints."""
import hashlib
import inspect
import json
import time
from pathlib import Path
from tqdm.auto import tqdm
from .prompts import task_input

def load_questions(path='data/questions.jsonl',split=None):
    rows=[json.loads(s) for s in Path(path).read_text().splitlines() if s.strip()]
    return [r for r in rows if split is None or r['split']==split]

def run_experiment(rows,model,solver,method,output_dir='outputs',retry_errors=False,tag='v1'):
    # Code and data hashes prevent stale caches when prompts, solver, or inputs change.
    inference_files=[Path('helpers')/name for name in ['models.py','prompts.py','experiment.py','references.py','guided_methods.py']]
    module=inspect.getmodule(solver)
    module_path=Path(module.__file__) if module is not None and getattr(module,'__file__',None) else None
    if module_path is not None and module_path.is_file():inference_files.append(module_path)
    code=''.join(p.read_text() for p in inference_files)
    try:code+=inspect.getsource(solver)
    except (OSError,TypeError):code+=str(solver.__code__.co_code) if hasattr(solver,'__code__') else repr(solver)
    payload={'model':model.config,'method':method,'tag':tag,'code':hashlib.sha256(code.encode()).hexdigest(),
             'assets':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path('data').glob('*')) if p.is_file() and p.name not in {'questions.jsonl','questions.csv','calculator_summary.csv'}},
             'tasks':[task_input(r) for r in rows]}
    fingerprint=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()[:16]
    root=Path(output_dir);root.mkdir(parents=True,exist_ok=True)
    path=root/f'{method}_{fingerprint}.jsonl'
    (root/f'{method}_{fingerprint}_config.json').write_text(json.dumps(payload,indent=2))
    cache={r['id']:r for r in [json.loads(s) for s in path.read_text().splitlines()]} if path.exists() else {}
    for row in tqdm(rows,desc=method):
        old=cache.get(row['id'])
        if old is not None and not (retry_errors and old.get('error')):continue
        started=time.perf_counter();model.last_usage={};model.call_log=[]
        try:
            if hasattr(model,'reset_task_seed'):model.reset_task_seed(row['id'],method)
            response=solver(task_input(row),model)
            if not isinstance(response,(str,dict)):raise TypeError('A solver must return a raw string or a JSON-compatible dict')
            error=None
        except NotImplementedError:
            raise  # A TODO is not an experimental failure: stop and implement it.
        except Exception as exc:
            response='';error=f'{type(exc).__name__}: {exc}'
        rec={'id':row['id'],'method':method,'model':model.config,'raw':response,'error':error,
             'seconds':time.perf_counter()-started,'calls':model.call_log.copy(),
             'usage_last_call':model.last_usage,'fingerprint':fingerprint}
        cache[row['id']]=rec
        with path.open('a') as f:f.write(json.dumps(rec,ensure_ascii=False)+'\n')
    # Return one latest record per ID; a retry appends rather than destroying prior evidence.
    print(f'Saved {len(rows)} rows: {path}')
    return [cache[r['id']] for r in rows]
