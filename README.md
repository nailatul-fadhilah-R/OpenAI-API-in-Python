# OpenAI-API-in-Python

Instead of using ChatGPT in the browser, this project calls OpenAI models directly from Python to get control over the system message, temperature, token limits, and to use model responses in my own code. This project is from [roadmap.sh](https://roadmap.sh/projects/openai-api-python)
 
## Features
 
- Client setup with the current `openai >= 1.0.0` syntax
- API key stored in an environment variable (`python-dotenv`)
- First call with `client.chat.completions.create()`
- Experiments with `temperature`, `max_tokens`, and system messages
- Interactive terminal chatbot
- Side-by-side comparison of outputs at different temperatures
## Files
 
| File | Purpose |
|---|---|
| `first_call.py` | Minimal first API call with token usage |
| `experiments.py` | `max_tokens` and system message experiments |
| `compare_temperature.py` | Same prompt at several temperatures, saved to JSON |
| `chat_cli.py` | Interactive chatbot with conversation memory |
| `llm.py` | Shared client and error handling |
 
## Setup
 
```bash
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env         # macOS/Linux: cp .env.example .env
```
 
Put your key in `.env` (never commit it):
 
```
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o-mini
```
 
## Run Order
 
```bash
python first_call.py
python experiments.py
python compare_temperature.py
python chat_cli.py
```
 
## Key Takeaways
 
- **Tokens:** the unit models read and write; they determine cost and length limits.
- **`max_tokens`:** caps reply length; a cut-off reply returns `finish_reason="length"`.
- **`temperature`:** low values give consistent answers, high values give varied and creative ones.
- **System message:** changes tone and style for the same question.
## Notes
 
- The API requires account credit and is billed separately from a ChatGPT subscription.
- Any OpenAI-compatible provider can be used by setting `OPENAI_BASE_URL` in `.env`.
