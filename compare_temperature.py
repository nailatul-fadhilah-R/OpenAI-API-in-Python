import argparse
import json
import os
from datetime import datetime

from llm import DEFAULT_MODEL, ask, get_client

DEFAULT_PROMPTS = [
    "Apa ibu kota Indonesia? Jawab singkat.",                       # faktual
    "Buat satu slogan kreatif untuk kedai kopi bernama 'Senja'.",   # kreatif
]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", help="Prompt kustom (default: 1 faktual + 1 kreatif)")
    p.add_argument("--temps", type=float, nargs="+", default=[0.0, 0.7, 1.2, 1.8])
    p.add_argument("--runs", type=int, default=3, help="Jumlah pengulangan per temperature")
    p.add_argument("--max-tokens", type=int, default=100)
    p.add_argument("--model", default=DEFAULT_MODEL)
    args = p.parse_args()

    client = get_client()
    prompts = [args.prompt] if args.prompt else DEFAULT_PROMPTS
    results = []

    for prompt in prompts:
        print("\n" + "=" * 70)
        print(f"PROMPT: {prompt}")
        print("=" * 70)
        messages = [
            {"role": "system", "content": "Kamu asisten yang menjawab dalam Bahasa Indonesia."},
            {"role": "user", "content": prompt},
        ]
        for temp in args.temps:
            print(f"\n--- temperature = {temp} ---")
            outputs = []
            for i in range(1, args.runs + 1):
                r = ask(client, messages, model=args.model, temperature=temp, max_tokens=args.max_tokens)
                outputs.append(r["text"])
                print(f"  [{i}] {r['text']}")
            unique = len(set(outputs))
            print(f"  => {unique} jawaban unik dari {args.runs} percobaan")
            results.append({"prompt": prompt, "temperature": temp, "outputs": outputs})

    os.makedirs("results", exist_ok=True)
    path = f"results/temperature_{datetime.now():%Y%m%d_%H%M%S}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nHasil disimpan di: {path}")
    print("Pengamatan: temperature rendah -> konsisten/deterministik; tinggi -> beragam & kreatif (tapi bisa ngawur).")


if __name__ == "__main__":
    main()
