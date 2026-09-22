import re

from app.tool_executor import execute_tool


def is_math_expression(expression):
    """
    Check whether the expression contains only
    characters allowed for basic mathematics.
    """

    if not isinstance(expression, str):
        return False

    expression = expression.strip()

    if not expression:
        return False

    if len(expression) > 100:
        return False

    # Only numbers, decimal points, spaces and
    # basic mathematical operators.
    return bool(
        re.fullmatch(
            r"[0-9+\-*/().\s]+",
            expression
        )
    )


def detect_calculator_request(message):
    """
    Detect genuine calculator requests.
    """

    if not isinstance(message, str):
        return None

    text = message.strip()

    patterns = [
        r"^calculate\s+(.+)$",
        r"^solve\s+(.+)$",
    ]

    for pattern in patterns:

        match = re.match(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            expression = match.group(1).strip()

            if is_math_expression(expression):
                return expression

            return None

    # Also allow direct mathematical expressions
    # such as 100/5 or 25*100.
    if is_math_expression(text):

        if any(
            operator in text
            for operator in ["+", "-", "*", "/"]
        ):
            return text

    return None


def route_tool_request(message):
    """
    Route recognized mathematical requests
    through the secure calculator.
    """

    expression = detect_calculator_request(message)

    if expression is None:
        return None

    return execute_tool(
        "calculator",
        {
            "expression": expression
        }
    )