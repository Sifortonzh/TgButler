
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
| `/remind <time> <task>` | Set reminders (`in 10m`, `23:30`, full date) |
| `/remindlist` | View all active reminders |
| `/cancelremind <index>` | Cancel a specific reminder |
| `/setmodel openai|deepseek` | Switch the AI backend |
| `/reply <user_id> <message>` | Send a reply to any forwarded user |
| 🔁 **Passive Features** | |
| ✉️ Message forwarding to bot owner | With AI-generated summary |
| 🧠 AI Summary | Auto summary via English prompt |
| 🔔 Keyword detection in groups | Alerts owner if keywords like “Netflix” appear |
| 🙋 Auto-welcome | Friendly message for new group members |
| ♻️ Railway uptime keep-alive | Optional Flask route for UptimeRobot |

---

## 🧠 AI Summary

All forwarded messages include an AI summary using OpenAI/DeepSeek.  
Prompt used:

```
Summarize the following message in one sentence.
Be concise, objective, and professional.
```

---

## ⚙️ Environment Variables

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

### 2. Railway / Render

- Connect your GitHub repo
- Add required environment variables
- **Start Command**: `python tgbutler.py`
- Add: `PYTHON_VERSION = 3.11.9`

---

### ♻️ Prevent Railway from Sleeping (UptimeRobot)

Add this Flask route:

```python
from flask import Flask
import threading

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return 'TgButler is alive 💡'

def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)

# Start the server
threading.Thread(target=run_flask).start()
```

Register the resulting Railway URL (e.g. `https://yourapp.up.railway.app/`)  
with [UptimeRobot](https://uptimerobot.com) to ping it every 5 minutes.

---

## 📄 License

MIT License © 2025 Avecrouge
