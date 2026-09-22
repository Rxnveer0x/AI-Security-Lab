from pathlib import Path
from collections import Counter


LOG_FILE = Path("data/reports/security.log")


def read_security_logs():
    """Read all security log entries."""

    if not LOG_FILE.exists():
        return []

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        return [
            line.strip()
            for line in file
            if line.strip()
        ]


def get_security_summary():
    """Generate a summary of security events."""

    logs = read_security_logs()

    status_counter = Counter()
    risk_counter = Counter()

    for line in logs:

        parts = line.split(" | ")

        if len(parts) < 2:
            continue

        status = parts[1]
        status_counter[status] += 1

        if "Risk Level: HIGH" in line:
            risk_counter["HIGH"] += 1

        elif "Risk Level: MEDIUM" in line:
            risk_counter["MEDIUM"] += 1

        elif "Risk Level: LOW" in line:
            risk_counter["LOW"] += 1

    return {
        "total_events": len(logs),

        "events": {
            "ALLOWED": status_counter["ALLOWED"],
            "PROMPT_INJECTION": status_counter["PROMPT_INJECTION"],
            "JAILBREAK_DETECTED": status_counter["JAILBREAK_DETECTED"],
            "PII_DETECTED": status_counter["PII_DETECTED"],
            "INPUT_BLOCKED": status_counter["INPUT_BLOCKED"],
            "RATE_LIMITED": status_counter["RATE_LIMITED"],
            "OUTPUT_PII_DETECTED": status_counter["OUTPUT_PII_DETECTED"],
            "OUTPUT_BLOCKED": status_counter["OUTPUT_BLOCKED"],
            "RAG_INJECTION_BLOCKED": status_counter["RAG_INJECTION_BLOCKED"],
            "AI_ERROR": status_counter["AI_ERROR"],
        },

        "risk_levels": {
            "HIGH": risk_counter["HIGH"],
            "MEDIUM": risk_counter["MEDIUM"],
            "LOW": risk_counter["LOW"],
        }
    }