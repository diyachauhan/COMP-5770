"""Provided prompt building blocks. Gold fields are never part of task inputs."""
import json

TASK_KEYS = ('id', 'calculator_id', 'calculator', 'kind', 'note', 'question')
DIRECT_FORMAT = 'Return ONLY a JSON object with keys answer (a numeric string without units) and unit (a string). Give the final answer only.'
TRACE_FORMAT = ('Return ONLY JSON with keys formula (string), inputs (object with values and units), '
                'calculation (a concise worked calculation or point breakdown), answer (numeric string), unit (string). '
                'Give a concise, checkable solution, including relevant conversions and thresholds.')

def task_input(row):
    return {k: row[k] for k in TASK_KEYS}

def messages(task, reasoning=False, example=None, reference=None):
    result=[{'role':'system','content':'Solve this medical calculation research exercise. '+(TRACE_FORMAT if reasoning else DIRECT_FORMAT)}]
    if example is not None:
        result.extend([
            {'role':'user','content': 'Patient note:\n'+example['note']+'\nQuestion:\n'+example['question']},
            {'role':'assistant','content':json.dumps({'formula':'See worked calculation below',
                'inputs':example['gold_entities'], 'calculation':example['gold_explanation'],
                'answer':str(example['gold_answer']), 'unit':example.get('gold_unit','as requested')})}])
    content='Patient note:\n'+task['note']+'\nQuestion:\n'+task['question']
    if reference is not None:
        content+='\nCalculator reference (not a patient-specific answer):\n'+str(reference)
    result.append({'role':'user','content':content})
    return result

def direct_solver(task, model):
    return model.generate(messages(task))

def diagnostic_solver(task, model):
    """Provided diagnostic run for inspecting an observable calculation trace."""
    return model.generate(messages(task, reasoning=True))
