MAX_MESSAGE_LENGTH = 1000


def validate_input(data):
    if not isinstance(data, dict):
        return False, "Invalid JSON data."

    if "message" not in data:
        return False, "Message field is required."

    message = data["message"]

    if not isinstance(message, str):
        return False, "Message must be text."

    if not message.strip():
        return False, "Message cannot be empty."

    if len(message) > MAX_MESSAGE_LENGTH:
        return False, "Message is too long."

    return True, "Input is valid."
