from pathlib import Path
from datetime import datetime

from security.security_events import get_recent_events


REPORT_DIR = Path("data/reports")
REPORT_FILE = REPORT_DIR / "security_report.txt"


def generate_security_report():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    events = get_recent_events(100)

    total_events = len(events)

    event_counts = {}

    for event in events:
        event_type = event["event"]

        event_counts[event_type] = (
            event_counts.get(event_type, 0) + 1
        )

    report = []

    report.append("=" * 60)
    report.append("AI SECURITY LAB - SECURITY REPORT")
    report.append("=" * 60)
    report.append("")

    report.append(
        f"Generated: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    report.append("")

    report.append("SUMMARY")
    report.append("-" * 60)
    report.append(f"Total Security Events: {total_events}")
    report.append("")

    report.append("EVENT COUNTS")
    report.append("-" * 60)

    if event_counts:
        for event_type, count in sorted(event_counts.items()):
            report.append(f"{event_type}: {count}")
    else:
        report.append("No security events recorded.")

    report.append("")

    report.append("RECENT SECURITY EVENTS")
    report.append("-" * 60)

    if events:
        for event in events:
            report.append(
                f"[{event['timestamp']}] "
                f"{event['event']} | "
                f"{event['message']}"
            )
    else:
        report.append("No recent events.")

    report.append("")
    report.append("=" * 60)
    report.append("END OF SECURITY REPORT")
    report.append("=" * 60)

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(report))

    return REPORT_FILE


if __name__ == "__main__":
    report_path = generate_security_report()

    print("Security report generated:")
    print(report_path)