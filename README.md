# 🤖 Telegram Anti-Bot Guard

Ein einfacher Telegram-Bot, der automatisch neue Bots aus einer Gruppe entfernt.

## 🔧 Funktionen

- Überwacht neue Mitglieder einer Telegram-Gruppe.
- Erkennt, ob ein neues Mitglied ein Bot ist.
- Entfernt automatisch neue Bots aus der Gruppe.
- Sendet eine Benachrichtigung über die Entfernung.

## 🛠️ Voraussetzungen

- Python 3.12+
- Virtuelle Umgebung (empfohlen)

## 🚀 Installation

1. Repository klonen oder Dateien speichern:
   ```bash
   git clone https://github.com/dein-user/telegram-bot-kickbots.git
   cd telegram-bot-kickbots
   ```

2. Virtuelle Umgebung erstellen (optional, empfohlen):
   ```bash
   python3 -m venv venv
   source venv/bin/activate       # Windows: venv\Scripts\activate
   ```

3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

4. `.env`-Datei erstellen mit folgendem Inhalt:
   ```env
   BOT_TOKEN=dein_telegram_bot_token
   ```

## ▶️ Bot starten

```bash
python bot.py
```

Wenn alles korrekt ist, erscheint:
```
Bot läuft... Drücke STRG+C zum Beenden.
```

## ⚠️ Wichtig

- Der Bot **muss Adminrechte** in der Telegram-Gruppe besitzen, **inklusive** der Berechtigung **„Mitglieder entfernen“**.
- Der Bot entfernt **nur neue** Bot-Mitglieder, die der Gruppe **nach dem Start** beitreten.
- Bereits vorhandene Bots in der Gruppe werden **nicht entfernt**.
