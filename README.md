# Personal AI Agent — Telegram Edition

**Live website:** [Open Personal AI Agent](https://personal-ai-agent-ddckhx3sqrmfdhpknnepkc.streamlit.app/)


A deployable Python personal assistant controlled from Telegram. Features: Gemini-powered chat, per-user SQLite conversation memory, notes, tasks, basic authorization, Docker deployment. This is an original starter implementation based on the user's description of a tutorial, **not** a verified reproduction of the video's exact code. Native iMessage integration is **not included**.

## Requirements
- Python 3.11–3.12 (or Docker)
- Telegram bot token from [@BotFather](https://t.me/BotFather)
- Your numeric Telegram user ID (e.g. from [@userinfobot](https://t.me/userinfobot))
- Gemini API key from https://aistudio.google.com/apikey (free-tier availability and quotas depend on account and model)

## Local setup (macOS / Linux)
```bash
git clone https://github.com/Atrayee321/Personal-AI-Agent.git
cd Personal-AI-Agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```
Edit `.env` and fill in `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_USER_IDS`, and `GEMINI_API_KEY`. The default model is `gemini-3.1-flash-lite`; availability and free-tier quotas vary. Never commit or share `.env`.

Run:
```bash
python -m agent.main
```
Open your bot in Telegram, tap Start, and send `/help`.

## Commands
- `/note Buy milk` — save a note
- `/notes` — list latest notes
- `/task Submit assignment` — create task
- `/tasks` — list tasks
- `/done 1` — complete task by ID
- `/clear` — delete stored AI chat history (notes/tasks remain)
- Ordinary messages — AI chat

## Test
```bash
python -m unittest discover -s tests -v
python -m compileall -q agent
```

## Docker deployment
1. Install Docker Engine / Docker Desktop on a computer or VPS.
2. Copy this folder to the server and configure `.env` there.
3. Run `docker compose up -d --build`.
4. Check `docker compose logs -f agent`.
5. Keep `./data` on persistent storage; backups should include `data/agent.db`.

This bot uses **long polling**, so it needs a continuously running background process, not a static site or request-only serverless hosting. A paid or free-tier VPS/container host with an always-on worker and persistent disk can work; free hosting availability varies. No inbound HTTP port is needed.

## Security and limitations
- Only numeric IDs in `TELEGRAM_ALLOWED_USER_IDS` can use the bot. Keep the token and API key private.
- AI requests are sent to the configured Google Gemini API. Chat and notes/tasks are stored locally in unencrypted SQLite; secure your host and backups.
- Chat messages are capped at 6000 characters; model output is limited for cost control.
- The bot cannot send emails, access accounts, execute shell commands, browse the web, or act on third-party services. No such abilities are implied.
- No automatic reminders or iMessage integration in this starter edition.
- To remove stored data, stop the app and securely manage/delete the database file.
- This implementation is intended for a single running bot instance; do not run multiple pollers with the same Telegram token.

## Streamlit web dashboard (separate from Telegram)

The website is hosted on Streamlit Community Cloud. Deploy this repository with main file path `streamlit_app.py`, branch `main`. Set the following in **Streamlit Cloud → App settings → Secrets** (do not commit secrets):

```toml
APP_PASSWORD = "choose-a-long-private-password"
GEMINI_API_KEY = "your-private-gemini-api-key"
GEMINI_MODEL = "gemini-3.1-flash-lite"
```

The model must be enabled for your Gemini API key; availability and free quotas vary. For local testing, create `.streamlit/secrets.toml` based on `.streamlit/secrets.toml.example` and run `streamlit run streamlit_app.py`.

Web chat, notes, and tasks live only in the browser session; they may disappear after restart/reconnect and are not synchronized with the Telegram SQLite database. The app uses one shared password and is not suitable for multi-user private accounts. Streamlit hosting does not keep the Telegram polling bot running continuously. The Telegram bot must run separately on an always-on host.
