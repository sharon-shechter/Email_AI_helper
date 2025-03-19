from gpt4all import GPT4All



model_name = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")

# Generate a response
prompt = """
what is the capital of itali? answer in one word only.
"""
response = model_name.generate(prompt)  

# Print the response
print(response)
