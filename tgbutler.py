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
    help_text = """Here’s what I can do for you:

/chat <message> — Chat with AI 🤖
/note <text> — Save a quick note 📝
/remind <time> <task> — Set a reminder ⏰
/setmodel <deepseek|openai> — Switch AI model ⚙️
"""
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

# ---------------------- Improved AI Summary Function ----------------------
async def ai_summarize(text: str) -> str:
    summary_prompt = (
        "Summarize the following message in one sentence. "
        "Be concise, objective, and professional.\n"
        f"Message: {text}"
    )
    try:
        summary = await ask_ai(summary_prompt)
        return summary.strip()
    except Exception as e:
        return f"[AI Summary Failed] Raw message:\n{text}"

# ---------------------- /note 笔记 ----------------------
async def note_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    note = " ".join(context.args)
    if not note:
        await update.message.reply_text("Type something to save. I’ll keep it safe 🗂️")
        return
    await update.message.reply_text(f"Got it! I’ve saved your note: “{note}”")




from apscheduler.jobstores.base import JobLookupError

# ---------------------- /remindlist 查看所有提醒 ----------------------
async def remind_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = scheduler.get_jobs()
    if not jobs:
        await update.message.reply_text("🔕 当前没有待执行的提醒。")
        return
    message_lines = []
    for i, job in enumerate(jobs, 1):
        run_time = job.next_run_time.strftime("%Y-%m-%d %H:%M")
        message_lines.append(f"{i}. ⏰ {run_time} - {job.name}")
    await update.message.reply_text("\n".join(message_lines))

# ---------------------- /cancelremind <任务序号> ----------------------
async def cancel_remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = scheduler.get_jobs()
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("用法：/cancelremind <任务编号> （用 /remindlist 查看）")
        return
    index = int(context.args[0]) - 1
    if index < 0 or index >= len(jobs):
        await update.message.reply_text("❌ 提醒编号无效。")
        return
    try:
        jobs[index].remove()
        await update.message.reply_text(f"✅ 已取消提醒：{jobs[index].name}")
    except JobLookupError:
        await update.message.reply_text("⚠️ 无法取消，提醒可能已执行。")



# ---------------------- 自动欢迎新成员 ----------------------
async def welcome_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        name = member.full_name
        welcome_text = (
            f"""Hi {name} 👋\n"
            "I'm *AVECROUGE* — your AI assistant here to help, remind, and chat.\n"
            "Type /help to get started 🧠"""
        )
        await update.message.reply_text(welcome_text, parse_mode="Markdown")


# ---------------------- 群关键词监听 ----------------------
async def keyword_listener(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat = update.effective_chat

    if any(keyword.lower() in text.lower() for keyword in KEYWORDS):
        summary = await ai_summarize(text)
        forward_text = (
            f"📩 *New Message with AI Summary*\n\n"
            f"{chat.title if chat.title else '👤 Private Chat'}\n"
            f"👤 From: `{update.effective_user.full_name}` (`{update.effective_user.id}`)\n\n"
            f"📝 Summary:\n{summary}"
        )
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=forward_text,
            parse_mode="Markdown"
        )

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