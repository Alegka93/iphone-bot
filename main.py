from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask, request
import asyncio
import os

TOKEN = os.environ.get("7847656840:AAEoG9zSN9gCmJ25VHzmzqOXtlO7aV14_TI")
ADMIN_ID = 486443841
APP_URL = os.environ.get("APP_URL")

user_data = {}
app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📲 Залишити заявку", "📍 Локація сервісу"], ["💬 Зв’язок з майстром"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привіт! Я бот для запису на ремонт iPhone 📱", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = update.effective_user.id

    if text == "📲 Залишити заявку":
        await update.message.reply_text("Введи модель iPhone:")
        user_data[uid] = {"step": "model"}
    elif text == "📍 Локація сервісу":
        await update.message.reply_text("Наша адреса: 📍 м. Львів, вул. Чупринки 1")
    elif text == "💬 Зв’язок з майстром":
        await update.message.reply_text("Напиши нам у Telegram: @Enforcer1")
    else:
        if uid in user_data:
            step = user_data[uid]["step"]
            if step == "model":
                user_data[uid]["model"] = text
                user_data[uid]["step"] = "problem"
                await update.message.reply_text("Опиши проблему з iPhone:")
            elif step == "problem":
                user_data[uid]["problem"] = text
                user_data[uid]["step"] = "phone"
                await update.message.reply_text("Введи свій номер телефону:")
            elif step == "phone":
                user_data[uid]["phone"] = text
                data = user_data[uid]
                message = (
                    f"📥 Нова заявка від @{update.effective_user.username or 'без username'}\n\n"
                    f"📱 Модель: {data['model']}\n"
                    f"⚠️ Проблема: {data['problem']}\n"
                    f"📞 Телефон: {data['phone']}")
                await context.bot.send_message(chat_id=ADMIN_ID, text=message)
                await update.message.reply_text("✅ Дякуємо! Майстер скоро зв’яжеться з тобою.")
                del user_data[uid]

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    asyncio.run(telegram_app.process_update(update))
    return "ok"

@app.route("/")
def set_webhook():
    telegram_app.bot.set_webhook(url=f"{APP_URL}/webhook/{TOKEN}")
    return "Webhook встановлено"
