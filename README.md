🤖 Telegram Anti-Bot Guard

Beschreibung

Dieser Bot ist ein intelligenter Wächter für deine Telegram-Gruppen. Er entfernt nicht nur bekannte Bots, sondern stellt auch allen neuen Mitgliedern eine dynamische Kontrollfrage, um hochentwickelte Spam- und User-Bots abzuwehren, die nicht als offizielle Bot-Konten gekennzeichnet sind.

Dadurch wird sichergestellt, dass nur echte Menschen der Gruppe beitreten können, während der Chat sauber und spamfrei bleibt.

Features

    Sofortige Bot-Entfernung: Erkennt und bannt offizielle Telegram-Bots beim Beitritt.

    Dynamische Mensch-Verifizierung: Stellt neuen Mitgliedern eine simple, aber zufällig generierte Mathe-Kontrollfrage, um automatisierte User-Bots zu blockieren.

    Sichere Überprüfung: Die Validierung ist so gebaut, dass Bots die richtige Antwort nicht einfach aus den Button-Daten auslesen können.

    Automatisierte Chat-Bereinigung: Die Verifizierungs-Nachricht wird nach Erfolg, Misserfolg oder Zeitablauf automatisch gelöscht, um den Chatverlauf sauber zu halten.

    Keine Beeinflussung bestehender Mitglieder.

🛠️ Voraussetzungen

    Python 3.12+

    Eine aktive Internetverbindung und ein Telegram Bot Token.

🚀 Installation

    Repository klonen oder die Quellcode-Dateien herunterladen:
    Bash

git clone https://github.com/dein-user/telegram-bot-kickbots.git
cd telegram-bot-kickbots

Eine virtuelle Umgebung erstellen und aktivieren (dringend empfohlen):
Bash

# Für macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Für Windows
python -m venv venv
venv\Scripts\activate

Die notwendigen Abhängigkeiten aus der requirements.txt installieren:
Bash

pip install -r requirements.txt

Eine .env-Datei im Hauptverzeichnis des Projekts erstellen und deinen Bot-Token eintragen:
Code-Snippet

    BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123456789

▶️ Bot starten

Führe das Hauptskript aus (angenommen, es heißt bot.py):
Bash

python bot.py

Wenn alles korrekt eingerichtet ist, siehst du die Bestätigung im Terminal:

Bot läuft... Drücke STRG+C zum Beenden.

⚠️ Wichtig: Benötigte Adminrechte

Damit der Bot korrekt funktioniert, muss er Administratorrechte in der Telegram-Gruppe haben. Er benötigt mindestens die folgenden Berechtigungen:

    Mitglieder bannen: Um Bots und fehlgeschlagene Verifizierungen zu entfernen.

    Nachrichten löschen: Um die Verifizierungs-Fragen nach der Interaktion zu bereinigen.

Der Bot agiert nur bei neuen Mitgliedern, die der Gruppe beitreten, während er online ist. Bereits vorhandene Mitglieder werden nicht überprüft oder entfernt.

Lizenz

Dieses Projekt steht unter der MIT-Lizenz – siehe die LICENSE-Datei für weitere Informationen.
