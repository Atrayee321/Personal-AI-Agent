# 🤖 Personal AI Agent — AI Chatbot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google Gemini" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Generative_AI-8A2BE2?style=for-the-badge" alt="Generative AI" />
</p>

<p align="center">
  <strong>A simple interactive AI chatbot powered by Google Gemini and built with Python and Streamlit.</strong>
</p>

<p align="center">
  <a href="https://personal-ai-agent-ddckhx3sqrmfdhpknnepkc.streamlit.app/">
    <img src="https://img.shields.io/badge/🚀_Try_Live_Chatbot-Open_App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live Demo" />
  </a>
</p>

---

## 📌 Project Overview

**Personal AI Agent** is a lightweight AI chatbot that allows users to interact with an artificial intelligence assistant through a simple web interface.

The application uses Google's **Gemini API** to understand user prompts and generate conversational responses. It is built using Python and Streamlit, providing an accessible interface for asking questions and exploring AI-powered conversations.

This project demonstrates the integration of a Large Language Model (LLM) into a Python web application.

## ✨ Key Features

- 💬 **Interactive AI Chat:** Communicate with an AI assistant through a chat interface.
- 🧠 **Gemini-Powered Responses:** Generate responses using Google's Gemini model.
- ⚡ **Real-Time Interaction:** Submit prompts and receive AI-generated responses.
- 🌐 **Web-Based Interface:** Access the chatbot through a Streamlit application.
- 🔑 **API Integration:** Connect the application to Google's Gemini API.

## ⚙️ How It Works

The application follows a simple workflow:

```text
       User
        |
        v
   Enter a Prompt
        |
        v
   Streamlit Interface
        |
        v
    Python Backend
        |
        v
     Gemini API
        |
        v
   AI-Generated Response
        |
        v
   Display in Chat Interface
```

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Google Gemini API | AI-powered response generation |
| Streamlit | Interactive web application |
| Google GenAI SDK | Communication with the Gemini API |

## 🚀 Run Locally

Follow these steps to run the chatbot on your computer.

### 1. Clone the repository

```bash
git clone https://github.com/Atrayee321/Personal-AI-Agent.git
```

### 2. Navigate to the project directory

```bash
cd Personal-AI-Agent
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure your Gemini API key

Create a `.streamlit/secrets.toml` file in your project directory and add:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
```

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

**Important:** Never upload your actual API key or `secrets.toml` file to GitHub. Keep your credentials private.

### 6. Run the application

```bash
streamlit run streamlit_app.py
```

Open the local URL displayed in your terminal to start chatting with the AI assistant.

## 🌐 Live Deployment

The chatbot is deployed using **Streamlit Community Cloud**.

<p align="center">
  <a href="https://personal-ai-agent-ddckhx3sqrmfdhpknnepkc.streamlit.app/">
    <img src="https://img.shields.io/badge/Launch_Personal_AI_Chatbot-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Launch Chatbot" />
  </a>
</p>

**Live Application:**  
https://personal-ai-agent-ddckhx3sqrmfdhpknnepkc.streamlit.app/

## 🔐 Security & Limitations

- A valid Google Gemini API key is required.
- API usage is subject to Google's model availability, quotas, and usage limits.
- AI-generated responses may occasionally be inaccurate.
- Chat history is limited to the application's browser session and is not guaranteed to persist after a restart or reconnection.
- The chatbot does not provide Telegram or iMessage integration.
- It does not independently execute tasks, access external accounts, or perform actions on behalf of users.

## 🔮 Future Improvements

Possible enhancements for future versions:

- Persistent conversation history.
- Multiple AI model support.
- Chat export functionality.
- Customizable chatbot personalities.
- Document upload and question answering.
- Improved conversation management.

## 👩‍💻 Author

**Atrayee Chatterjee**

- GitHub: [Atrayee321](https://github.com/Atrayee321)
- LinkedIn: [Connect with me](https://www.linkedin.com/in/atrayee-chatterjee-44a003307/)
- Email: [atrayeetintin@gmail.com](mailto:atrayeetintin@gmail.com)

## 📄 Copyright

Copyright © 2026 Atrayee Chatterjee. All rights reserved for original project code and documentation except where otherwise stated.

Third-party libraries, APIs, and dependencies remain subject to their respective licenses and terms of use.

---

<p align="center">
  <strong>💡 Exploring AI, One Conversation at a Time.</strong>
</p>

<p align="center">
  ⭐ Thanks for visiting this project!
</p>
