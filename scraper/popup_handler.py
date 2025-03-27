# popup_handler.py

def dismiss_facebook_popups(page):
    """
    Versucht, Login- und Cookie-Overlays auf Facebook-Seiten automatisch zu schließen.
    """
    print("[~] Versuche Facebook-Popups zu entfernen ...")

    # Cookie-Banner abfangen (mehrsprachig)
    cookie_texts = [
        "Atmesti nebūtinus slapukus",  # litauisch
        "Nur notwendige Cookies erlauben",
        "Nur essentielle Cookies erlauben",
        "Nur erforderliche Cookies zulassen",
        "Alle Cookies ablehnen",
        "Nur notwendige Cookies auswählen",
    ]

    for text in cookie_texts:
        try:
            page.locator(f"text={text}").click(timeout=3000)
            print(f"[+] Cookie-Banner geschlossen: '{text}'")
            break
        except:
            continue

    # Login-Overlay (Blende / Close-Button)
    try:
        close_button = page.locator("div[aria-label='Schließen'], div[aria-label='Close']")
        if close_button:
            close_button.first.click(timeout=3000)
            print("[+] Facebook-Login-Overlay geschlossen")
    except:
        print("[~] Kein Login-Overlay erkannt")

    print("[~] Popup-Handling abgeschlossen.")
