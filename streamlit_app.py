"""Password-protected Streamlit interface; Telegram bot runs separately."""
import hmac
import logging
import os
import time

import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import ServerError

logger = logging.getLogger(__name__)
st.set_page_config(page_title="Personal AI Agent", page_icon="🤖", layout="centered")


def setting(name, default=""):
    try:
        value = st.secrets.get(name)
        if value is not None:
            return str(value)
    except (FileNotFoundError, KeyError):
        pass
    return os.getenv(name, default)


def require_login():
    password = setting("APP_PASSWORD")
    if not password:
        st.error("Configure APP_PASSWORD in Streamlit Cloud → App settings → Secrets.")
        st.stop()
    if st.session_state.get("authenticated"):
        return
    st.title("🔐 Personal AI Agent")
    with st.form("login"):
        entered = st.text_input("App password", type="password")
        submit = st.form_submit_button("Unlock")
    if submit:
        if hmac.compare_digest(entered, password):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")
    st.stop()


def generate_answer(messages):
    api_key = setting("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured")
    client = genai.Client(api_key=api_key)
    contents = [
        types.Content(
            role="user" if item["role"] == "user" else "model",
            parts=[types.Part.from_text(text=item["content"])],
        )
        for item in messages[-12:]
    ]
    model = setting("GEMINI_MODEL", "gemini-3.1-flash-lite")
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction="You are a helpful personal AI assistant. Never claim to have performed actions you cannot perform.",
                    max_output_tokens=800,
                ),
            )
            return response.text or "No response generated."
        except ServerError as exc:
            if getattr(exc, "code", None) != 503 or attempt == 2:
                raise
            time.sleep(2 ** attempt)


require_login()
st.title("🤖 Personal AI Agent")
st.caption("Gemini AI chat · Notes · Tasks")

for key in ("messages", "notes", "tasks"):
    if key not in st.session_state:
        st.session_state[key] = []

with st.sidebar:
    page = st.radio("Workspace", ["AI Chat", "Notes", "Tasks"])
    st.caption("Your web data is session-only and may disappear on restart or reconnect. It is not shared with Telegram.")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()
    if st.button("Lock app"):
        st.session_state.authenticated = False
        st.rerun()

if page == "AI Chat":
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    prompt = st.chat_input("Ask your assistant...")
    if prompt:
        if len(prompt) > 6000:
            st.error("Please keep messages under 6000 characters.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        answer = generate_answer(st.session_state.messages)
                    except Exception as exc:
                        logger.exception("Gemini request failed")
                        st.error("Gemini is temporarily unavailable or the request failed. If this persists, check your model access, API quota, and Streamlit logs.")
                        st.caption(f"Error type: {type(exc).__name__}; model: {setting('GEMINI_MODEL', 'gemini-3.1-flash-lite')}")
                    else:
                        st.write(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
elif page == "Notes":
    with st.form("add_note", clear_on_submit=True):
        note = st.text_area("Write a note")
        if st.form_submit_button("Save note") and note.strip():
            st.session_state.notes.append(note.strip())
            st.rerun()
    for i, note in enumerate(reversed(st.session_state.notes), 1):
        st.write(f"**{i}.** {note}")
else:
    with st.form("add_task", clear_on_submit=True):
        title = st.text_input("New task")
        if st.form_submit_button("Add task") and title.strip():
            st.session_state.tasks.append({"title": title.strip(), "done": False})
            st.rerun()
    for i, task in enumerate(st.session_state.tasks):
        task["done"] = st.checkbox(task["title"], value=task["done"], key=f"task_{i}")
