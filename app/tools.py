import ast
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def calculate(expression):
    """
    Safely evaluate basic mathematical expressions.
    """

    if not isinstance(expression, str):
        return False, "Expression must be text."

    if len(expression) > 100:
        return False, "Expression is too long."

    try:
        tree = ast.parse(
            expression,
            mode="eval"
        )

        result = evaluate_node(tree.body)

        return True, result

    except Exception:
        return False, "Invalid mathematical expression."


def evaluate_node(node):

    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Invalid value.")

    if isinstance(node, ast.BinOp):

        operator_function = OPERATORS.get(
            type(node.op)
        )

        if operator_function is None:
            raise ValueError("Operator not allowed.")

        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        return operator_function(left, right)

    raise ValueError("Operation not allowed.")