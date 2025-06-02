import os
import asyncio
import random
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, ContextTypes, MessageHandler, CallbackQueryHandler, filters
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
pending_tasks = {}
pending_answers = {}

# Beispiel-Fragen
questions = [
    {"question": "Was ergibt 2 + 2?", "correct": "4", "options": ["3", "4", "5"]},
    {"question": "Welche Farbe hat der Himmel?", "correct": "Blau", "options": ["Grün", "Blau", "Rot"]},
    {"question": "Welcher Tag kommt nach Montag?", "correct": "Dienstag", "options": ["Sonntag", "Dienstag", "Freitag"]},
    {"question": "Wie viele Beine hat eine Katze?", "correct": "4", "options": ["2", "4", "6"]},
    {"question": "Was trinkt eine Kuh?", "correct": "Wasser", "options": ["Milch", "Cola", "Wasser"]},
]

async def welcome_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.new_chat_members is None:
        return

    for member in update.message.new_chat_members:
        if member.is_bot:
            await context.bot.ban_chat_member(update.effective_chat.id, member.id)
            await update.message.reply_text(f"Bot {member.full_name} wurde entfernt.")
        else:
            question = random.choice(questions)
            buttons = [
                InlineKeyboardButton(opt, callback_data=f"answer_{member.id}_{'correct' if opt == question['correct'] else 'wrong'}")
                for opt in question["options"]
            ]
            keyboard = InlineKeyboardMarkup([buttons])
            await update.message.reply_text(
                f"Willkommen {member.full_name}! Bitte beantworte die Frage:\n\n<b>{question['question']}</b>",
                reply_markup=keyboard,
                parse_mode="HTML"
            )

            task = asyncio.create_task(kick_after_timeout(context, update.effective_chat.id, member))
            pending_tasks[member.id] = task

async def kick_after_timeout(context, chat_id, member, timeout=60):
    await asyncio.sleep(timeout)
    if member.id in pending_tasks:
        try:
            await context.bot.ban_chat_member(chat_id, member.id)
            await context.bot.send_message(chat_id, f"{member.full_name} wurde gesperrt – keine richtige Antwort erhalten.")
        except Exception as e:
            print(f"Fehler beim Entfernen von {member.full_name}: {e}")
        finally:
            pending_tasks.pop(member.id, None)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data.startswith(f"answer_{user_id}_"):
        result = data.split("_")[-1]
        task = pending_tasks.pop(user_id, None)

        if result == "correct":
            if task:
                task.cancel()
            await query.edit_message_text("✅ Richtig beantwortet – willkommen in der Gruppe!")
        else:
            await query.edit_message_text("❌ Falsche Antwort – du wurdest entfernt.")
            await context.bot.ban_chat_member(query.message.chat.id, user_id)
    else:
        await query.answer("Das ist nicht für dich.", show_alert=True)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_members))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("Bot läuft... Drücke STRG+C zum Beenden.")
    app.run_polling()
