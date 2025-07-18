import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ---------------------- 配置区域 ----------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))  # 必填
MODEL = os.getenv("DEFAULT_MODEL", "deepseek")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
_current_model = MODEL

# 关键词列表（群监听）
KEYWORDS = ["合租", "上车", "Netflix", "YouTube", "Spotify", "MAX"]

# ---------------------- 日志设置 ----------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ---------------------- /start /help ----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi there 👋 I'm TgButler, your personal assistant bot. Use /help to see what I can do.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Here’s what I can do for you:

"
        "/chat <message> — Chat with AI 🤖
"
        "/note <text> — Save a quick note 📝
"
        "/remind <time> <task> — Set a reminder ⏰
"
        "/setmodel <deepseek|openai> — Switch AI model ⚙️
"
    )
    await update.message.reply_text(help_text)

# ---------------------- /chat 聊天 ----------------------
async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = " ".join(context.args)
    if not user_input:
        await update.message.reply_text("Just say something, and I’ll reply! 💬")
        return
    reply = await ask_ai(user_input)
    await update.message.reply_text(reply)

async def ask_ai(prompt: str) -> str:
    if _current_model == "openai":
        return f"[OpenAI] Answer: {prompt}"
    elif _current_model == "deepseek":
        return f"[Deepseek] Response: {prompt}"
    return "Hmm, I’m not sure which AI model I’m using 🤔"

# ---------------------- /setmodel 模型切换 ----------------------
async def set_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global _current_model
    if update.effective_user.id != OWNER_ID:
        return
    if not context.args:
        await update.message.reply_text("Please specify a model: openai or deepseek.")
        return
    model = context.args[0].lower()
    if model in ["openai", "deepseek"]:
        _current_model = model
        await update.message.reply_text(f"Sure! I’ve switched to `{model}` mode 🤖")
    else:
        await update.message.reply_text("I only support `openai` and `deepseek` for now.")

# ---------------------- /note 笔记 ----------------------
async def note_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    note = " ".join(context.args)
    if not note:
        await update.message.reply_text("Type something to save. I’ll keep it safe 🗂️")
        return
    await update.message.reply_text(f"Got it! I’ve saved your note: “{note}”")

# ---------------------- /remind 提醒（占位） ----------------------
async def remind_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏰ Reminder system coming soon. I’m still learning how to set timers.")

# ---------------------- 群关键词监听 ----------------------
async def keyword_listener(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if any(keyword.lower() in text.lower() for keyword in KEYWORDS):
        await context.bot.send_message(chat_id=OWNER_ID, text=f"🔔 Keyword alert in group:

{text}")

# ---------------------- 启动入口 ----------------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("chat", chat_handler))
    app.add_handler(CommandHandler("note", note_handler))
    app.add_handler(CommandHandler("remind", remind_handler))
    app.add_handler(CommandHandler("setmodel", set_model))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, keyword_listener))

    app.run_polling()