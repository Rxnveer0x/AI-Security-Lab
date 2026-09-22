from security.security_logger import log_security_event


ALLOWED_TOOLS = {
    "calculator",
    "security_info",
}


def is_tool_allowed(tool_name):
    """
    Check whether a requested tool is allowed.
    """

    if not isinstance(tool_name, str):
        return False

    return tool_name in ALLOWED_TOOLS


def validate_tool_request(tool_name, arguments):
    """
    Validate a tool request before execution.
    """

    if not is_tool_allowed(tool_name):
        log_security_event(
            f"Blocked tool: {tool_name}",
            "TOOL_BLOCKED"
        )

        return False, "Tool is not allowed."

    if not isinstance(arguments, dict):
        log_security_event(
            f"Invalid arguments for tool: {tool_name}",
            "TOOL_INPUT_BLOCKED"
        )

        return False, "Tool arguments must be a dictionary."

    log_security_event(
        f"Allowed tool request: {tool_name}",
        "TOOL_ALLOWED"
    )

    return True, "Tool request is valid."