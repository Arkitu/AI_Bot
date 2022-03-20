from transformers import pipeline, set_seed

generator = pipeline('text-generation', model='gpt2')
set_seed(42)
result = generator("Julie: Hi neighbor !\nGeorges: Hi ! How are you today ?\nJulie: Good. And you ?\n", max_length=200, num_return_sequences=1)
print(result[0]["generated_text"])