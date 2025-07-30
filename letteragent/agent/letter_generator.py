from transformers import pipeline
from agent.prompt_builder import build_prompt

# Use an open-access instruction-tuned model
generator = pipeline("text2text-generation", model="google/flan-t5-base", device_map="auto")

def generate_letter(employee, policy_chunks):
    prompt = build_prompt(employee, policy_chunks)

    # Generate letter
    output = generator(prompt, max_new_tokens=1024, do_sample=False)
    return output[0]['generated_text']
