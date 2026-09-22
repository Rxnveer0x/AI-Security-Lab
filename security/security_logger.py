from datetime import datetime
from pathlib import Path

LOG_DIR = Path("data/reports")
LOG_FILE = LOG_DIR / "security.log"


def log_security_event(message, status):
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{time} | {status} | {message}\n")