from pathlib import Path


LOG_FILE = Path("data/reports/security.log")


def get_recent_events(limit=20):
    """
    Read the latest security events from security.log
    and convert them into structured event objects.
    """

    if not LOG_FILE.exists():
        return []

    with open(
        LOG_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        lines = [
            line.strip()
            for line in file
            if line.strip()
        ]

    # Get the newest events
    lines = lines[-limit:]

    events = []

    for line in lines:

        parts = line.split(" | ")

        if len(parts) < 3:
            continue

        timestamp = parts[0]
        event_type = parts[1]
        message = parts[2]

        event = {
            "timestamp": timestamp,
            "event": event_type,
            "message": message
        }

        # ----------------------------------------------------
        # Read additional fields
        # ----------------------------------------------------

        for part in parts[3:]:

            if part.startswith("Risk Level:"):

                risk_level = part.replace(
                    "Risk Level:",
                    "",
                    1
                ).strip()

                event["risk_level"] = risk_level

            elif part.startswith("Metadata:"):

                metadata_text = part.replace(
                    "Metadata:",
                    "",
                    1
                ).strip()

                metadata = {}

                for item in metadata_text.split(","):

                    item = item.strip()

                    if "=" not in item:
                        continue

                    key, value = item.split(
                        "=",
                        1
                    )

                    metadata[key.strip()] = value.strip()

                event["metadata"] = metadata

        events.append(event)

    return events