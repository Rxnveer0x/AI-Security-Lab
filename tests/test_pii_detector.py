from security.pii_detector import detect_pii


def test_email_detection():
    result = detect_pii("My email is test@example.com")
    assert "EMAIL" in result


def test_phone_detection():
    result = detect_pii("My phone number is 9876543210")
    assert "PHONE" in result


def test_ip_detection():
    result = detect_pii("The server IP is 192.168.1.10")
    assert "IP_ADDRESS" in result


def test_credit_card_detection():
    result = detect_pii("Card number 1234 5678 9012 3456")
    assert "CREDIT_CARD" in result


def test_no_pii():
    result = detect_pii("What is cybersecurity?")
    assert result == []