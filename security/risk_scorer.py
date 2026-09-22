def calculate_risk_score(
    prompt_injection=False,
    pii_detected=None
):
    score = 0
    reasons = []

    if prompt_injection:
        score += 70
        reasons.append("Prompt injection detected")

    if pii_detected:
        score += 30
        reasons.append(
            "Sensitive information detected: "
            + ", ".join(pii_detected)
        )

    if score >= 70:
        risk_level = "HIGH"
    elif score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "score": score,
        "risk_level": risk_level,
        "reasons": reasons
    }