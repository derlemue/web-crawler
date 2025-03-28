import os
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

from database import init_db, save_snapshot
from telegram_alert import send_telegram_image
from popup_handler import dismiss_facebook_popups
from urls import watchlist_urls

load_dotenv()

DATA_DIR = Path("data/screenshots")
DATA_DIR.mkdir(parents=True, exist_ok=True)
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
TELEGRAM_ENABLED = os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID")

def is_facebook(url: str) -> bool:
    return "facebook.com" in url

def safe_filename(name: str) -> str:
    return name.replace(" ", "_").replace(".", "").replace("/", "_")

def find_previous_screenshot(name: str):
    safe_name = safe_filename(name)
    files = sorted(DATA_DIR.glob(f"{safe_name}_*.png"), reverse=True)
    if len(files) >= 2:
        return files[1]
    return None

def images_are_significantly_different(img1, img2, threshold=60):
    diff = ImageChops.difference(img1, img2)
    stat = ImageStat.Stat(diff)
    mean_diff = sum(stat.mean) / len(stat.mean)
    return mean_diff > threshold

def capture_page(name: str, url: str):
    print(f"[+] Capturing: {name} -> {url}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 2160})
        page = context.new_page()

        try:
            page.goto(url, timeout=120000)
            time.sleep(5)
            page.wait_for_load_state("networkidle", timeout=15000)

            dismiss_facebook_popups(page)

            if is_facebook(url):
                for text in ["Akzeptieren", "Jetzt nicht"]:
                    try:
                        page.click(f"text={text}", timeout=3000)
                    except:
                        pass

            # Scrollen für dynamischen Content
            for _ in range(2):
                page.evaluate("window.scrollBy(0, 1080)")
                time.sleep(3)

            # Screenshot speichern
            timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
            safe_name = safe_filename(name)
            screenshot_path = DATA_DIR / f"{safe_name}_{timestamp}.png"
            page.screenshot(path=screenshot_path, clip={"x": 0, "y": 0, "width": 1920, "height": 2160})

            # Vergleich mit vorherigem Screenshot
            last_path = find_previous_screenshot(name)
            changed = True
            if last_path and last_path.exists():
                try:
                    img1 = Image.open(screenshot_path)
                    img2 = Image.open(last_path)
                    diff = ImageChops.difference(img1, img2)
                    changed = diff.getbbox() is not None
                except Exception as e:
                    print(f"[!] Bildvergleich fehlgeschlagen: {e}")
                    changed = True

            if changed:
                save_snapshot(name, url, timestamp, str(screenshot_path))
                if TELEGRAM_ENABLED:
                    send_telegram_image(
                        caption=f"📸 Änderung bei: {name}\n{url}\n⏱️ {timestamp}",
                        image_path=screenshot_path
                    )
                else:
                    print(f"[!] Telegram-Konfiguration fehlt.")
            else:
                print(f"[i] Keine Änderung bei {name}, Screenshot verworfen.")
                screenshot_path.unlink(missing_ok=True)

        except Exception as e:
            print(f"[❌] Fehler bei {url}: {e}")
        finally:
            context.close()
            browser.close()

def main():
    init_db()
    for name, url in watchlist_urls.items():
        capture_page(name, url)

if __name__ == "__main__":
    main()
