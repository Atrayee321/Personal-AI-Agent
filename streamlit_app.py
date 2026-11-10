"""Streamlit web interface for the Personal AI Agent.

The web interface intentionally uses session-scoped notes, tasks and chat.
They may disappear after inactivity/restart; Telegram's SQLite database is separate.
"""
import hmac
import logging
import os
import time

import streamlit as st

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


def authenticate():
    password = setting("APP_PASSWORD")
    if not password:
        st.error("APP_PASSWORD is not configured. Add it in Streamlit Cloud → App settings → Secrets.")
        st.stop()
    if st.session_state.get("authenticated"):
        return
    st.title("🔐 Personal AI Agent")
    with st.form("login"):
        attempt = st.text_input("App password", type="password")
        submitted = st.form_submit_button("Unlock")
    if submitted:
        if hmac.compare_digest(attempt, password):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()


SYSTEM_PROMPT = (
    "You are a helpful personal assistant. Answer clearly and concisely unless "
    "the user asks for detail. Never claim to perform actions you cannot perform."
)


def stream_reply(messages):
    """Yield response chunks as the provider generates them."""
    provider = setting("AI_PROVIDER", "gemini").lower().strip()
    model = setting("AI_MODEL", "gemini-3.1-flash-lite")
    recent = messages[-6:]
    if provider == "gemini":
        from google import genai
        from google.genai import types

        key = setting("GEMINI_API_KEY")
        if not key:
            raise ValueError("GEMINI_API_KEY is missing from Streamlit Secrets.")
        client = genai.Client(api_key=key)
        transcript = "\n\n".join(
            ("User" if msg["role"] == "user" else "Assistant") + ": " + msg["content"]
            for msg in recent
        )
        stream = client.models.generate_content_stream(
            model=model,
            contents=SYSTEM_PROMPT + "\n\n" + transcript,
            config=types.GenerateContentConfig(
                max_output_tokens=512,
                temperature=0.5,
            ),
        )
        for chunk in stream:
            if chunk.text:
                yield chunk.text
        return
    if provider == "openai":
        from openai import OpenAI

        key = setting("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY is missing from Streamlit Secrets.")
        client = OpenAI(api_key=key)
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + recent,
            max_tokens=512,
            stream=True,
        )
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content
        return
    raise ValueError("AI_PROVIDER must be 'gemini' or 'openai'.")


authenticate()
st.title("🤖 Personal AI Agent")
st.caption("Private web dashboard • AI chat • Notes • Tasks")

for name, default in (("messages", []), ("notes", []), ("tasks", [])):
    if name not in st.session_state:
        st.session_state[name] = default

with st.sidebar:
    st.subheader("Your workspace")
    page = st.radio("Navigate", ["AI Chat", "Notes", "Tasks"])
    st.info("Chat, notes and tasks are stored only in this browser session and may be lost after app restart or inactivity.")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()
    if st.button("Lock app"):
        st.session_state.authenticated = False
        st.rerun()

if page == "AI Chat":
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    question = st.chat_input("Ask your AI assistant...")
    if question:
        if len(question) > 6000:
            st.error("Please keep messages under 6000 characters.")
        else:
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.write(question)
            with st.chat_message("assistant"):
                started = time.perf_counter()
                reply = ""
                try:
                    reply = st.write_stream(stream_reply(st.session_state.messages))
                except Exception as exc:
                    logger.exception("AI provider request failed")
                    st.error("AI request failed. Check Streamlit Cloud → Manage app → Logs for the error code. Never share API keys.")
                    st.caption(f"Error type: {type(exc).__name__}. Provider: {setting('AI_PROVIDER', 'gemini')}. Model: {setting('AI_MODEL', 'gemini-3.1-flash-lite')}.")
                if reply:
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.caption(f"Response time: {time.perf_counter() - started:.1f} seconds")

elif page == "Notes":
    with st.form("note_form", clear_on_submit=True):
        note = st.text_area("Write a note")
        if st.form_submit_button("Save note") and note.strip():
            st.session_state.notes.append(note.strip())
            st.rerun()
    for index, note in enumerate(reversed(st.session_state.notes), 1):
        st.write(f"**{index}.** {note}")

else:
    with st.form("task_form", clear_on_submit=True):
        task = st.text_input("New task")
        if st.form_submit_button("Add task") and task.strip():
            st.session_state.tasks.append({"title": task.strip(), "done": False})
            st.rerun()
    for index, task in enumerate(st.session_state.tasks):
        checked = st.checkbox(task["title"], value=task["done"], key=f"task_{index}")
        task["done"] = checked
