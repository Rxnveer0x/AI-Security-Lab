from datetime import datetime
from pathlib import Path


LOG_DIR = Path("data/reports")
LOG_FILE = LOG_DIR / "security.log"


def log_security_event(message, status, risk_level=None, metadata=None):
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        parts = [
            time,
            status,
            message
        ]

        if risk_level:
            parts.append(f"Risk Level: {risk_level}")

        if metadata:
            metadata_text = ", ".join(
                f"{key}={value}"
                for key, value in metadata.items()
            )
            parts.append(f"Metadata: {metadata_text}")

        file.write(" | ".join(parts) + "\n")