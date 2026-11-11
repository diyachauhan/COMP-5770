"""Shared, blinded review forms and explicit pairwise agreement (no automatic consensus)."""
import json
import random
from collections import Counter
from itertools import combinations
from pathlib import Path
import pandas as pd
from .evaluation import baseline_score
from .references import calculator_reference, render_reference

ASPECTS = ['answer', 'inputs', 'rule_or_formula', 'units', 'arithmetic', 'process', 'overall']
LABELS = {'pass', 'fail', 'unobservable'}
ERROR_TYPES = ['wrong_formula', 'wrong_input_or_timepoint', 'missing_input', 'rule_interpretation',
               'unit_conversion', 'arithmetic', 'precision', 'format_or_parse', 'other']

def select_review(outputs, questions, n=24, seed=2026):
    """One output per question; balanced rule/numerical sample, independent of correctness."""
    gold = {r['id']: r for r in questions}
    if len({r['id'] for r in outputs}) != len(outputs):
        raise ValueError('Select one method at a time: question IDs must be unique.')
    if n < 4 or n % 2 or n > len(outputs):
        raise ValueError('Choose an even n >= 4, at most the output count.')
    rng = random.Random(seed)
    selected = []
    for kind in ['rule', 'numerical']:
        pool = [r for r in outputs if gold[r['id']]['kind'] == kind]
        rng.shuffle(pool)
        if len(pool) < n // 2:
            raise ValueError(f'Not enough {kind} outputs for balanced selection.')
        selected.extend(pool[:n // 2])
    rng.shuffle(selected)
    return selected

def make_review_files(outputs, questions, root, annotators=('A', 'B'), holdout_n=8, partitions=None, prefix='review'):
    """Export identical response sets with no baseline vote or solver/model name in forms.

    Human labels start empty; input review selection should be fixed before inspecting scores.
    Existing review files are protected from accidental overwriting.
    """
    root = Path(root); root.mkdir(parents=True, exist_ok=True)
    annotators = list(annotators)
    if len(annotators) < 2 or len(set(annotators)) != len(annotators):
        raise ValueError('Use at least two distinct annotator IDs for agreement.')
    if partitions is None and not 0 < holdout_n < len(outputs):
        raise ValueError('Reserve some responses for judge validation and some for calibration.')
    targets = [root / f'annotations_{a}.csv' for a in annotators] + [root/'review_key.json', root/'adjudication.csv']
    if any(f.exists() for f in targets):
        raise FileExistsError('Review files exist. Reuse them or choose a new versioned directory.')
    gold = {r['id']: r for r in questions}
    if len({(r['method'],r['id']) for r in outputs}) != len(outputs):
        raise ValueError('Duplicate method/question responses in review.')
    question_ids=list(dict.fromkeys(r['id'] for r in outputs))
    if partitions is None:
        if not 0 < holdout_n < len(question_ids):raise ValueError('Split by unique questions, with both partitions nonempty.')
        partitions={q:('judge_validation' if i<holdout_n else 'judge_calibration') for i,q in enumerate(question_ids)}
    if any(partitions.get(q) not in {'judge_validation','judge_calibration'} for q in question_ids):
        raise ValueError('Every question needs a calibration/validation partition.')
    key, forms, adjudication = [], [], []
    for i, out in enumerate(outputs):
        g = gold[out['id']]; rid = f'{prefix}_{i+1:03d}'
        partition = partitions[g['id']]
        key.append(dict(response_id=rid, question_id=g['id'], method=out['method'],
                        partition=partition, output=out,
                        baseline_answer='pass' if baseline_score(out['raw'], g)['answer_correct'] else 'fail'))
        row = dict(response_id=rid, calculator=g['calculator'], note=g['note'], question=g['question'],
                   candidate_raw=out['raw'], calculator_reference=render_reference(calculator_reference(g['calculator_id'])),
                   reference_answer=g['gold_answer'], reference_unit=g['gold_unit'],
                   reference_entities=json.dumps(g['gold_entities']), reference_explanation=g['gold_explanation'],
                   **{a:'' for a in ASPECTS}, error_types='', first_error='', evidence='', notes='')
        forms.append(row)
        adjudication.append(dict(response_id=rid, **{a:'' for a in ASPECTS}, error_types='', first_error='',
                                 evidence='', resolution_notes='', rubric_version=''))
    for a in annotators:
        table = pd.DataFrame(forms); table.insert(1, 'annotator', a)
        table.to_csv(root/f'annotations_{a}.csv', index=False)
    pd.DataFrame(adjudication).to_csv(root/'adjudication.csv', index=False)
    (root/'review_key.json').write_text(json.dumps(key, indent=2))
    return pd.DataFrame([{k:v for k,v in r.items() if k!='output'} for r in key])

def read_annotations(paths):
    frames = [pd.read_csv(p, keep_default_na=False, dtype=str) for p in paths]
    if not frames:
        raise ValueError('Supply completed annotation files.')
    table = pd.concat(frames, ignore_index=True)
    if table.duplicated(['response_id', 'annotator']).any():
        raise ValueError('Duplicate annotator/response labels.')
    for a in ASPECTS:
        if not table[a].isin(LABELS).all():
            raise ValueError(f'Complete {a} labels using {sorted(LABELS)}.')
    return table

def label_comparison(left, right):
    """Nominal raw agreement/kappa on all supplied labels; binary error metrics separately."""
    if len(left) != len(right) or not left:
        raise ValueError('Need nonempty paired labels of equal length.')
    allowed = LABELS | {'error'}
    if any(x not in allowed for x in list(left)+list(right)):
        raise ValueError('Unrecognized or incomplete label.')
    n = len(left); lc, rc = Counter(left), Counter(right)
    observed = sum(a==b for a,b in zip(left,right))/n
    expected = sum(lc[k]*rc[k] for k in allowed)/n**2
    kappa = (observed-expected)/(1-expected) if expected < 1 else None
    cells = Counter((a,b) for a,b in zip(left,right) if a in {'pass','fail'} and b in {'pass','fail'})
    tp, tn = cells['fail','fail'], cells['pass','pass']
    fp, fn = cells['pass','fail'], cells['fail','pass']
    ratio = lambda a,b: a/b if b else None
    return dict(n=n, agreement=observed, kappa=kappa, n_binary=tp+tn+fp+fn,
                binary_coverage=(tp+tn+fp+fn)/n, error_precision=ratio(tp,tp+fp),
                error_recall=ratio(tp,tp+fn), tp=tp,tn=tn,fp=fp,fn=fn,
                reference_labels=dict(lc), candidate_labels=dict(rc))

def pairwise_agreement(table, aspects=ASPECTS):
    reports=[]
    for a,b in combinations(sorted(table.annotator.unique()),2):
        l=table[table.annotator==a].set_index('response_id')
        r=table[table.annotator==b].set_index('response_id')
        shared=sorted(set(l.index)&set(r.index))
        if not shared:continue
        for aspect in aspects:
            reports.append(dict(reviewer_a=a,reviewer_b=b,aspect=aspect,
                                n_a=len(l),n_b=len(r),**label_comparison(l.loc[shared,aspect].tolist(),r.loc[shared,aspect].tolist())))
    return pd.DataFrame(reports)

def load_adjudication(path, expected_ids):
    table=pd.read_csv(path,keep_default_na=False,dtype=str)
    if table.response_id.duplicated().any() or set(table.response_id)!=set(expected_ids):
        raise ValueError('Adjudication must cover every selected response exactly once.')
    for a in ASPECTS:
        if not table[a].isin(LABELS).all():raise ValueError(f'Complete adjudicated {a} labels.')
    if (table.resolution_notes.str.strip()=='').any() or (table.rubric_version.str.strip()=='').any():
        raise ValueError('Record resolution notes and rubric version, including unanimous decisions.')
    return table

def compare_baseline(key, human):
    """Compare like-for-like final answers; process is separately meaningful."""
    base=pd.DataFrame([{k:r[k] for k in ['response_id','baseline_answer']} for r in key])
    joined=base.merge(human,on='response_id',validate='one_to_one')
    if len(joined)!=len(base):raise ValueError('Missing adjudicated responses.')
    report=label_comparison(joined.answer.tolist(),joined.baseline_answer.tolist())
    joined['answer_disagreement']=joined.answer!=joined.baseline_answer
    joined['baseline_pass_process_fail']=(joined.baseline_answer=='pass')&(joined.process=='fail')
    return report,joined
