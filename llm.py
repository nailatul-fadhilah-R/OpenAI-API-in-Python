import os
import sys

from dotenv import load_dotenv
from openai import (
    APIConnectionError,
    AuthenticationError,
    BadRequestError,
    OpenAI,
    RateLimitError,
)

load_dotenv()  # membaca file .env (OPENAI_API_KEY, OPENAI_MODEL)

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def get_client() -> OpenAI:
    """Membuat client. API key dibaca otomatis dari env OPENAI_API_KEY."""
    if not os.getenv("OPENAI_API_KEY"):
        sys.exit(
            "OPENAI_API_KEY tidak ditemukan.\n"
            "Buat file .env (salin dari .env.example) lalu isi API key kamu."
        )
    return OpenAI()


def ask(client, messages, model=DEFAULT_MODEL, temperature=1.0, max_tokens=300):
    """
    Memanggil client.chat.completions.create() dan mengembalikan dict ringkas:
    text, finish_reason, prompt_tokens, completion_tokens, total_tokens.
    """
    params = dict(model=model, messages=messages, temperature=temperature)

    try:
        try:
            resp = client.chat.completions.create(max_tokens=max_tokens, **params)
        except BadRequestError as e:
            # Model baru (mis. seri o / gpt-5) memakai max_completion_tokens
            if "max_completion_tokens" in str(e):
                resp = client.chat.completions.create(
                    max_completion_tokens=max_tokens, **params
                )
            else:
                raise
    except AuthenticationError:
        sys.exit("API key salah/tidak valid. Cek lagi isi file .env kamu.")
    except RateLimitError:
        sys.exit("Rate limit atau kuota/saldo habis. Cek billing di platform.openai.com.")
    except APIConnectionError:
        sys.exit("Gagal terhubung ke OpenAI. Cek koneksi internet kamu.")
    except BadRequestError as e:
        sys.exit(f"Request ditolak: {e}\n(Beberapa model tidak mendukung parameter temperature.)")

    choice = resp.choices[0]
    return {
        "text": (choice.message.content or "").strip(),
        "finish_reason": choice.finish_reason,  # "stop" = selesai, "length" = terpotong max_tokens
        "prompt_tokens": resp.usage.prompt_tokens,
        "completion_tokens": resp.usage.completion_tokens,
        "total_tokens": resp.usage.total_tokens,
    }
