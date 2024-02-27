from typing import List
from transformers import AutoTokenizer, AutoModelForCausalLM
import pandas as pd
from dotenv import load_dotenv

from utils import format_gemma_output 


load_dotenv()

def batch_llm(
        user_inputs: list, 
        output_instruction: str,
        model: str = "gemma_instruct_2b_en",
):

    tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it")
    model = AutoModelForCausalLM.from_pretrained("google/gemma-2b-it")
    prompts, responses = [], []

    for text_input in user_inputs:
        instruction = f"<start_of_turn>model{output_instruction}<end_of_turn>\n"
        user_input = f"<start_of_turn>user{text_input}<end_of_turn>\n"
        response = "<start_of_turn>model "
        prompt = instruction + user_input + response
        input_ids = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(**input_ids, max_length=1000, num_return_sequences=1)
        formatted_response = format_gemma_output(prompt, tokenizer.decode(outputs[0]))
        responses.append(formatted_response)
        prompts.append(prompt)

    return pd.DataFrame({"prompt": prompts, "response": responses})


if __name__ == "__main__":
    user_inputs = ["I am feeling sad", "I am feeling happy"]
    output_instruction = "Categorize the user input as positive or negative."
    df = batch_llm(user_inputs, output_instruction)
    print(df.head())