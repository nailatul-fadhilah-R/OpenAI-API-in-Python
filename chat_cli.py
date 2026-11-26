import argparse

from llm import DEFAULT_MODEL, ask, get_client

DEFAULT_SYSTEM = "Kamu adalah asisten AI yang membantu, ramah, dan menjawab dalam Bahasa Indonesia."


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--temperature", type=float, default=0.7)
    p.add_argument("--max-tokens", type=int, default=500)
    p.add_argument("--system", default=DEFAULT_SYSTEM)
    args = p.parse_args()

    client = get_client()
    model, temperature, max_tokens, system = args.model, args.temperature, args.max_tokens, args.system
    history = [{"role": "system", "content": system}]
    total_used = 0

    print(f"Model={model} | temperature={temperature} | max_tokens={max_tokens}")
    print("Ketik /help untuk perintah, /exit untuk keluar.\n")

    while True:
        try:
            user_input = input("Kamu  : ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSampai jumpa!")
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            cmd, _, arg = user_input.partition(" ")
            arg = arg.strip()
            if cmd == "/exit":
                print("Sampai jumpa!")
                break
            elif cmd == "/reset":
                history = [{"role": "system", "content": system}]
                print("[riwayat direset]")
            elif cmd == "/system" and arg:
                system = arg
                history = [{"role": "system", "content": system}]
                print("[system message diganti, riwayat direset]")
            elif cmd == "/temp" and arg:
                try:
                    t = float(arg)
                    if 0 <= t <= 2:
                        temperature = t
                        print(f"[temperature = {temperature}]")
                    else:
                        print("Temperature harus antara 0 dan 2.")
                except ValueError:
                    print("Masukkan angka, contoh: /temp 0.5")
            elif cmd == "/max" and arg.isdigit():
                max_tokens = int(arg)
                print(f"[max_tokens = {max_tokens}]")
            elif cmd == "/usage":
                print(f"[total token terpakai sesi ini: {total_used}]")
            else:
                print(__doc__)
            continue

        history.append({"role": "user", "content": user_input})
        r = ask(client, history, model=model, temperature=temperature, max_tokens=max_tokens)
        history.append({"role": "assistant", "content": r["text"]})
        total_used += r["total_tokens"]

        print(f"\nAI    : {r['text']}")
        note = " (TERPOTONG, naikkan /max)" if r["finish_reason"] == "length" else ""
        print(f"        [token: {r['total_tokens']}{note}]\n")


if __name__ == "__main__":
    main()
