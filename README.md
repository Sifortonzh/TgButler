
# 🛡️ TgButler – Your Telegram AI Assistant

**TgButler** is a personal Telegram bot powered by AI, designed to help you **chat, take notes, set reminders, forward important messages**, and more.  
Built with ✨ `python-telegram-bot`, OpenAI/DeepSeek models, and `apscheduler`.

---

## 🌟 Features

| Command | Description |
|---------|-------------|
| `/start` | Friendly Slack-style onboarding |
| `/help` | Show all available commands |
| `/chat <message>` | Chat with AI (OpenAI or DeepSeek) |
| `/note <text>` | Save quick notes |
| `/remind <time> <text>` | Set reminders (supports `in 10m`, `23:30`, full date) |
| `/remindlist` | View pending reminders |
| `/cancelremind <index>` | Cancel a specific reminder |
| `/setmodel openai|deepseek` | Switch the AI backend |
| `/reply <user_id> <message>` | Send a reply to any forwarded user |
| 🔁 **Passive Features** | |
| ✉️ Message forwarding to bot owner | With AI-generated summary |
| 🔔 Keyword detection in groups | Notifies owner if “Netflix”, “YouTube”, etc. are mentioned |
| 🙋 Auto-welcome | New group members get a friendly welcome message |

---

## 🧠 AI Summary

Every forwarded message includes an **AI-generated summary** (via OpenAI or DeepSeek).  
Prompt used:

```
"Summarize the following message in one sentence. 
Be concise, objective, and professional."
```

---

## ⚙️ Environment Variables

You need to set the following environment variables in your `.env` file or in Railway/Render UI:

```env
BOT_TOKEN=your_botfather_token
OWNER_ID=your_telegram_user_id
OPENAI_API_KEY=sk-xxxxxxx
DEFAULT_MODEL=deepseek   # or "openai"
TZ=Asia/Shanghai
```

---

## 🚀 How to Deploy

### 1. Locally

```bash
pip install -r requirements.txt
python tgbutler.py
```

### 2. Railway / Render (Recommended)

- Connect GitHub repository
- Set environment variables
- **Start Command**: `python tgbutler.py`
- Optional: add `PYTHON_VERSION=3.11.9`

---

### 3. Prevent Railway from Sleeping (UptimeRobot)

By default, Railway will put your service to sleep if there's no incoming HTTP request for 10 minutes.  
To keep your bot alive (especially when using `run_polling()`), add a tiny Flask server:

```python
from flask import Flask
import threading

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return 'TgButler is alive 💡'

def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)

# Start the Flask server in background
threading.Thread(target=run_flask).start()
```

---

## 📎 Screenshots



---

## 💡 Inspiration

Slack’s tone. Your personal AI secretary. A hands-off message monitor.  
TgButler is designed to **“do things you don’t want to do manually”** — but with style.

---

## 📄 License

MIT License © 2025 Avecrouge
