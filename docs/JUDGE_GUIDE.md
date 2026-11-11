# LLM judging: human alignment and error attribution

After direct human review, agreement, CoT/one-shot experiments and human reasoning review, your group has two related tasks: design a judge that better agrees with independently reviewed human labels, and analyze the intermediate errors in outputs from different solving methods. Both depend on a defensible rubric and evidence, not just a judge's fluent explanation.

## Build your judge from the human rubric, step by step

Human validation takes time; an LLM judge is a candidate way to apply the rubric to more responses. Translate the human definitions into `JUDGE_CRITERIA`, explain thresholds and overall decisions in `JUDGE_DECISION_RULES`, and require supported quotations and reference checks in `JUDGE_EVIDENCE_RULES`. Assemble them as version 1, print a prompt for one development reasoning response, inspect its verdict alongside human adjudication, then run the development batch. Revise definitions only using development evidence. These are design prompts, not a completed correctness policy.

## Improve and validate two judge versions

Write the first rubric in the notebook. `judge_messages` gives the note, candidate output, calculator card and evaluation annotations to a model. The schema separates final answer, inputs, formula/rule, units, arithmetic, process and overall assessment, with reasons, evidence and error categories. `run_judges` retains raw prompts, model settings and usage, caches identical requests, and keeps call/parse failures visible. Structural parsing does not verify the content of a judgment.

Use only the question-disjoint development responses (default: 16 direct plus eight reasoning responses) for inspecting judge failures and designing an improvement. Choose an intervention for a reason: clearer rules for equivalent formulas, explicit missing-process handling, independent arithmetic checks, or adjudicated calibration demonstrations. Save version 1 before changing anything. Then freeze version 2 and compare both on the same reserved responses (default: eight direct plus eight reasoning responses, from eight questions; the reasoning subset covers four questions). Split by question: do not use another method's response to a reserved question as a demonstration. For a richer study, expand the independently annotated validation set before drawing broader conclusions.

`compare_with_humans` reports per-dimension percent agreement, kappa, binary coverage and error detection precision/recall, plus false-positive and false-negative counts. Fail is the positive class: false positives reject a human-passing response; false negatives miss a human-labeled error. Unobservable and judge-error statuses remain in total coverage and label distributions, but do not become binary passes/fails. Explain the label policy and inspect excluded pairs. Use all selected responses, not only judgments the model parsed successfully.

Review exact evidence quotes and reference checks. Ask whether the judge actually checks the equation or simply anchors on the gold number. Deliberately test correct-number/wrong-input cases, equivalent valid formulas, boundary rules, missing facts and absent worked solutions. Keep artificial probes separate from natural model outputs. Reference annotations may be disputed; adjudication should record those concerns.

## Small Qwen and optional GPT comparison

A Qwen judge can use the existing solving-model instance, keeping GPU requirements modest. Disclose correlated errors when the same model solves and judges. Optional GPT access uses `EndpointModel` and a key from the Colab secret/environment mechanism in `docs/MODEL_GUIDE.md`; do not require classmates to buy access. Compare the two judges on identical responses, rubric, references and requested output budget. Record model/version, temperature, context, call count, runtime and usage; wall time is hardware/provider dependent. GPT labels are not human truth. If only one judge is available, make the comparison a clearly labeled proposal in the individual reflection.

## Intermediate-error analysis across solving methods

Evaluate every worked output using the settled judge. Use the same question set for all methods. `error_table` exports aspect labels, categories, first error, evidence, baseline pass, solver failure and judge failure. Report dimension-specific pass rates alongside unobservable/error coverage; a lower detected-error rate can mean the judge missed more errors. Do not treat direct-only responses as valid or invalid visible calculations.

For a wrong extracted value followed by mathematically correct substitution, distinguish the extraction fault from its downstream numerical consequence. Do not automatically count each downstream step as an independent arithmetic failure. Let categories overlap when distinct mistakes are evidenced. Inspect matched cases manually and state which method comparisons have independent human validation. The initial direct plus supplementary reasoning human sets validate judging only on their sampled distributions; it does not validate the judge on every later method automatically.

## Individual reflection and possible judge-training data

Use group findings to discuss which dimensions can be automated credibly and where human review remains needed. Identify evidence and limits, not a universal claim. If proposing judge fine-tuning, describe: independently generated candidate solutions; human or executable checks for labels; authentic and deliberately perturbed mistakes; valid paraphrases/equivalent formulas; error diversity and balance; evidence annotations; and splits by patient/question/template to prevent answer or perturbation-pattern leakage. Test on authentic held-out outputs and, if feasible, held-out calculators. Training on another LLM's unchecked labels can amplify its mistakes. Actual training is optional; a rigorous data and validation proposal is appropriate for this course.

An evaluation judge receives patient gold and must remain separate from solver feedback. An improved solving verifier needs a gold-free prompt.

Optional primary references: Zheng et al., [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685); Liu et al., [G-Eval](https://arxiv.org/abs/2303.16634); Lightman et al., [Let's Verify Step by Step](https://arxiv.org/abs/2305.20050). These motivate questions; none establishes correctness for this dataset or requires a named judge implementation.

Always separate direct-only and reasoning judge results. Many direct outputs should have unobservable process labels; correctly recognizing their absence does not demonstrate the ability to catch faulty reasoning. Report response and unique-question counts, and keep all variants of a reserved question out of judge demonstrations/tuning.

Use the settled answer-tolerance policy from human evaluation in the judge rubric. Use pass/fail for observable aspects and unobservable for calculation steps the response does not show.
