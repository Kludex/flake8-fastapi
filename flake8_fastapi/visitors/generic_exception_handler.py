import ast
from typing import Union

from flake8_plugin_utils import Visitor

from flake8_fastapi.errors import GenericExceptionHandlerError


class GenericExceptionHandler(Visitor):
    def generic_visit(self, node: ast.AST) -> None:
        for node in ast.walk(node):
            if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
                self._visit_func(node)

    def _visit_func(self, node: Union[ast.AsyncFunctionDef, ast.FunctionDef]) -> None:
        for decorator in node.decorator_list:
            if (
                isinstance(decorator, ast.Call)
                and isinstance(decorator.func, ast.Attribute)
                and decorator.func.attr == "exception_handler"
            ):
                for arg in decorator.args:
                    if isinstance(arg, ast.Name) and arg.id == "Exception":
                        self.error_from_node(GenericExceptionHandlerError, node)

                for keyword in decorator.keywords:
                    if (
                        isinstance(keyword.value, ast.Name)
                        and keyword.arg == "exc_class_or_status_code"
                        and keyword.value.id == "Exception"
                    ):
                        self.error_from_node(GenericExceptionHandlerError, node)
