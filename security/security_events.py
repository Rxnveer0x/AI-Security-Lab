from pathlib import Path


LOG_FILE = Path("data/reports/security.log")


def get_recent_events(limit=20):
    """
    Read the most recent security events from the security log.
    """

    if not LOG_FILE.exists():
        return []

    events = []

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines[-limit:]:
        line = line.strip()

        if not line:
            continue

        parts = line.split(" | ", 2)

        if len(parts) != 3:
            continue

        timestamp, event_type, message = parts

        events.append({
            "timestamp": timestamp,
            "event": event_type,
            "message": message
        })

    return events