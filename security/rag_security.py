import re


SUSPICIOUS_RAG_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "disregard previous instructions",
    "ignore the system instructions",
    "follow these instructions instead",
    "override the instructions",
    "forget the instructions",
]


def detect_rag_injection(text):
    """
    Detect prompt-injection instructions hidden inside
    retrieved documents or RAG context.

    Returns:
        True  -> suspicious instruction detected
        False -> no suspicious instruction detected
    """

    if not isinstance(text, str):
        return False

    text = re.sub(r"\s+", " ", text.lower()).strip()

    for pattern in SUSPICIOUS_RAG_PATTERNS:
        if pattern in text:
            return True

    return False


def validate_rag_context(context):
    """
    Validate retrieved RAG context before it is given to the AI.

    Returns:
        (True, "RAG context is safe.")
        or
        (False, "Suspicious instruction detected in RAG context.")
    """

    if not isinstance(context, str):
        return False, "Invalid RAG context."

    if not context.strip():
        return False, "RAG context is empty."

    if detect_rag_injection(context):
        return False, "Suspicious instruction detected in RAG context."

    return True, "RAG context is safe."