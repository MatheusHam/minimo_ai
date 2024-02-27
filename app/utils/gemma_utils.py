def format_gemma_output(input: str, response: str):
    tags = [
        input,
        "<bos>",
        "<eos>",
        "<start_of_turn>user",
        "<end_of_turn>model",
        "<start_of_turn>model",
        "<end_of_turn>user",
        "\n",
        
    ]
    for tag in tags:
        response = response.replace(tag, "")
    return response