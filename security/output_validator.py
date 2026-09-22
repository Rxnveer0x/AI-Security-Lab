import re


SECRET_PATTERNS = {
    "API_KEY": r"\b(?:sk-[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{20,})\b",

    "AWS_ACCESS_KEY": r"\bAKIA[0-9A-Z]{16}\b",

    "JWT_TOKEN": r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b",

    "PRIVATE_KEY": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",

    "PASSWORD": r"(?i)\b(?:password|passwd|pwd)\s*[:=]\s*[^\s]+",

    "SECRET": r"(?i)\b(?:secret|api_secret|client_secret)\s*[:=]\s*[^\s]+",
}


def detect_sensitive_output(text):
    """
    Detect secrets or sensitive credentials in AI-generated output.

    Returns:
        (detected, findings)
    """

    if not isinstance(text, str):
        return False, []

    findings = []

    for secret_type, pattern in SECRET_PATTERNS.items():
        if re.search(pattern, text):
            findings.append(secret_type)

    return bool(findings), findings


def validate_output(text):
    """
    Validate AI-generated output before returning it to the user.
    """

    detected, findings = detect_sensitive_output(text)

    if detected:
        return False, findings

    return True, []