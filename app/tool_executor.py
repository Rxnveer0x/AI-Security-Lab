from security.tool_security import validate_tool_request
from app.tools import calculate


def execute_tool(tool_name, arguments):
    """
    Securely execute an approved tool.
    """

    is_valid, message = validate_tool_request(
        tool_name,
        arguments
    )

    if not is_valid:
        return {
            "success": False,
            "error": message
        }

    if tool_name == "calculator":

        expression = arguments.get("expression")

        if not isinstance(expression, str):
            return {
                "success": False,
                "error": "Calculator expression is required."
            }

        success, result = calculate(expression)

        if not success:
            return {
                "success": False,
                "error": result
            }

        return {
            "success": True,
            "tool": "calculator",
            "result": result
        }

    if tool_name == "security_info":

        return {
            "success": True,
            "tool": "security_info",
            "result": (
                "This AI Security Lab protects AI systems "
                "using input validation, prompt injection "
                "detection, PII detection, output security, "
                "RAG security, and tool security."
            )
        }

    return {
        "success": False,
        "error": "Tool implementation not found."
    }