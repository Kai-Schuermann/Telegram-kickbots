# 🤖 Telegram Anti-Bot Guard

## Beschreibung

Dieser Bot entfernt automatisch neu hinzugefügte Bots aus Telegram-Gruppen.  
Er erkennt sowohl offizielle Bots (Telegram-Botkonten) als auch automatisierte Benutzerkonten, die sich wie Bots verhalten können, und blockiert diese, sobald sie der Gruppe beitreten.

## Features

- Entfernt neue Bots automatisch aus der Gruppe.
- Blockiert auch automatisierte Benutzerkonten, die nicht als offizielle Bots markiert sind.
- Nutzt eine einfache Button-Bestätigung, damit menschliche Nutzer nicht fälschlicherweise entfernt werden.
- Keine Löschung oder Beeinflussung bereits bestehender Gruppenmitglieder beim Neustart.

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


## Lizenz

Dieses Projekt steht unter der MIT-Lizenz – siehe [LICENSE](./LICENSE) für weitere Informationen.
