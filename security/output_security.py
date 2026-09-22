from security.pii_detector import detect_pii


def check_output(output):
    if not isinstance(output, str):
        return False, []

    pii_detected = detect_pii(output)

    if pii_detected:
        return True, pii_detected

    return False, []