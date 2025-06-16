from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from keep_alive import keep_alive
import os

TOKEN = os.getenv("BOT_TOKEN")  # ✅ БЕЗ ВСТАВКИ ВРУЧНУ — з Render ENV

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я працюю через Render і Flask Webhook! 🚀")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

# 🔗 Піднімаємо Flask-сервер
keep_alive()

# 🟢 Запускаємо бота
app.run_webhook(
    listen="0.0.0.0",
    port=int(os.environ.get("PORT", 5000)),
    url_path=TOKEN,
    webhook_url=f"https://{os.environ['RENDER_EXTERNAL_URL'].strip('/')}/{TOKEN}"
)
