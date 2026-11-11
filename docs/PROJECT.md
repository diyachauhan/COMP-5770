# Medical Calculations

## Project overview

Medical calculations offer a useful setting for studying language-model reliability: a numerical answer can be checked, but an acceptable final number does not necessarily establish that the model used the right information or calculation.

In this project, you will investigate how a language model solves medical calculation questions, how its performance should be evaluated, and whether the errors you identify can guide a better solving pipeline.

## Starting materials

The package contains 160 questions: eight rule-based and eight numerical calculators, ten questions each. There are 32 development and 128 test questions, plus 16 separate prompting examples. The calculator reference provides every formula, scoring table, input unit and convention. Patient-specific annotations are reference material for review, and may contain assumptions requiring scrutiny.

The notebook gives model-loading code, the original final-answer metric, annotation exports, agreement calculations, prompt-building helpers, and a judge runner. **Student TODOs are in the notebook.** Supporting helper files are complete. `docs/WARMUP_GUIDE.md`, `docs/ANNOTATION_GUIDE.md`, `docs/JUDGE_GUIDE.md` and `docs/MODEL_GUIDE.md` support the work.

## Guided warm-up: understand the original evaluation

Start by running direct answering and reading the exact evaluation policy. Numerical predictions pass if they fall within the supplied inclusive lower/upper limits, generally **±5%** of the reference answer. Rule-based predictions pass if Python `round(prediction)` equals the reference score; this uses ties-to-even, not always rounding upward. The parser requires a numeric JSON answer. Units, extracted inputs, formulas and intermediate calculations are not judged; parsing/inference failures count as incorrect. Use the printed policy and boundary examples to understand what the reported score means.

Each group member independently reviews a shared set of direct outputs. The suggested starter is **24 responses per person**, selected without using their correctness, balanced between rule-based and numerical cases. The default reserves 16 questions for development and eight for later judge validation. Groups may adjust the sample size, but use overlapping responses and report actual coverage.

For each selected question, **first calculate the answer yourself** from the note using the formulas, scoring rules and units in **`docs/CALCULATOR_REFERENCE.md`** (also available in `data/calculator_references.json`). Record your inputs, calculation, answer, unit and assumptions in the provided independent-calculation worksheet before consulting the model output, patient-specific reference answer or evaluator's label.

Then compare the model's direct answer with your own result and record your independent correctness judgment. Once recorded, check whether the current final-answer evaluation agrees. Explain disagreements involving tolerance, rounding, units, parsing or reference assumptions. Use the development cases for this discussion and keep reserved cases out of rubric/judge tuning. Compare your independent judgments with other reviewers, discuss differences and develop/refine the human evaluation rubric with evidence. Preserve the original calculations and labels.

You can verify the model's final answer through your own calculation, but do not infer its hidden process: a direct-only response leaves formula, extraction and arithmetic unobservable. Define overall validity relative to the requested direct-answer task. Reference answers are comparison evidence, not infallible ground truth.

Report pairwise percent agreement and Cohen's kappa with sample sizes and label frequencies. Discuss disagreements and document evidence-based adjudication; preserve the independent labels. Compare human and original-metric labels on the **same direct response**. Why might units, rounding or tolerance produce different judgments? Propose an improved policy. Use only development cases for rubric/judge changes and keep reserved questions out of tuning.

## After calculating: is the original tolerance appropriate?

Use your calculations to examine whether the generally ±5% numerical tolerance and rule-score rounding make sense. Explain cases where these choices disagree with human judgment. Could a tighter policy help, and could it wrongly reject a legitimate rounded answer? Consider relative versus absolute tolerance, calculator-specific precision and units.

**Implement a revised final-answer evaluator in the notebook's editable tolerance cell**, justify its policy and compare it with the unchanged original metric on the same saved development outputs. Keep failures in the denominator. Do not select thresholds simply to maximize a score. Record the new policy in your human rubric and later judge prompt; keep reserved cases out of tuning. A stricter final-answer metric is not by itself an evaluation of reasoning correctness.

## After agreement: how could you inspect the model's reasoning?

You now have an evaluation rubric, but a final number cannot establish how the model applied the calculator. Could a method expose a worked calculation that your rubric can inspect? Consult `docs/METHODS.md`, then use the notebook's guided TODOs:

1. **First try zero-shot CoT.** Write an instruction asking for a concise, checkable formula or scoring rule, extracted inputs, units, calculation and final answer. Print the prompt, smoke test it and run the development batch.  
2. **Then try one-shot CoT.** The separate demonstrations are in **`data/examples.json`**, loaded as `examples`; use `examples[str(task['calculator_id'])]`. Inspect a same-calculator example, add it before the new question, and write an instruction that extracts the new patient's facts rather than copying example values.  
3. **Apply your human rubric to the displayed reasoning.** Compare CoT and one-shot CoT on the same questions. Are the inputs, formula, thresholds, units and arithmetic supported? Can a correct final number conceal an invalid process? Can an equivalent valid formula be rejected unfairly?

Keep one solving model fixed and preserve exact prompts and raw outputs. A displayed worked solution is observable evidence; it is not guaranteed faithful access to the model's hidden reasoning. These are new generation experiments, so never compare the baseline vote for a direct response with the process label for a different CoT response as though they describe the same output.

