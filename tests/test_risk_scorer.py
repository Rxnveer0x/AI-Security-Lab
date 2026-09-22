from security.risk_scorer import calculate_risk_score


def test_low_risk():
    result = calculate_risk_score()

    assert result["score"] == 0
    assert result["risk_level"] == "LOW"


def test_pii_risk():
    result = calculate_risk_score(
        pii_detected=["EMAIL"]
    )

    assert result["score"] == 30
    assert result["risk_level"] == "MEDIUM"


def test_prompt_injection_risk():
    result = calculate_risk_score(
        prompt_injection=True
    )

    assert result["score"] == 70
    assert result["risk_level"] == "HIGH"


def test_combined_risk():
    result = calculate_risk_score(
        prompt_injection=True,
        pii_detected=["EMAIL"]
    )

    assert result["score"] == 100
    assert result["risk_level"] == "HIGH"