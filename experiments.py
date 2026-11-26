from llm import ask, get_client

client = get_client()


def show(title, r):
    print(f"\n{title}")
    print(r["text"])
    print(f"[finish_reason={r['finish_reason']} | completion_tokens={r['completion_tokens']}]")


print("EKSPERIMEN 1: max_tokens (membatasi panjang jawaban)")
question = [{"role": "user", "content": "Jelaskan bagaimana internet bekerja."}]
for limit in (20, 80, 300):
    show(f"max_tokens={limit}", ask(client, question, temperature=0.7, max_tokens=limit))
print("\nCatatan: finish_reason='length' artinya jawaban TERPOTONG karena kena batas token.")

print("EKSPERIMEN 2: system message (mengatur perilaku model)")
user_q = "Apa itu machine learning?"
personas = {
    "Tanpa system message": None,
    "Guru SD": "Kamu guru SD. Jelaskan dengan bahasa sangat sederhana, pakai analogi anak-anak. Bahasa Indonesia.",
    "Profesor formal": "Kamu profesor ilmu komputer. Jawab formal, teknis, dan ringkas. Bahasa Indonesia.",
    "Bajak laut": "Kamu bajak laut yang ramah. Jawab dengan gaya bajak laut yang lucu. Bahasa Indonesia.",
}
for name, system in personas.items():
    msgs = ([{"role": "system", "content": system}] if system else []) + [
        {"role": "user", "content": user_q}
    ]
    show(name, ask(client, msgs, temperature=0.7, max_tokens=150))
