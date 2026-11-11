"""Provided final-answer baseline. Intentionally permissive policy, strict numeric parsing."""
import json
import math
import re
import pandas as pd

POLICY = 'baseline_v1: round rule scores with Python round; numerical supplied bounds; ignore units'
NUMBER = re.compile(r'^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$')

def parse_response(raw):
    """Accept a JSON object, optionally fenced, never evaluate generated expressions."""
    if isinstance(raw, dict):
        return raw
    s = str(raw).strip()
    # Some models emit a separate thinking channel. Retain raw output in run logs.
    if '</think>' in s:
        s = s.rsplit('</think>', 1)[1].strip()
    if s.startswith('```') and s.endswith('```'):
        s = re.sub(r'^```(?:json)?\s*', '', s)[:-3].strip()
    try:
        obj = json.loads(s)
        return obj if isinstance(obj, dict) else {}
    except (ValueError, TypeError):
        return {}

def numeric_answer(raw):
    obj = parse_response(raw)
    value = obj.get('answer')
    if isinstance(value, bool) or value is None:
        return None
    text = str(value).strip()
    if not NUMBER.fullmatch(text):
        return None
    number = float(text)
    return number if math.isfinite(number) else None

def baseline_score(raw, gold):
    value = numeric_answer(raw)
    if value is None:
        return {'answer_correct': False, 'parse_ok': False, 'parsed_answer': None, 'policy': POLICY}
    if gold['kind'] == 'rule':
        correct = round(value) == gold['gold_answer']  # banker rounding; e.g. round(2.5)==2
    else:
        correct = gold['lower'] <= value <= gold['upper']
    return {'answer_correct': bool(correct), 'parse_ok': True, 'parsed_answer': value, 'policy': POLICY}

def score_run(outputs, gold_rows):
    by_id = {r['id']: r for r in gold_rows}
    if len(by_id) != len(gold_rows):
        raise ValueError('Duplicate gold IDs')
    if len({r['id'] for r in outputs}) != len(outputs):
        raise ValueError('Duplicate output IDs')
    if set(by_id) != {r['id'] for r in outputs}:
        raise ValueError('Outputs must exactly match this evaluation partition; missing rows cannot be dropped')
    return pd.DataFrame([{
        'id': r['id'], 'method': r['method'], 'calculator_id': by_id[r['id']]['calculator_id'],
        'calculator': by_id[r['id']]['calculator'], 'kind': by_id[r['id']]['kind'],
        'error': r.get('error'), **baseline_score(r['raw'], by_id[r['id']])
    } for r in outputs])

def summary(scores):
    # All rows remain in denominator, including formatting errors and timeouts.
    return scores.groupby(['method', 'kind']).agg(n=('id', 'size'), accuracy=('answer_correct', 'mean'), parse_rate=('parse_ok','mean')).reset_index()
