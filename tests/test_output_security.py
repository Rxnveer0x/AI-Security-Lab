from security.output_security import check_output


def test_safe_output():
    result, pii = check_output(
        "Cybersecurity protects systems and data."
    )

    assert result is False
    assert pii == []


def test_email_in_output():
    result, pii = check_output(
        "The user's email is test@example.com"
    )

    assert result is True
    assert "EMAIL" in pii


def test_phone_in_output():
    result, pii = check_output(
        "The phone number is 9876543210"
    )

    assert result is True
    assert "PHONE" in pii


def test_ip_in_output():
    result, pii = check_output(
        "The server address is 192.168.1.10"
    )

    assert result is True
    assert "IP_ADDRESS" in pii
    