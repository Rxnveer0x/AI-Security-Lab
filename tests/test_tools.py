from app.tools import calculate


def test_addition():
    result, value = calculate("10 + 5")

    assert result is True
    assert value == 15


def test_multiplication():
    result, value = calculate("25 * 4")

    assert result is True
    assert value == 100


def test_division():
    result, value = calculate("20 / 5")

    assert result is True
    assert value == 4


def test_invalid_expression():
    result, value = calculate("hello")

    assert result is False


def test_unsafe_expression():
    result, value = calculate(
        '__import__("os").system("whoami")'
    )

    assert result is False


def test_non_string_input():
    result, value = calculate(12345)

    assert result is False