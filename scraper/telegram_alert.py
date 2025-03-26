import os
import requests

def send_telegram_alert(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("[!] Telegram-Konfiguration fehlt.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print("[!] Telegram-Fehler:", response.text)
    except Exception as e:
        print("[!] Telegram-Ausnahme:", str(e))

def send_telegram_image(caption, image_path):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("[!] Telegram-Konfiguration fehlt.")
        return

    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    with open(image_path, "rb") as image:
        data = {
            "chat_id": chat_id,
            "caption": caption
        }
        files = {
            "photo": image
        }
        try:
            response = requests.post(url, data=data, files=files)
            if response.status_code != 200:
                print("[!] Telegram-Foto-Fehler:", response.text)
        except Exception as e:
            print("[!] Telegram-Upload fehlgeschlagen:", str(e))
