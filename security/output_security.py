import re

from security.pii_detector import detect_pii


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
# OUTPUT PII CHECK
# ============================================================

def check_output(text):
    """
    Check AI-generated output for PII.

    Returns:
        (
            pii_detected,
            detected_pii
        )
    """

    if not isinstance(text, str):
        return False, []

    detected_pii = detect_pii(text)

    return bool(detected_pii), detected_pii


# ============================================================
# SENSITIVE INFORMATION DETECTION
# ============================================================

def detect_sensitive_output(text):
    """
    Detect secrets and sensitive credentials
    in AI-generated output.
    """

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
# OUTPUT VALIDATOR
# ============================================================

def validate_output(text):
    """
    Validate AI-generated output.

    Returns:
        (
            output_is_safe,
            detected_findings
        )
    """

    detected_findings = detect_sensitive_output(text)

    return (
        len(detected_findings) == 0,
        detected_findings
    )