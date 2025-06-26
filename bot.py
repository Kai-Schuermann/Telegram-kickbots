import os
import asyncio
import random
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember
from telegram.ext import (
    ApplicationBuilder, ContextTypes, MessageHandler, CallbackQueryHandler, filters
)
from telegram.error import Forbidden, BadRequest

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Wir speichern hier jetzt die Aufgabe (Task), die Message-ID zum Löschen und die korrekte Antwort
pending_verifications = {}

# NEU: Funktion zum Generieren von dynamischen Mathe-Fragen
def generate_math_question():
    """Generiert eine einfache Additionsfrage und gibt sie mit Optionen zurück."""
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    correct_answer = a + b
    
    # Erstelle falsche Antworten, die sich von der korrekten unterscheiden
    wrong_answers = set()
    while len(wrong_answers) < 2:
        offset = random.randint(-5, 5)
        # Stelle sicher, dass die falsche Antwort nicht 0 ist und nicht der richtigen Antwort entspricht
        if offset != 0 and correct_answer + offset > 0:
            wrong_answers.add(correct_answer + offset)
            
    options = list(wrong_answers) + [correct_answer]
    random.shuffle(options)
    
    return {
        "question": f"Um zu beweisen, dass du ein Mensch bist: Was ergibt {a} + {b}?",
        "correct": str(correct_answer),
        "options": [str(o) for o in options]
    }

async def welcome_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.new_chat_members is None:
        return

    for member in update.message.new_chat_members:
        # Bestehende Logik für deklarierte Bots ist gut, wir behalten sie bei.
        if member.is_bot:
            try:
                await context.bot.ban_chat_member(update.effective_chat.id, member.id)
                await update.message.reply_text(f"Bot {member.full_name} wurde entfernt.")
            except (Forbidden, BadRequest) as e:
                print(f"Konnte Bot {member.full_name} nicht entfernen (evtl. keine Rechte): {e}")
            continue # Springe zum nächsten Mitglied

        # NEUE Logik für menschliche Benutzer
        question_data = generate_math_question()
        
        # ÜBERARBEITET: Die callback_data enthält jetzt nur noch die gewählte Antwort, nicht das Ergebnis.
        buttons = [
            InlineKeyboardButton(
                opt,
                callback_data=f"verify_{member.id}_{opt}"
            )
            for opt in question_data["options"]
        ]
        keyboard = InlineKeyboardMarkup([buttons])
        
        sent_message = await update.message.reply_text(
            f"Willkommen {member.full_name}!\n\n<b>{question_data['question']}</b>",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

        # ÜBERARBEITET: Wir erstellen eine Timeout-Task und speichern alle nötigen Infos
        timeout_task = asyncio.create_task(
            kick_after_timeout(context, update.effective_chat.id, member.id, sent_message.message_id)
        )
        
        pending_verifications[member.id] = {
            "task": timeout_task,
            "message_id": sent_message.message_id,
            "correct_answer": question_data["correct"],
            "full_name": member.full_name
        }

async def kick_after_timeout(context, chat_id, user_id, message_id, timeout=60):
    """Kickt den User nach Ablauf der Zeit, wenn er noch in der Verifizierungs-Liste ist."""
    await asyncio.sleep(timeout)
    
    if user_id in pending_verifications:
        user_info = pending_verifications.pop(user_id)
        try:
            await context.bot.ban_chat_member(chat_id, user_id)
            # NEU: Lösche die ursprüngliche Frage und sende eine Kick-Nachricht
            await context.bot.delete_message(chat_id, message_id)
            await context.bot.send_message(chat_id, f"{user_info['full_name']} hat die Verifizierung nicht bestanden und wurde entfernt.")
        except (Forbidden, BadRequest) as e:
            print(f"Fehler beim Entfernen von {user_info['full_name']} nach Timeout: {e}")
        # Der Task muss nicht mehr gecancelt werden, da er von selbst endet.
        
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # Wichtig: Immer dem Client antworten, dass der Klick empfangen wurde.

    try:
        _, user_id_str, chosen_answer = query.data.split("_", 2)
        user_id = int(user_id_str)
    except ValueError:
        await query.answer("Ungültige Callback-Daten.", show_alert=True)
        return

    # Prüfen, ob der klickende Benutzer der ist, für den die Frage bestimmt war
    if query.from_user.id != user_id:
        await query.answer("Diese Verifizierung ist nicht für dich bestimmt.", show_alert=True)
        return

    # Prüfen, ob eine Verifizierung für diesen Benutzer überhaupt aussteht
    if user_id not in pending_verifications:
        # Nachricht wurde eventuell schon durch Timeout oder eine andere Aktion bearbeitet
        await query.edit_message_text("Diese Anfrage ist bereits abgelaufen.")
        return

    # Alle Daten aus dem Dictionary holen und es direkt leeren, um Race Conditions zu vermeiden
    verification_data = pending_verifications.pop(user_id)
    verification_data["task"].cancel() # Timeout-Task abbrechen!

    correct_answer = verification_data["correct_answer"]
    message_id = verification_data["message_id"]

    if chosen_answer == correct_answer:
        # Erfolg: Nachricht bearbeiten und nach kurzer Zeit löschen
        await query.edit_message_text(f"✅ Danke, {query.from_user.full_name}! Willkommen in der Gruppe.")
        await asyncio.sleep(5) # Nachricht 5 Sekunden anzeigen
        await context.bot.delete_message(query.message.chat.id, message_id)
    else:
        # Falsche Antwort: Benutzer entfernen und Nachricht löschen
        try:
            await context.bot.ban_chat_member(query.message.chat.id, user_id)
            await query.edit_message_text(f"❌ Falsche Antwort. Du wurdest aus der Gruppe entfernt.")
            await asyncio.sleep(5) # Nachricht 5 Sekunden anzeigen
            await context.bot.delete_message(query.message.chat.id, message_id)
        except (Forbidden, BadRequest) as e:
            print(f"Konnte Benutzer {query.from_user.full_name} nach falscher Antwort nicht entfernen: {e}")
            await query.edit_message_text("Konnte dich aufgrund eines Fehlers nicht entfernen.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_members))
    app.add_handler(CallbackQueryHandler(button_callback, pattern=r"^verify_")) # Pattern zur Leistungsoptimierung
    print("Bot läuft... Drücke STRG+C zum Beenden.")
    app.run_polling()