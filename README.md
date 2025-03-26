# 🐾 h4ck3n-watchdog

Ein automatisierter Screenshot-Scraper zur Überwachung rechtsextremer Webseiten und Social-Media-Profile – inklusive Web-Interface, Datenbank und Screenshot-Historie.

---

## ⚙️ Features

- Unterstützung von **Facebook**, **Instagram**, **Webseiten**
- Schließt automatisch das Login-Popup bei Facebook
- Scrollt 2x die Seite herunter (1920x2160)
- Speichert Screenshots mit Timestamp
- **SQLite-Datenbank** mit Screenshot-Metadaten
- Webinterface auf **Port 5000** mit Login
- Pro Seite: Screenshot-Historie einsehbar
- Automatischer Cronjob alle **60 Minuten**

---

## 🚀 Setup (Docker)

1. **Repo klonen**  
   ```bash
   git clone <lokal kopieren oder struktur übernehmen>
   cd h4ck3n-watchdog
