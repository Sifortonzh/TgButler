
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

## 📎 Screenshots



---

## 💡 Inspiration

Slack’s tone. Your personal AI secretary. A hands-off message monitor.  
TgButler is designed to **“do things you don’t want to do manually”** — but with style.

---

## 📄 License

MIT License © 2025 Avecrouge
