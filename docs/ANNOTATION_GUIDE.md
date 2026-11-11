# Independent human review and agreement

Suggested workflow: first independently calculate the answers to the same 24 questions, then label the **same 24 direct outputs**, measure agreement and refine the human rubric. Unshown input extraction, formula and arithmetic remain unobservable. Then implement CoT and one-shot CoT and inspect their displayed reasoning with that rubric. The default supplements review with **16 reasoning outputs** (eight questions, two methods). Both stages are adjustable workload suggestions.

Direct review reserves 16 questions for development and eight for judge validation. Supplementary CoT/one-shot responses inherit those exact question partitions. The default combined judge benchmark contains 24 development responses and 16 validation responses, with only eight validation reasoning responses from four questions. More responses do not mean more independent questions; report both counts and the small sample's limits.

## First calculate, then compare

Open `independent_calculations_<reviewer>.csv` first. It contains only the note, question and general calculator card, plus blank fields for your inputs, calculation, answer, unit and assumptions. It does not contain the model output or patient-specific gold answer. Find all calculator equations and scoring tables in **`docs/CALCULATOR_REFERENCE.md`**; their JSON versions are in `data/calculator_references.json`. Complete your calculation before consulting the candidate, reference answer or baseline vote.

Next open your `annotations_<reviewer>.csv`. Compare the direct answer with your own result and record your independent human judgment. The annotation form includes comparison references, which you should verify rather than copy. Once your judgment is saved, use the notebook's independent-human-versus-metric comparison to ask whether the current evaluator agrees. Explain differences with your calculation and note/card evidence. Discuss development cases while refining the rubric; reserved comparisons are deferred to final validation.

Then compare reviewers' original labels, investigate disagreements and adjudicate with evidence. Preserve original calculations, independent labels and rubric versions. Direct and reasoning review IDs have different prefixes; later reasoning exports inherit the original question partitions. Forms omit model/method names and baseline votes; `review_key.json` stores those mappings separately. Existing worksheet files are not overwritten.

## Starting dimensions:  refine their definitions together

| Column | Question to answer |
| :---- | :---- |
| `answer` | Is the final number and required unit acceptable under your stated policy? |
| `inputs` | Are required facts, time-points and assumptions supported by the note? |
| `rule_or_formula` | Is the applicable version of the equation or scoring rule used correctly? |
| `units` | Are inputs and output units handled correctly? |
| `arithmetic` | Are the displayed substitutions, arithmetic or point totals valid? |
| `process` | Is the observable worked solution substantively valid overall? |
| `overall` | Under your rubric, does the response meet the full task requirements? |

&nbsp;

Use `pass` or `fail` for observable aspects, and `unobservable` only when the response does not show the relevant calculation step. Do not infer correctness from a confident style. A direct-only response has an unobservable process. Define how an upstream error affects arithmetic: valid arithmetic on a wrong extracted value can pass the local arithmetic check while the process fails. Explain this distinction in your rubric. For overall labels, define validity relative to the requested task: a direct-answer task does not automatically fail because it did not request a worked solution. For a worked-solution task define how answer/process failures and missing evidence are combined; do not assume the helper decides this for you.

For every substantive finding, record a candidate quote and the supporting note fact, formula, threshold or independent calculation in `evidence`. `error_types` may contain semicolon-separated categories; `first_error` identifies the first supported error, not merely the first criticism in the explanation. Use `notes` for disputed gold assumptions and rubric questions. Do not force an error label solely to match another reviewer.

Example: MAP for SBP 120/DBP 60 is 80 mmHg. “(120 \+ 60)/2 \= 80” has a correct final answer but the wrong formula and invalid arithmetic. “60 \+ (120−60)/3 \= 80” is valid. These are artificial probes, not dataset observations.

## Calculate and interpret agreement

Load completed CSVs using `read_annotations`; blank/invalid labels are rejected rather than silently discarded. `pairwise_agreement` aligns by response ID, reports each reviewer pair and dimension, paired sample size, raw agreement and nominal Cohen's kappa. Non-overlapping items are not magically paired; inspect `n_a`, `n_b` and `n` for coverage. Report label frequencies, not just a single averaged score.

Percent agreement is the fraction of identical labels. Kappa adjusts for agreement expected from each reviewer's marginal label distribution: `(observed − expected)/(1 − expected)`. It can be undefined when all labels are the same, and sensitive to skewed prevalence. There is no automatic “good enough” cutoff. The helper treats unobservable as an explicit nominal label; you may add binary-only analysis but report its reduced coverage. Binary error metrics use `fail` as positive.

Discuss disagreements using the original independent labels. Revise the rubric on development cases, preserve its earlier version and any reannotation, and record adjudicated labels, resolution notes and rubric version in `adjudication.csv`. Do not fabricate independent agreement from consensus labels. Do not automatically majority-vote; investigate whether even unanimous labels follow an incorrect reference. Reserved validation cases should receive the settled rubric without influencing judge tuning. If the rubric changes after reviewing their judge failures, obtain a new independent validation set before claiming held-out validation.

After each review stage, `compare_baseline` compares final-answer labels on the exact same response, and separately flags baseline-pass/process-fail cases. A human process failure is not a final-answer disagreement; report both phenomena separately.

Reference for Cohen's kappa: [scikit-learn documentation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html). The included helper implements the nominal formula directly and requires no scikit-learn installation.

Combine the stage-specific labels for judging only if rubric definitions are compatible and versions are documented. Preserve initial labels when revising definitions. Report judge agreement separately on direct-only and reasoning responses; a correct unobservable label on a direct answer is not evidence of successful reasoning-error detection.

After your independent calculations, examine the original ±5%/rounding choices and use the notebook's tolerance cell to propose and test a justified revision on development outputs. Preserve both scoring versions. Make the settled human rubric and LLM judge follow the same chosen answer policy.