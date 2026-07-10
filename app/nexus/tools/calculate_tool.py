import ast
import operator
from typing import Callable

from langchain_core.tools import tool

_ALLOWED_BINARY_OPERATORS: dict[type, Callable] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_ALLOWED_UNARY_OPERATORS: dict[type, Callable] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Apenas números são permitidos.")

    if isinstance(node, ast.BinOp):
        operator_type: type = type(node.op)

        if operator_type not in _ALLOWED_BINARY_OPERATORS:
            raise ValueError("Operador não suportado.")

        left: float = _evaluate_node(node=node.left)
        right: float = _evaluate_node(node=node.right)

        return _ALLOWED_BINARY_OPERATORS[operator_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operator_type: type = type(node.op)

        if operator_type not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError("Operador unário não suportado.")

        operand: float = _evaluate_node(node=node.operand)

        return _ALLOWED_UNARY_OPERATORS[operator_type](operand)

    raise ValueError("Expressão inválida.")


@tool
def calculate_tool(expression: str) -> dict:
    """
    Avalia uma expressão aritmética simples e retorna o resultado.

    Args:
        expression: A expressão aritmética a ser avaliada, ex.: "2 + 3 * (4 - 1)".

    Returns:
        Um dict com a chave `result` contendo o valor numérico em caso de sucesso,
        ou a chave `error` com a mensagem de erro em caso de falha.
    """
    try:
        parsed: ast.Expression = ast.parse(
            source=expression,
            mode="eval",
        )

        result: float = _evaluate_node(node=parsed.body)

        return {"result": result}

    except (ValueError, SyntaxError, ZeroDivisionError) as error:
        return {"error": str(error)}
