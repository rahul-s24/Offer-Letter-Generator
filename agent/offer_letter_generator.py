from transformers import pipeline

generator = pipeline("text2text-generation", model="google/flan-t5-large", device=-1)

def generate_letter(prompt: str) -> str:
    output = generator(prompt, max_length=1024, do_sample=False)[0]["generated_text"]
    return output.strip()