The starter supplementary review selects four development and four reserved questions from the original question partitions, and reviews both CoT and one-shot CoT: **16 additional responses per person**. Adjust this supplement for workload and report its selection. Review independently and adjudicate again. Extend the group's rubric with explicit process criteria and record its version; if answer criteria change, document reannotation rather than mixing incompatible labels. Keep the original independent annotations.

Formula-grounded prompting, Self-Refine and other entries in `docs/METHODS.md` are **optional extensions after CoT and one-shot CoT**. A separate novel solving pipeline is also optional. The main contribution remains human evaluation data and judge reliability.

## Human review is time-consuming: could an LLM judge apply your rubric?

Your group has now assessed final answers and worked solutions. Repeating this review across every model and prompting method costs time. Explore whether an LLM judge can apply **the same human rubric**, and whether its decisions are sufficiently reliable for your study. Automation is a hypothesis to test, not a substitute for validation.

Build the judge step by step: translate human aspect definitions into criteria; define decision rules for tolerances and missing process; specify the note/card/reference evidence it receives; request structured labels and exact supporting excerpts; then print and test one development judgment against human adjudication. The notebook has separate TODOs for criteria, decision rules and evidence requirements. The helper supplies mechanics, not the correct rubric.

## Group research question 1: how can the LLM judge better match humans?

Implement an LLM judge using your group's rubric and the helper interface. It should return dimension-specific labels and evidence. Start with a clear first version, examine its mistakes on judge-development cases, and design **one meaningful improvement**. You might refine rubric definitions, supply independently adjudicated demonstrations from development cases, separate arithmetic checking from semantic interpretation, or combine deterministic checks with model judgment. Explain why the change addresses an observed judging error.

Combine the direct and reasoning human references, retaining their response types and fixed question partitions. The default benchmark has 24 development responses and 16 validation responses (only eight validation responses contain displayed reasoning, from four questions). Freeze the judge and rubric before evaluating the reserved cases. Compare both judge versions with the same adjudicated human labels. Report agreement, false positives, missed errors and unobservable labels and call/parse failures per dimension, separately for direct-only and reasoning outputs. A large number of unobservable direct processes must not inflate claims about reasoning-error detection. Check the claimed evidence against the response and reference. A judge that labels most cases “pass” can have high agreement while missing important errors. Keep failures in the coverage accounting and report how many cases support each result.

A small Qwen model is sufficient to run the project. A GPT judge is an **optional** comparison if approved access and budget are available; no paid API is required. If you compare them, use the same rubric, references, output budget and response set, log configurations and costs, and explain unavoidable differences. GPT is another candidate judge, not the ground truth. Reusing the solver as judge may produce correlated errors.

## Group research question 2: what goes wrong inside the solutions?

Use the settled judge and your human-review evidence to analyze the worked outputs from the different solving methods. Separate wrong extraction/time-point, missing inputs, formula/scoring rule, unit conversion, arithmetic, precision and formatting errors, adapting the categories if justified. Locate the first supported error and distinguish downstream consequences from independent mistakes. Allow multiple errors when supported by evidence; do not invent a process label for a direct-only response.

Compare patterns by method and calculator category. Look for correct-answer/wrong-process cases, valid solutions rejected by the metric, changes after prompting, and judge disagreements. Inspect cases across methods on the same question. For methods outside your human-validated set, explicitly identify conclusions based only on model judging; review additional matched cases if necessary to substantiate a claim. Freeze solving prompts and judge design on development data before any final test runs. You may evaluate a reproducible test subset if compute is limited; report its sampling and size.

Bring these findings to a **group presentation**: the original evaluation problem, human rubric and agreement, judge design and validation, comparative error analysis, and remaining limitations. Include concrete evidence, not only accuracy bars. Submit the shared notebook/code, original annotations, adjudication notes, judge outputs and a group findings report or presentation document. Specify contributions so the collaboration is reviewable.

## Final report: what still needs human judgment?

- Which parts of the evaluation framework can an LLM judge handle credibly in your experiment, and which still need human involvement? What evidence supports that boundary?  
- How would you decide whether to trust this judge? Where did it fail, and could its mistakes change the conclusions about solving methods?  
- If you tested GPT and a small Qwen judge, where did they differ? If you did not, propose a controlled comparison and distinguish it from an observed result.  
- How could judge reliability improve further? For example, how would you build training data with independently verified labels, correct-answer/wrong-process examples, equivalent valid formulas, boundary cases and unit-conversion errors? How would you prevent data leakage and test generalization?  
- What succeeded, what failed, what remains untested, and what would you investigate next?

These prompts support an argument, not a required number of pages or checklist of technologies. Judge fine-tuning is an optional future direction; a thoughtful data construction and evaluation proposal is sufficient. Do not claim an unperformed experiment as evidence.

## Keep the study defensible

Solvers may receive the question, note, general calculator cards and separate example bank. They must not receive the evaluated patient's gold answer, entities, bounds or gold-dependent feedback. Evaluation judges may use these references. A verifier embedded in a solving pipeline needs a separate prompt without patient gold. Maintain the development/test split, and reserve judge-validation responses by **question**, so variants of the same question do not leak into judge tuning.

Preserve raw outputs, unsuccessful calls, independent labels and all versions of the rubric. Report missing labels, failed calls and disagreement coverage. Human adjudication is a documented reference, not perfect clinical truth. This is an educational study of applying an identified calculator, not a tool for patient care.