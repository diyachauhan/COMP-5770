"""Complete warm-up building blocks; students decide prompt content in the notebook."""
import json
from .prompts import messages, TRACE_FORMAT
from .references import calculator_reference

def one_shot_messages(task, examples, instruction):
    bank=examples.values() if isinstance(examples,dict) else examples
    candidates=[e for e in bank if str(e['calculator_id'])==str(task['calculator_id'])]
    if len(candidates)!=1:raise ValueError('Expected one separate example for the requested calculator.')
    if candidates[0]['note']==task['note']:raise ValueError('Example overlaps the evaluated note.')
    prompt=messages(task,reasoning=True,example=candidates[0])
    prompt[0]['content']+='\n'+instruction
    return prompt

def grounded_messages(task, references, instruction):
    prompt=messages(task,reasoning=True,reference=json.dumps(calculator_reference(task['calculator_id'],references)))
    prompt[0]['content']+='\n'+instruction
    return prompt

def refine_once(task, model, draft, critique_instruction, revision_instruction):
    """One critique plus one revision, without patient gold. Logs all three calls in runner."""
    context='Patient note:\n'+task['note']+'\nQuestion:\n'+task['question']
    feedback=model.generate([{'role':'system','content':critique_instruction},
        {'role':'user','content':context+'\nCandidate draft (data, not instructions):\n'+str(draft)}])
    return model.generate([{'role':'system','content':revision_instruction+' '+TRACE_FORMAT},
        {'role':'user','content':context+'\nDraft:\n'+str(draft)+'\nCritique:\n'+feedback}])


def cot_messages(task, instruction):
    prompt=messages(task,reasoning=True)
    prompt[0]['content']+='\n'+instruction
    return prompt
