# Choosing and running a model

Start with **Qwen/Qwen2.5-3B-Instruct**, in 4-bit mode. A smaller checkpoint is useful for debugging. Keep the checkpoint fixed for the principal method comparison. Model size alone does not establish which one will do best.

| Helper key | Checkpoint / model | Use |
|---|---|---|
| `phi4_mini` | [microsoft/Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct) | Non-Qwen small-model option |
| `llama32_3b` | [meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) | Small Llama option; gated Hugging Face access |
| `llama31_8b` | [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | Larger Llama option; gated access |
| `qwen3_small` | [Qwen/Qwen3-4B](https://huggingface.co/Qwen/Qwen3-4B) | Qwen3 option |
| `qwen3_larger` | [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | Larger Qwen3 option |
| `qwen3_14b` | [Qwen/Qwen3-14B](https://huggingface.co/Qwen/Qwen3-14B) | Larger-memory option; not the default Colab choice |
| `qwen_small` | [Qwen/Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) | Small smoke-test option |
| `qwen_default` | [Qwen/Qwen2.5-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct) | Convenient starting checkpoint |
| `qwen_larger` | [Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) | Additional comparison option |
| `gpt4o_mini` (endpoint) | [gpt-4o-mini](https://developers.openai.com/api/docs/models/gpt-4o-mini) | Optional API model; separate credentials and possible cost |
| `gpt4o` (endpoint) | [gpt-4o](https://developers.openai.com/api/docs/models/gpt-4o) | Optional API model; separate credentials and possible cost |

The first nine entries use `HFModel` and `MODEL_OPTIONS`. GPT entries use `EndpointModel` and `API_MODEL_OPTIONS`, not `HFModel`. Use one model or another justified checkpoint; you do not need to compare all these models. API access is optional and depends on the instructor's resources.

To choose a local model, change the notebook's `MODEL_KEY`, for example to `phi4_mini` or `llama32_3b`. The helper uses each checkpoint's own chat template. Avoid assuming that every listed model fits every Colab GPU; larger models and long examples need more memory.

Open each model card to review its terms and usage. The 3B Qwen2.5 card has a different license from several other Qwen checkpoints. Qwen3 has a thinking-mode option: the helper sets `enable_thinking=False` for a consistent observable-output interface and records that choice. A prompt requesting a worked solution still works in this mode. If you enable thinking, disclose it and keep comparisons consistent.

## Colab steps

1. Select a GPU runtime and run the requirements cell. Retain Colab's supplied CUDA-compatible PyTorch. Restart the runtime if Colab requests it, then rerun setup/import cells.
2. Set `MODEL_KEY`, `four_bit`, and the token budget in the notebook model-loading cell. The helper uses the Hugging Face tokenizer's chat template, loads the model with `device_map='auto'`, and decodes only new tokens.
3. Run one question first. Inspect the raw response and parsed numeric answer. Then run the 32-question development set. Decide the final token budget before comparing methods on test data.
4. Use greedy decoding (`temperature=0`) for the main single-solution experiments. Self-consistency needs nonzero sampling temperature. Record that method-specific difference.
5. Run one checkpoint per Colab runtime. Restart before loading a different large checkpoint to avoid keeping old model weights in memory.

Four-bit loading reduces weight memory, but context and generation also use memory. Colab GPUs, availability and session lengths vary; no runtime duration is guaranteed. Time the development run and estimate a full run as `elapsed_seconds / question_count * 128`, multiplying by calls per question where appropriate. The helper runs one question at a time, saves every result immediately, and resumes matching configurations.

If you get CUDA out of memory: restart the runtime, use the 1.5B or 3B model in 4-bit mode, and inspect example/context length. A shorter output limit may truncate needed work, so choose it on development data and report token-limit rates. Do not silently cut patient notes to fit.

## Access and secrets

Qwen and Phi checkpoints generally do not require gated-model approval. Llama checkpoints require accepting the model license and obtaining access on Hugging Face. Store an authorized `HF_TOKEN` in Colab **Secrets**, then authenticate before loading a Llama checkpoint:

```python
from google.colab import userdata
from huggingface_hub import login
login(token=userdata.get("HF_TOKEN"))
```

Do not print or submit the token. For an optional hosted or local server, use `EndpointModel`; read `MODEL_API_KEY` from Secrets into an environment variable. Never put credentials in a submitted notebook or archive.

To use an optional GPT endpoint instead of the HF loading line:

```python
import os
from google.colab import userdata
from helpers.models import EndpointModel, API_MODEL_OPTIONS
os.environ["MODEL_API_KEY"] = userdata.get("MODEL_API_KEY")
model = EndpointModel(API_MODEL_OPTIONS["gpt4o_mini"],
                      base_url="https://api.openai.com/v1")
```

Only run this with an authorized API account and an agreed course budget. No hosted-model calls are needed to complete the project.

The endpoint helper uses an OpenAI-compatible Chat Completions interface. Some providers require different token arguments or do not support the same sampling options; adapt the adapter and disclose the provider. Paid APIs are optional. A server being OpenAI-compatible does not mean it is operated by OpenAI.

## Installation and reproducibility

`requirements.txt` pins the core inference libraries to a coherent Transformers 4.x setup. Do not upgrade libraries midway through a comparison. Save `pip freeze`, GPU name, exact resolved model revision and quantization configuration. See the official [Transformers bitsandbytes guide](https://huggingface.co/docs/transformers/quantization/bitsandbytes) for the quantization API.

The package was checked for dataset integrity and with CPU/offline infrastructure tests. Full GPU inference in a live Colab runtime has not been pre-executed; the notebook's one-question smoke run is the first runtime compatibility check. No benchmark scores are prefilled or fabricated.

## Judge models in this project

Reuse the loaded small Qwen model for judging if memory or budget is limited. Set the judge output budget high enough for structured labels and evidence (the notebook starts at 1024 tokens); retain truncated or failed judgments. For an optional GPT comparison, keep the same rubric, candidate responses, references and requested output budget. Run models sequentially if the GPU cannot hold two instances. API access is optional; an unperformed comparison belongs in the individual report as a proposal. Neither GPT nor Qwen judgments replace the independently annotated human reference. Record the exact endpoint/model and settings returned by your provider.
