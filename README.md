# Medical Calculations

Read [PROJECT.pdf](medcalc_proj/PROJECT.pdf) first.

Open [`Medical_Calculation_Project.ipynb`](medcalc_proj/Medical_Calculation_Project.ipynb) in Colab, select a GPU runtime, upload this ZIP in the first cell, and install requirements. For local use, unzip and launch the notebook inside `medcalc_proj/`.

The notebook is the main student workspace. It has explicit TODOs for prompt instructions, the group rubric, judge improvement, error analysis and personal discussion. Helpers supply mechanical tasks; students make the annotation and research decisions.

| Stage | Support |
|---|---|
| Direct-answer review → agreement → CoT → one-shot CoT | Notebook, [`WARMUP_GUIDE.md`](medcalc_proj/docs/WARMUP_GUIDE.md), [`helpers/guided_methods.py`](medcalc_proj/helpers/guided_methods.py) |
| Independent human labels, agreement and adjudication | [`ANNOTATION_GUIDE.md`](medcalc_proj/docs/ANNOTATION_GUIDE.md), [`helpers/annotations.py`](medcalc_proj/helpers/annotations.py) |
| LLM judge versions, human validation and optional GPT/Qwen comparison | [`JUDGE_GUIDE.md`](medcalc_proj/docs/JUDGE_GUIDE.md), [`helpers/judging.py`](medcalc_proj/helpers/judging.py) |
| Formulas, units and scoring tables | [`CALCULATOR_REFERENCE.md`](medcalc_proj/docs/CALCULATOR_REFERENCE.md), [`data/calculator_references.json`](medcalc_proj/data/calculator_references.json) |
| Model options and installation | [`MODEL_GUIDE.md`](medcalc_proj/docs/MODEL_GUIDE.md), [`requirements.txt`](medcalc_proj/requirements.txt) |
| Optional method papers | [`METHODS.md`](medcalc_proj/docs/METHODS.md) |

The unchanged dataset contains 160 questions: 32 development and 128 test, with 16 separate examples. First calculate the answers independently using [`CALCULATOR_REFERENCE.md`](medcalc_proj/docs/CALCULATOR_REFERENCE.md) and the exported calculation worksheets. Then review the 24 shared direct responses, record human judgments, compare them with the current metric and examine agreement. Then implement CoT and one-shot CoT using [`data/examples.json`](medcalc_proj/data/examples.json), and review a suggested 16 supplementary reasoning responses. These are adjustable workload suggestions; all variants retain their original question-level development/validation partition. Report actual coverage. All independent labels and adjudication evidence must be preserved.

Raw generations and judgments, review forms and summaries are saved under `outputs/`. You can point this directory at mounted Drive. Existing annotation forms are protected from accidental overwriting. Download the submission archive and completed notebook before Colab ends; include original reviewer CSVs, adjudication, judge versions, group presentation/findings and individual reports. Unexecuted experiments must be identified as proposals. No real-model results are shipped.

Patient gold is allowed for evaluation, not solving. See [`DATA_LICENSE.md`](medcalc_proj/docs/DATA_LICENSE.md) for data attribution and terms.

After independent calculation, the notebook explicitly asks whether the original tolerance is appropriate and supplies an editable re-scoring cell. The original metric is preserved for comparison.

## Package layout

- `README.md`: start here.
- `medcalc_proj/PROJECT.pdf`: project overview and assignment instructions.
- `medcalc_proj/Medical_Calculation_Project.ipynb`: main student workspace.
- `medcalc_proj/docs/`: warm-up, annotation, judge and model guides, methods, calculator reference, data license, and Markdown source of the project document.
- `medcalc_proj/data/`: questions, examples, calculator summaries and references.
- `medcalc_proj/helpers/`: supporting Python modules.
- `medcalc_proj/requirements.txt`: dependencies.

Documentation paths such as `docs/` and `data/` are relative to `medcalc_proj/`. For local use, start Jupyter from that folder. In Colab, upload the complete ZIP when prompted; the setup cell enters that folder automatically.
