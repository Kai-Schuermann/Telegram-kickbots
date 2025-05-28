import os
import asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, ContextTypes, MessageHandler, CallbackQueryHandler, filters
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Aufgaben-Tracking pro User
pending_tasks = {}

async def welcome_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.new_chat_members is None:
        return

    for member in update.message.new_chat_members:
        if member.is_bot:
            await context.bot.ban_chat_member(update.effective_chat.id, member.id)
            await update.message.reply_text(f"Bot {member.full_name} wurde entfernt.")
        else:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Ich bin kein Bot", callback_data=f"verify_{member.id}")]
            ])
            await update.message.reply_text(
                f"Willkommen {member.full_name}! Bitte bestätige, dass du kein Bot bist:",
                reply_markup=keyboard
            )

            # Starte Timeout-Task
            task = asyncio.create_task(kick_after_timeout(context, update.effective_chat.id, member))
            pending_tasks[member.id] = task

async def kick_after_timeout(context, chat_id, member, timeout=60):
    await asyncio.sleep(timeout)
    if member.id in pending_tasks:
        try:
            await context.bot.ban_chat_member(chat_id, member.id)
            await context.bot.send_message(chat_id, f"{member.full_name} wurde entfernt – keine Bestätigung erhalten.")
        except Exception as e:
            print(f"Fehler beim Entfernen von {member.full_name}: {e}")
        finally:
            pending_tasks.pop(member.id, None)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if data == f"verify_{user_id}":
        task = pending_tasks.pop(user_id, None)
        if task:
            task.cancel()
        await query.edit_message_text("Danke für die Bestätigung! Du bleibst in der Gruppe.")
    else:
        await query.answer("Das ist nicht für dich.", show_alert=True)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_members))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("Bot läuft... Drücke STRG+C zum Beenden.")
    app.run_polling()
