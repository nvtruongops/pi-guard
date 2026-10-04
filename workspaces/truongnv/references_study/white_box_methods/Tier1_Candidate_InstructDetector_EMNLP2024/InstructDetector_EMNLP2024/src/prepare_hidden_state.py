import torch
import argparse
import numpy as np
import pickle
from transformers import AutoTokenizer, AutoModelForCausalLM
from sklearn.utils import shuffle
from tqdm import tqdm
from utils import *


def parse_args():
    parser = argparse.ArgumentParser(description="Run hidden state extraction experiment")
    parser.add_argument("--model_name", type=str, default="meta-llama/Llama-3.1-8B-Instruct",
                       help="HuggingFace model name")
    parser.add_argument("--train_data_size", type=int, default=200,
                       help="Number of training samples to use")
    parser.add_argument("--data_type", type=str, choices=["wiki", "news"], default="wiki",
                       help="Type of training data (wiki/news)")
    parser.add_argument("--instruction_type", type=str, choices=["1", "2"], default="1",
                       help="Type of instruction (1/2)")
    return parser.parse_args()

def get_data_func(data_type, is_train=True):
    if data_type == "wiki":
        return get_data_wiki_train() if is_train else get_data_wiki_test()
    else:
        return get_data_news_train() if is_train else get_data_news_test()

def get_instruction_func(instruction_type, is_train=True):
    if instruction_type == "1":
        return get_instruction_1_train() if is_train else get_instruction_1_test()
    else:
        return get_instruction_2_train() if is_train else get_instruction_2_test()

def process_prompts_instruct(prompt):
    chat = [{"role": "user", "content": f"{prompt}"}]
    return tokenizer.apply_chat_template(
        chat, tokenize=False, add_generation_prompt=True
    )

def get_hidden_states(data):
    inputs = tokenizer(process_prompts_instruct(data), return_tensors='pt', padding=True, truncation=True)
    input_ids = inputs['input_ids'].to(device)
    with torch.no_grad():
        outputs = model(input_ids, output_hidden_states=True)
    hidden_states = outputs.hidden_states
    last_token_hidden_states = []
    for layer_hidden_state in hidden_states:
        last_token_hidden_state = layer_hidden_state[:, -1, :].cpu().numpy()
        last_token_hidden_states.append(last_token_hidden_state.squeeze())
    return np.array(last_token_hidden_states)

args = parse_args()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained(args.model_name)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(args.model_name, output_hidden_states=True).to(device)

instructions_train = get_instruction_func(args.instruction_type, is_train=True)
data_train = get_data_func(args.data_type, is_train=True)[:args.train_data_size/2]
mixed_data_train = []
for i, context in enumerate(data_train):
    attack = instructions_train[i % len(instructions_train)]
    mixed_data_train.append(insert_middle(context, attack))
data_embeddings_train = [get_hidden_states(data) for data in tqdm(data_train, desc="Processing data_train")]
with open('hidden_states/train_data.pkl', 'wb') as f:
    pickle.dump(data_embeddings_train, f)
instruction_embeddings_train = [get_hidden_states(data) for data in tqdm(mixed_data_train, desc="Processing mixed_data_train")]
with open('hidden_states/train_instruction.pkl', 'wb') as f:
    pickle.dump(instruction_embeddings_train, f)
x_train = np.array(data_embeddings_train + instruction_embeddings_train)
y_train = np.array([0] * len(data_embeddings_train) + [1] * len(instruction_embeddings_train))
x_train, y_train = shuffle(x_train, y_train, random_state=42)


instructions_test = get_instruction_func("1", is_train=False)
data_test = get_data_func("wiki", is_train=False)
mixed_data_test = []
for i, context in enumerate(data_test):
    attack = instructions_test[i % len(instructions_test)]
    mixed_data_test.append(insert_middle(context, attack))
data_embeddings_test = [get_hidden_states(data) for data in tqdm(data_test, desc="Processing data_test")]
with open('hidden_states/test_data1.pkl', 'wb') as f:
    pickle.dump(data_embeddings_test, f)
instruction_embeddings_test = [get_hidden_states(data) for data in tqdm(mixed_data_test, desc="Processing mixed_data_test")]
with open('hidden_states/test_instruction1.pkl', 'wb') as f:
    pickle.dump(instruction_embeddings_test, f)


data_test = get_data_func("news", is_train=False)
mixed_data_test = []
for i, context in enumerate(data_test):
    attack = instructions_test[i % len(instructions_test)]
    mixed_data_test.append(insert_middle(context, attack))
data_embeddings_test = [get_hidden_states(data) for data in tqdm(data_test, desc="Processing data_test")]
with open('hidden_states/test_data2.pkl', 'wb') as f:
    pickle.dump(data_embeddings_test, f)
instruction_embeddings_test = [get_hidden_states(data) for data in tqdm(mixed_data_test, desc="Processing mixed_data_test")]
with open('hidden_states/test_instruction2.pkl', 'wb') as f:
    pickle.dump(instruction_embeddings_test, f)

instructions_test = get_instruction_func("2", is_train=False)
data_test = get_data_func("wiki", is_train=False)
mixed_data_test = []
for i, context in enumerate(data_test):
    attack = instructions_test[i % len(instructions_test)]
    mixed_data_test.append(insert_middle(context, attack))
data_embeddings_test = [get_hidden_states(data) for data in tqdm(data_test, desc="Processing data_test")]
with open('hidden_states/test_data3.pkl', 'wb') as f:
    pickle.dump(data_embeddings_test, f)
instruction_embeddings_test = [get_hidden_states(data) for data in tqdm(mixed_data_test, desc="Processing mixed_data_test")]
with open('hidden_states/test_instruction3.pkl', 'wb') as f:
    pickle.dump(instruction_embeddings_test, f)

data_test = get_data_func("news", is_train=False)
mixed_data_test = []
for i, context in enumerate(data_test):
    attack = instructions_test[i % len(instructions_test)]
    mixed_data_test.append(insert_middle(context, attack))
data_embeddings_test = [get_hidden_states(data) for data in tqdm(data_test, desc="Processing data_test")]
with open('hidden_states/test_data4.pkl', 'wb') as f:
    pickle.dump(data_embeddings_test, f)
instruction_embeddings_test = [get_hidden_states(data) for data in tqdm(mixed_data_test, desc="Processing mixed_data_test")]
with open('hidden_states/test_instruction4.pkl', 'wb') as f:
    pickle.dump(instruction_embeddings_test, f)