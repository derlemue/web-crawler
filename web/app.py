from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
import bcrypt
from dotenv import load_dotenv
from database import get_latest_snapshots, get_history_for
import subprocess

app = Flask(__name__)
app.secret_key = os.urandom(24)

load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD_HASH = os.getenv("PASSWORD_HASH").encode()  # Wichtig: encode!

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        entered_pw = request.form["password"]
        valid_pw = bcrypt.checkpw(entered_pw.encode(), PASSWORD_HASH)

        print(f"[DEBUG] Login-Versuch mit: {entered_pw}")
        print(f"[DEBUG] Passwort korrekt? {valid_pw}")

        if request.form["username"] == USERNAME and valid_pw:
            session["user"] = USERNAME
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Falscher Login")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    snapshots = get_latest_snapshots()
    msg = session.pop("run_result", None)
    telegram_ok = bool(os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"))
    return render_template("index.html", snapshots=snapshots, telegram_ok=telegram_ok, run_result=msg)

@app.route("/history/<name>")
def history(name):
    if "user" not in session:
        return redirect(url_for("login"))
    history = get_history_for(name)
    return render_template("history.html", name=name, history=history)

@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)

@app.route("/data/<path:path>")
def send_data(path):
    return send_from_directory("data", path)

@app.route("/run")
def run_scraper():
    if "user" not in session:
        return redirect(url_for("login"))

    try:
        result = subprocess.run(
            ["python3", "run_async.py"],
            cwd="/app",
            capture_output=True,
            text=True,
            timeout=1200
        )
        session["run_result"] = f"⏳ Scraper wurde im Hintergrund gestartet."
    except Exception as e:
        session["run_result"] = f"❌ Fehler beim Start des Scrapers:\n{e}"

    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/test-telegram")
def test_telegram():
    if "user" not in session:
        return redirect(url_for("login"))

    from telegram_alert import send_telegram_alert, send_telegram_image

    try:
        test_text = "🔔 Test-Alarm vom h4ck3n-watchdog"
        send_telegram_alert(test_text)

        test_img = "data/screenshots/test.jpg"
        if os.path.exists(test_img):
            send_telegram_image("🖼️ Beispielbild", test_img)

        session["run_result"] = "✅ Test-Telegram-Alarm wurde gesendet."
    except Exception as e:
        session["run_result"] = f"❌ Telegram-Test fehlgeschlagen:\n{e}"

    return redirect(url_for("dashboard"))

@app.route("/logs")
def show_logs():
    if "user" not in session:
        return redirect(url_for("login"))

    log_dir = "data/logs"
    logs = []
    selected = request.args.get("file")

    try:
        logs = sorted([
            f for f in os.listdir(log_dir) if f.endswith(".log")
        ], reverse=True)
    except Exception as e:
        logs = [f"[Fehler beim Lesen: {e}]"]

    content = ""
    if selected:
        try:
            with open(os.path.join(log_dir, selected), "r") as f:
                content = f.read()
        except Exception as e:
            content = f"[Fehler beim Öffnen: {e}]"

    return render_template("logs.html", logs=logs, content=content, selected=selected)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
