import re


PII_PATTERNS = {
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",

    "PHONE": r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",

    "IP_ADDRESS": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",

    "CREDIT_CARD": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
}


def detect_pii(message):
    detected = []

    for pii_type, pattern in PII_PATTERNS.items():

        if re.search(pattern, message):
            detected.append(pii_type)

    return detected