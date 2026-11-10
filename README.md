# Personal AI Agent — Telegram Edition

**Live website:** [Open Personal AI Agent](https://personal-ai-agent-ddckhx3sqrmfdhpknnepkc.streamlit.app/)


A deployable Python personal assistant controlled from Telegram. Features: Gemini-powered chat, per-user SQLite conversation memory, notes, tasks, basic authorization, Docker deployment. This is an original starter implementation based on the user's description of a tutorial, **not** a verified reproduction of the video's exact code. Native iMessage integration is **not included**.

## Requirements
- Python 3.11–3.12 (or Docker)
- Telegram bot token from [@BotFather](https://t.me/BotFather)
- Your numeric Telegram user ID (e.g. from [@userinfobot](https://t.me/userinfobot))
- Gemini API key from https://aistudio.google.com/apikey (free-tier availability and quotas depend on account and model)

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
