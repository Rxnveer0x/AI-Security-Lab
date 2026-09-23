import re


# ============================================================
# SENSITIVE OUTPUT PATTERNS
# ============================================================

SENSITIVE_PATTERNS = {

    "API_KEY": [
        r"\bsk-[A-Za-z0-9_-]{10,}\b",
        r"\bapi[_-]?key\s*[:=]\s*[A-Za-z0-9_-]{8,}\b",
    ],

    "AWS_ACCESS_KEY": [
        r"\bAKIA[0-9A-Z]{16}\b",
    ],

    "PASSWORD": [
        r"\bpassword\s*[:=]\s*\S+\b",
    ],

}


# ============================================================
# DETECT SENSITIVE OUTPUT
# ============================================================

def detect_sensitive_output(text):

    if not isinstance(text, str):
        return []

    detected = []

    for category, patterns in SENSITIVE_PATTERNS.items():

        for pattern in patterns:

            if re.search(
                pattern,
                text,
                re.IGNORECASE
            ):

                detected.append(category)

                break

    return detected


# ============================================================
# VALIDATE OUTPUT
# ============================================================

def validate_output(text):

    detected_findings = detect_sensitive_output(
        text
    )

    if detected_findings:

        return (
            False,
            detected_findings
        )

    return (
        True,
        []
    )