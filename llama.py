from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
model = AutoModelForCausalLM.from_pretrained("daryl149/llama-2-7b-chat-hf",
                                             device_map='auto',
                                             torch_dtype=torch.float16,
                                             load_in_8bit=True)
model = model.eval()
tokenizer = AutoTokenizer.from_pretrained("daryl149/llama-2-7b-chat-hf",user_fast=False)
tokenizer.pad_token = tokenizer.eos_token
input_ids = tokenizer('<s>Human: 什麼是自然處理語言\n</s><s>Assistant: ', return_tensors='pt', add_special_tokens=False).input_ids.to('cuda')
generate_input = {
    'input_ids': input_ids,
    'max_length': 512,
    'do_sample': True,
    'top_k': 50,
    'top_p': 0.95,
    'temperature': 0.3,
    "repetition_penalty": 1.3,
    "eos_token_id": tokenizer.eos_token_id,
    "bos_token_id": tokenizer.bos_token_id,
    "pad_token_id": tokenizer.pad_token_id
}
generate_ids = model.generate(**generate_input)
text = tokenizer.decode(generate_ids[0])
print(text)