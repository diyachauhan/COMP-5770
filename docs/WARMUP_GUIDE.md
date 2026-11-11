# Guided model warm-up

The model experiments produce data for your main annotation and evaluation study. Keep one solving model fixed and preserve the exact prompts. First run direct answering, calculate each selected answer independently using `docs/CALCULATOR_REFERENCE.md`, then compare the direct response with your calculation. Record your own judgment before checking the current metric. Use these comparisons to question the original ±5%/rounding choices. Edit the notebook tolerance cell, re-score the same development outputs and justify the changes, then establish/refine the human rubric through agreement discussions. The absent worked process stays unobservable. Then follow the notebook TODOs for CoT and one-shot CoT; the helpers handle message construction.

## First: zero-shot CoT

Write `COT_INSTRUCTION` to request supported inputs, an equation/scoring rule, units and a concise worked calculation before the answer. `cot_messages` provides the JSON schema and original task, without examples or patient gold. Print the prompt, smoke test one case and run development questions. Check the displayed solution with the human rubric; fluent reasoning and a passing number are not sufficient evidence.

## Next: one-shot CoT

1. Find the demonstrations in **`data/examples.json`**, loaded as `examples`. Access the matching entry using `examples[str(task['calculator_id'])]`. Look up the separate worked example by the requested calculator ID. Inspect its note and explanation; check it against the formula card and record questionable assumptions.
2. Build messages with that example as a user/assistant exchange, followed by the new note and question. `one_shot_messages` does this and refuses an exact note overlap.
3. Write your instruction: for instance, ask the model to extract the new patient's facts independently, apply the same calculator, and return the required worked JSON. Do not copy the example patient's values.
4. Print the messages for a smoke case, then generate and inspect the result. Run the development batch and score with the unchanged final-answer metric.

The example bank has one example per calculator. This is a controlled one-shot method, not nearest-neighbor retrieval.

## Optional extension: formula-grounded prompting

1. Inspect the correct general formula card and its boundaries/units.
2. `grounded_messages` inserts the card into the new task prompt. It contains no patient-specific answer.
3. Write an instruction that directs extraction, units, rule thresholds and calculation under the card's conventions. Keep the output format consistent with zero-shot CoT.
4. Print a smoke-case prompt. Compare the development outputs with worked and one-shot outputs on the same questions. A card cannot compensate automatically for a wrong extracted input.

The calculator is already identified, so card lookup is deterministic. Do not describe this as testing calculator retrieval or full RAG.

## Optional critique and revision

Start with a worked draft; write a critique prompt that checks note evidence, formula, units and arithmetic. Then write a revision prompt using the draft and critique. `refine_once` makes those two extra calls without patient gold. The experiment runner saves all calls, including the initial draft. Inspect both repairs and newly introduced errors. This is one round of a Self-Refine-style adaptation, not proof that repeated refinement is better.

## Prompt changes and experiment records

The notebook passes your full instruction strings into the experiment cache tag so edited prompts generate new experiments. Keep decoding and model fixed for the main comparison. Log additional calls and context tokens; longer prompts and examples supply more information. If a prompt contains evaluation-patient annotations or the evaluated answer, the comparison is invalid.

## Human reasoning review before LLM judging

Use the same note/card checks and human definitions established during direct review, adding process criteria where previously unobservable. Independently review matched CoT/one-shot outputs, measure agreement, and adjudicate with evidence. Keep question-level development/validation partitions fixed. The starter adds 16 reasoning responses (eight questions, two methods); adjust and report workload and coverage. A changed answer rubric needs documented reannotation.

Human review scales poorly across many outputs. After this manual comparison, build an LLM judge step by step from the group's rubric and validate it against those human labels. Do not treat its justifications as verified labels.

Do not train a new solver for this warm-up. More advanced retrieval, Self-Refine loops, MedPrompt or a separate new solving pipeline are optional extensions in `docs/METHODS.md`.
