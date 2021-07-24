import ast
from typing import Union

from flake8_plugin_utils import Visitor

from flake8_fastapi.errors import RouteDecoratorError


class RouteDecorator(Visitor):
    def generic_visit(self, node: ast.AST) -> None:
        for node in ast.walk(node):
            if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
                self._visit_func(node)

    def _visit_func(self, node: Union[ast.AsyncFunctionDef, ast.FunctionDef]) -> None:
        for decorator in node.decorator_list:
            if (
                isinstance(decorator, ast.Call)
                and isinstance(decorator.func, ast.Attribute)
                and decorator.func.attr == "route"
            ):
                self.error_from_node(RouteDecoratorError, node)
