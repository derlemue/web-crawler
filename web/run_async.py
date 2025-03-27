import subprocess
import datetime
import os

LOG_DIR = "data/logs"
os.makedirs(LOG_DIR, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logfile = os.path.join(LOG_DIR, f"scraper_{timestamp}.log")

try:
    container_id = subprocess.check_output(
        ["docker", "ps", "-qf", "name=_scraper"],
        text=True
    ).strip()

    if not container_id:
        with open(logfile, "w") as f:
            f.write("[!] Kein laufender Scraper-Container gefunden.\n")
    else:
        with open(logfile, "w") as f:
            f.write(f"[+] Starte Scraper im Container {container_id} ({timestamp})\n\n")
            subprocess.Popen(
                ["docker", "exec", container_id, "python", "main.py"],
                stdout=f,
                stderr=subprocess.STDOUT
            )

except Exception as e:
    with open(logfile, "w") as f:
        f.write(f"[!] Ausnahme beim Start: {e}\n")
