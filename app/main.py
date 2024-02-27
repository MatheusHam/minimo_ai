from typing import List
from transformers import AutoTokenizer, AutoModelForCausalLM
import pandas as pd
from dotenv import load_dotenv

from utils import format_gemma_output 
import streamlit as st


load_dotenv()
st.session_state["loaded"] = False

                                             
def batch_llm(
        user_inputs: list, 
        output_instruction: str,
        model_name: str = "google/gemma-2b-it",
):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
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
        prompts.append(format_gemma_output("",prompt))

    return pd.DataFrame({"prompt": prompts, "response": responses})



def execute():
    user_inputs = st.session_state["user_inputs"].split("\n")
    df = batch_llm(user_inputs, st.session_state["output_instruction"])
    st.dataframe(df)

    

st.title("Sentiment Classification")
st.session_state["user_inputs"] = st.text_area("Enter your feelings (one per line):")
st.session_state["output_instruction"] = st.text_input("Output instruction:")
st.button("Run", on_click=execute)

