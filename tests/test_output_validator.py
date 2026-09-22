from security.output_validator import validate_output


def test_clean_output():
    result, findings = validate_output(
        "Cybersecurity protects systems and data."
    )

    assert result is True
    assert findings == []


def test_api_key_detection():
    result, findings = validate_output(
        "API key: sk-123456789012345678901234"
    )

    assert result is False
    assert "API_KEY" in findings


def test_password_detection():
    result, findings = validate_output(
        "password=MySecret123"
    )

    assert result is False
    assert "PASSWORD" in findings


def test_aws_key_detection():
    result, findings = validate_output(
        "AWS key: AKIA1234567890ABCDEF"
    )

    assert result is False
    assert "AWS_ACCESS_KEY" in findings