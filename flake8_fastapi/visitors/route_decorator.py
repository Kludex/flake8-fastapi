import ast
from typing import Union

from flake8_plugin_utils import Visitor

from flake8_fastapi.errors import RouteDecoratorError


class RouteDecorator(Visitor):
    def _visit_func(self, node: Union[ast.AsyncFunctionDef, ast.FunctionDef]) -> None:
        for decorator in node.decorator_list:
            if (
                isinstance(decorator, ast.Call)
                and isinstance(decorator.func, ast.Attribute)
                and decorator.func.attr == "route"
            ):
                self.error_from_node(RouteDecoratorError, node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_func(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_func(node)
