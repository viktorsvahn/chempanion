#!/usr/bin/python

"""
Expression evaluator with vectorized arithmetic support.

This module safely evaluates mathematical expressions involving scalars
and Python-style list literals, applying arithmetic operators element-wise
to lists when applicable.

If an expression cannot be evaluated using the supported rules, the
original expression string is returned unchanged.
"""

import ast
import operator
from numbers import Number


#: Mapping of supported AST binary operators to their Python equivalents.
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Pow: operator.pow,
}


class EvaluationError(Exception):
    """
    Exception raised when an expression cannot be evaluated.

    This is used internally to distinguish evaluation failures from
    other runtime errors and allows graceful fallback behavior.
    """


class VectorEvaluator(ast.NodeVisitor):
    """
    AST visitor that evaluates scalar and vector expressions.

    This evaluator supports:
    - Scalar arithmetic (int, float)
    - List literals
    - Element-wise arithmetic between lists and/or scalars
    - Unary plus and minus

    Unsupported syntax or operations raise EvaluationError.
    """

    def visit_Expression(self, node):
        """
        Visit the root expression node.

        Parameters
        ----------
        node : ast.Expression
            The root AST node.

        Returns
        -------
        Any
            The evaluated result of the expression.
        """
        return self.visit(node.body)

    def visit_Constant(self, node):
        """
        Visit a constant literal (number).

        Parameters
        ----------
        node : ast.Constant

        Returns
        -------
        Number
            The literal value.
        """
        return node.value

    def visit_List(self, node):
        """
        Visit a list literal.

        Each element is recursively evaluated.

        Parameters
        ----------
        node : ast.List

        Returns
        -------
        list
            A list of evaluated elements.
        """
        return [self.visit(elt) for elt in node.elts]

    def visit_UnaryOp(self, node):
        """
        Visit a unary operation.

        Supports unary plus and minus.

        Parameters
        ----------
        node : ast.UnaryOp

        Returns
        -------
        Any
            The evaluated operand after applying the unary operator.

        Raises
        ------
        EvaluationError
            If the unary operator is unsupported.
        """
        value = self.visit(node.operand)

        if isinstance(node.op, ast.USub):
            return -value
        if isinstance(node.op, ast.UAdd):
            return value

        raise EvaluationError("Unsupported unary operator")

    def visit_BinOp(self, node):
        """
        Visit a binary operation.

        Applies element-wise operations when one or both operands are lists.

        Parameters
        ----------
        node : ast.BinOp

        Returns
        -------
        Any
            The evaluated result.

        Raises
        ------
        EvaluationError
            If operand types are incompatible or unsupported.
        """
        left = self.visit(node.left)
        right = self.visit(node.right)

        try:
            op = OPS[type(node.op)]
        except KeyError as exc:
            raise EvaluationError("Unsupported binary operator") from exc

        # Scalar ∘ scalar
        if isinstance(left, Number) and isinstance(right, Number):
            return op(left, right)

        # List ∘ scalar
        if isinstance(left, list) and isinstance(right, Number):
            return [op(x, right) for x in left]

        # Scalar ∘ list
        if isinstance(left, Number) and isinstance(right, list):
            return [op(left, x) for x in right]

        # List ∘ list
        if isinstance(left, list) and isinstance(right, list):
            if len(left) != len(right):
                raise EvaluationError("Vector length mismatch")
            return [op(x, y) for x, y in zip(left, right)]

        raise EvaluationError(
            f"Unsupported operands: {type(left).__name__} and {type(right).__name__}"
        )

    def generic_visit(self, node):
        """
        Catch-all handler for unsupported AST nodes.

        Raises
        ------
        EvaluationError
            Always raised for unsupported syntax.
        """
        raise EvaluationError(f"Unsupported syntax: {type(node).__name__}")


def evaluate(expr):
    """
    Safely evaluate a mathematical expression.

    If the expression cannot be evaluated using the supported rules,
    the original expression string is returned unchanged.

    Parameters
    ----------
    expr : str
        The expression to evaluate.

    Returns
    -------
    Any
        The evaluated result, or the original expression if evaluation fails.
    """
    try:
        tree = ast.parse(expr, mode="eval")
        return VectorEvaluator().visit(tree)
    except (EvaluationError, SyntaxError, ZeroDivisionError):
        return expr
