# Personal AI Agent

A personal AI assistant with a **Streamlit web dashboard** and a separate **Telegram bot**. The web app supports AI chat, notes and tasks; Telegram bot code remains available for deployment on a continuously running worker.

## Free Streamlit Community Cloud deployment (no hosting payment card)

1. Open https://share.streamlit.io/ and sign in with GitHub.
2. Click **Create app** → **Deploy a public app from GitHub**.
3. Choose repository `Atrayee321/Personal-AI-Agent`, branch `main`, main file path `streamlit_app.py`.
4. Open **Advanced settings** or **App settings → Secrets** and paste the following, replacing placeholders:

```toml
APP_PASSWORD = "choose-a-long-unique-password"
AI_PROVIDER = "gemini"
AI_MODEL = "gemini-3.1-flash-lite"
GEMINI_API_KEY = "your-private-gemini-api-key"
```

Create a Gemini API key at https://aistudio.google.com/apikey . Free API allowances depend on country, account eligibility, model and quota. If that model is unavailable, choose a supported Gemini model from AI Studio and change `AI_MODEL` accordingly. Do **not** put secrets in GitHub files or share them in chat.

5. Click **Deploy**. When the app starts, enter your `APP_PASSWORD` to unlock it.

### OpenAI alternative

Use the following secrets instead (OpenAI API billing is separate from ChatGPT subscriptions):

```toml
APP_PASSWORD = "choose-a-long-unique-password"
AI_PROVIDER = "openai"
AI_MODEL = "gpt-4o-mini"
OPENAI_API_KEY = "your-private-openai-api-key"
```

## Important limitations

- Streamlit Community Cloud may sleep when inactive. It does not run the Telegram polling bot 24/7.
- Web chat history, notes and tasks are **session-only**; they can disappear after restart, session expiration or reconnect. They are not synchronized with Telegram's SQLite database.
- This is a single-password demo app, not a multi-user production authentication system. Avoid storing highly sensitive personal data.
- The AI can respond to text but cannot execute external actions, browse, send emails or manage other accounts.
- This is an original implementation based on the tutorial description, not a copy of its exact code.

## Local Streamlit setup

```bash
git clone https://github.com/Atrayee321/Personal-AI-Agent.git
cd Personal-AI-Agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml to add private values
streamlit run streamlit_app.py
```

## Telegram bot (separate deployment)

For the Telegram bot, copy `.env.example` to `.env` and fill in `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_USER_IDS` and `OPENAI_API_KEY`. Run `python -m agent.main` or `docker compose up -d --build` on an always-on machine. Docker configuration is for the Telegram bot, **not** Streamlit hosting.

Telegram commands: `/help`, `/note`, `/notes`, `/task`, `/tasks`, `/done`, `/clear`.

## Testing

```bash
python -m unittest discover -s tests -v
python -m compileall -q agent streamlit_app.py
```

Never commit `.env`, `.streamlit/secrets.toml`, SQLite databases, or API tokens.
