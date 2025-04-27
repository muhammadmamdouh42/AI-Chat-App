from __future__ import annotations

import ast
import logging
import operator
from datetime import UTC, datetime
from typing import Optional

from langchain.tools import StructuredTool
from langchain.tools.retriever import create_retriever_tool
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field, ValidationError, model_validator

from app.vectorstore import vectorstore

logger = logging.getLogger(__name__)

# Calculator
class _CalcInput(BaseModel):
    """Input schema for the Calculator tool."""

    expression: str = Field(
        ...,
        description="Any arithmetic expression e.g. '2 + (3*4)'.",
        examples=["(21 / 3) + 7"],
    )

    @model_validator(mode="after")
    def _validate(self) -> "_CalcInput":  # noqa: D401
        expr = self.expression
        try:
            tree = ast.parse(expr, mode="eval")
            allowed = {
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Constant,
                ast.Add,
                ast.Sub,
                ast.Mult,
                ast.Div,
                ast.Mod,
                ast.Pow,
                ast.UAdd,
                ast.USub,
            }
            if any(node.__class__ not in allowed for node in ast.walk(tree)):
                raise ValueError("disallowed token detected")
        except Exception as exc:
            raise ValidationError.from_exception_data(
                "_CalcInput",
                [
                    {
                        "loc": ("expression",),
                        "msg": f"Invalid arithmetic expression: {exc}",
                        "type": "value_error",
                    }
                ],
            ) from exc
        return self


_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _safe_eval(expression: str) -> str:
    """Safely evaluate a simple arithmetic expression."""
    def _eval(node: ast.AST) -> float:  # recursive inner
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            if not isinstance(node.value, (int, float)):
                raise ValueError("Only numeric literals are allowed.")
            return float(node.value)
        if isinstance(node, ast.BinOp):
            return _OPS[type(node.op)](_eval(node.left), _eval(node.right))  # type: ignore[index]
        if isinstance(node, ast.UnaryOp):
            return _OPS[type(node.op)](_eval(node.operand))  # type: ignore[index]
        raise ValueError(f"Unsupported element: {node.__class__.__name__}")

    try:
        result = _eval(ast.parse(expression, mode="eval"))
    except Exception:  # noqa: BLE001
        logger.exception("Calculator failed on expression=%s", expression)
        raise
    return str(result)


calculator_tool = StructuredTool.from_function(
    name="calculator",
    description="Evaluate basic arithmetic expressions safely.",
    func=_safe_eval,
    args_schema=_CalcInput,
    return_type=str,
)

# Today-date tool
class _NoInput(BaseModel):
    """Schema for tools with no parameters (LangChain requires one)."""

    dummy: Optional[str] = Field(None, description="No input required.")


def _today_date() -> str:
    return datetime.now(UTC).date().isoformat()


today_date_tool = StructuredTool.from_function(
    name="today_date",
    description="Get today's date (UTC, ISO-8601).",
    func=_today_date,
    args_schema=_NoInput,
    return_type=str,
)

# Retriever & web search
retriever_tool = create_retriever_tool(
    vectorstore.get_retriever(),
    name="retrieve_docs",
    description=(
        "Search the user-supplied documents for relevant context "
        "and return it verbatim."
    ),
)

tavily_search_tool = TavilySearch(max_results=2)

# Public
def get_tools():
    return [
        calculator_tool,
        today_date_tool,
        retriever_tool,
        tavily_search_tool,
    ]
