"""Single-question HF inference, with optional OpenAI-compatible endpoint support."""
import os
import copy
import hashlib

MODEL_OPTIONS = {
 'qwen_small':'Qwen/Qwen2.5-1.5B-Instruct',
 'qwen_default':'Qwen/Qwen2.5-3B-Instruct',
 'qwen_larger':'Qwen/Qwen2.5-7B-Instruct',
 'qwen3_small':'Qwen/Qwen3-4B',
 'qwen3_larger':'Qwen/Qwen3-8B',
 'qwen3_14b':'Qwen/Qwen3-14B',
 'phi4_mini':'microsoft/Phi-4-mini-instruct',
 'llama32_3b':'meta-llama/Llama-3.2-3B-Instruct',
 'llama31_8b':'meta-llama/Llama-3.1-8B-Instruct',
}

# Optional endpoint identifiers; availability is provider-dependent.
API_MODEL_OPTIONS = {'gpt4o_mini':'gpt-4o-mini', 'gpt4o':'gpt-4o'}

class HFModel:
    def __init__(self, model_id=MODEL_OPTIONS['qwen_default'], four_bit=True, max_new_tokens=768,
                 temperature=0.0, seed=2026, revision=None):
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, set_seed
        if not torch.cuda.is_available():
            raise RuntimeError('Choose Runtime > Change runtime type > GPU in Colab. Use offline smoke checks without a GPU.')
        set_seed(seed)
        self.torch=torch
        self.tokenizer=AutoTokenizer.from_pretrained(model_id, revision=revision)
        config=dict(device_map='auto', torch_dtype=torch.float16, revision=revision)
        if four_bit:
            config['quantization_config']=BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4',
                bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16)
        self.model=AutoModelForCausalLM.from_pretrained(model_id, **config).eval()
        self.config={'backend':'hf','model_id':model_id,'four_bit':four_bit,'max_new_tokens':max_new_tokens,
                     'temperature':temperature,'seed':seed,'revision':getattr(self.model.config,'_commit_hash',revision),
                     'thinking':False}
        self.max_new_tokens=max_new_tokens;self.temperature=temperature
        self.context_limit=min(int(getattr(self.model.config,'max_position_embeddings',32768)),32768)
        self.last_usage={};self.call_log=[]

    def reset_task_seed(self, task_id, method):
        from transformers import set_seed
        key=f'{self.config["seed"]}:{task_id}:{method}'
        seed=int(hashlib.sha256(key.encode()).hexdigest()[:8],16)
        set_seed(seed)

    def generate(self, messages, temperature=None):
        temp=self.temperature if temperature is None else temperature
        extra={'enable_thinking':False} if 'Qwen3' in self.config['model_id'] else {}
        prompt=self.tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,**extra)
        inputs=self.tokenizer(prompt,return_tensors='pt').to(self.model.device)
        n=inputs['input_ids'].shape[-1]
        if n+self.max_new_tokens>self.context_limit:
            raise ValueError('Context too long; do not silently truncate clinical facts. Redesign your prompt or select a longer-context model.')
        options=dict(max_new_tokens=self.max_new_tokens,do_sample=temp>0,
                     pad_token_id=self.tokenizer.eos_token_id)
        if temp>0:options.update(temperature=temp,top_p=.95)
        with self.torch.inference_mode():
            out=self.model.generate(**inputs,**options)
        generated=out[0,n:]
        self.last_usage={'input_tokens':n,'output_tokens':len(generated),
                         'hit_token_limit':len(generated)>=self.max_new_tokens}
        text=self.tokenizer.decode(generated,skip_special_tokens=True)
        self.call_log.append({'messages':copy.deepcopy(messages),'raw':text,'usage':self.last_usage.copy()})
        return text

class EndpointModel:
    """Optional server or paid endpoint. Only uses an environment variable for the key."""
    def __init__(self, model_id, base_url, key_env='MODEL_API_KEY', max_new_tokens=768, temperature=0):
        from openai import OpenAI
        self.client=OpenAI(base_url=base_url,api_key=os.environ[key_env],timeout=120,max_retries=2)
        self.config={'backend':'endpoint','model_id':model_id,'base_url':base_url,
                     'max_new_tokens':max_new_tokens,'temperature':temperature}
        self.last_usage={};self.call_log=[]
    def generate(self,messages,temperature=None):
        r=self.client.chat.completions.create(model=self.config['model_id'],messages=messages,
            max_tokens=self.config['max_new_tokens'],temperature=self.config['temperature'] if temperature is None else temperature)
        self.last_usage=r.usage.model_dump() if r.usage else {}
        text=r.choices[0].message.content or ''
        self.call_log.append({'messages':copy.deepcopy(messages),'raw':text,'usage':self.last_usage.copy()})
        return text
