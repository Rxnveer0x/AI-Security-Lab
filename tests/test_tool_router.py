from app.tool_router import (
    detect_calculator_request,
    route_tool_request
)


def test_calculator_detection():
    result = detect_calculator_request(
        "calculate 25 * 4"
    )

    assert result == "25 * 4"


def test_solve_detection():
    result = detect_calculator_request(
        "solve 10 + 5"
    )

    assert result == "10 + 5"


def test_normal_message():
    result = detect_calculator_request(
        "Hello"
    )

    assert result is None


def test_calculator_routing():
    result = route_tool_request(
        "calculate 25 * 4"
    )

    assert result["success"] is True
    assert result["result"] == 100