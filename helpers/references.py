"""Calculator facts for review or explicit formula-grounded experiments; never patient gold."""
import json
from pathlib import Path

def load_reference_library(path='data/calculator_references.json'):
    return json.loads(Path(path).read_text())

def calculator_reference(calculator_id, library=None):
    bank=load_reference_library() if library is None else library
    return bank[str(calculator_id)]

def render_reference(card):
    text=f"### {card['calculator']}\n\n`{card['formula']}`\n\n"
    if card['inputs']:
        text+='| Variable | Meaning | Input unit |\n|---|---|---|\n'
        text+=''.join(f'| {v} | {meaning} | {unit} |\n' for v,meaning,unit in card['inputs'])+'\n'
    if card['criteria']:
        text+='| Category | Condition / points |\n|---|---|\n'
        text+=''.join(f'| {name} | {rule} |\n' for name,rule in card['criteria'])+'\n'
    text+='\n\n'.join(card['notes'])+'\n\n'
    text+='References: '+'; '.join(f'[Source {i+1}]({url})' for i,url in enumerate(card['sources']))
    return text
