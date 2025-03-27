from playwright.sync_api import sync_playwright
from datetime import datetime
from database import init_db, save_snapshot
from urls import watchlist_urls
from telegram_alert import send_telegram_image
from popup_handler import dismiss_facebook_popups
from PIL import ImageChops, Image
import os
import time

def is_facebook(url):
    return "facebook.com" in url

def find_previous_screenshot(name):
    folder = "data/screenshots"
    safe_name = name.replace(" ", "_").replace(".", "")
    candidates = sorted([
        f for f in os.listdir(folder) if f.startswith(safe_name)
    ], reverse=True)
    if len(candidates) >= 2:
        return os.path.join(folder, candidates[1])
    return None

def capture_page(name, url):
    print(f"[+] Capturing: {name} -> {url}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        try:
            page.goto(url, timeout=60000)
            time.sleep(5)
            dismiss_facebook_popups(page)

            if is_facebook(url):
                try:
                    page.click("text=Akzeptieren", timeout=5000)
                except:
                    pass
                try:
                    page.click("text=Jetzt nicht", timeout=5000)
                except:
                    pass

            # Scroll zwei Seiten
            page.evaluate("window.scrollBy(0, 1080)")
            time.sleep(4)
            page.evaluate("window.scrollBy(0, 1080)")
            time.sleep(4)

            # Screenshot speichern
            timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
            safe_name = name.replace(" ", "_").replace(".", "")
            screenshot_path = f"data/screenshots/{safe_name}_{timestamp}.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            page.screenshot(path=screenshot_path, full_page=True)

            # Vergleich mit vorherigem Screenshot
            last_path = find_previous_screenshot(name)
            changed = True
            if last_path:
                try:
                    img1 = Image.open(screenshot_path)
                    img2 = Image.open(last_path)
                    diff = ImageChops.difference(img1, img2)
                    changed = diff.getbbox() is not None
                except Exception as e:
                    print(f"[!] Bildvergleich fehlgeschlagen: {e}")
                    changed = True  # sicherheitshalber Alert

            if changed:
                save_snapshot(name, url, timestamp, screenshot_path)
                send_telegram_image(
                    caption=f"📸 Änderung bei: {name}\n{url}\n⏱️ {timestamp}",
                    image_path=screenshot_path
                )
            else:
                print(f"[i] Keine Änderung bei {name}")

        except Exception as e:
            print(f"[!] Fehler bei {url}: {e}")
        finally:
            context.close()
            browser.close()

def main():
    init_db()
    for name, url in watchlist_urls.items():
        capture_page(name, url)

if __name__ == "__main__":
    main()
