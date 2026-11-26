from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Kamu adalah asisten yang ramah dan menjawab dalam Bahasa Indonesia."},
        {"role": "user", "content": "Jelaskan apa itu token pada LLM dalam 2 kalimat."},
    ],
)

print(response.choices[0].message.content)
print("\n Usage ")
print("Prompt tokens    :", response.usage.prompt_tokens)
print("Completion tokens:", response.usage.completion_tokens)
print("Total tokens     :", response.usage.total_tokens)
