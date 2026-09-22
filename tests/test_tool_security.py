from security.tool_security import (
    is_tool_allowed,
    validate_tool_request
)


def test_allowed_tool():
    assert is_tool_allowed("calculator") is True


def test_second_allowed_tool():
    assert is_tool_allowed("security_info") is True


def test_unknown_tool():
    assert is_tool_allowed("unknown_tool") is False


def test_invalid_tool_type():
    assert is_tool_allowed(123) is False


def test_valid_tool_request():
    result, message = validate_tool_request(
        "calculator",
        {"expression": "2 + 2"}
    )

    assert result is True


def test_blocked_tool_request():
    result, message = validate_tool_request(
        "system_command",
        {}
    )

    assert result is False


def test_invalid_arguments():
    result, message = validate_tool_request(
        "calculator",
        "2 + 2"
    )

    assert result is False