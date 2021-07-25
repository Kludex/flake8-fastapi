import ast
from typing import Union

from flake8_plugin_utils import Visitor

from flake8_fastapi.errors import NoContentResponseError


class NoContentResponse(Visitor):
    METHODS = ("get", "post", "put", "patch", "delete", "head", "options", "trace")

    def generic_visit(self, node: ast.AST) -> None:
        for node in ast.walk(node):
            if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
                self._visit_func(node)

    def _visit_func(self, node: Union[ast.AsyncFunctionDef, ast.FunctionDef]) -> None:
        return_stmt = None
        for arg in node.body:
            if (
                isinstance(arg, ast.Return)
                and isinstance(arg.value, ast.Call)
                and isinstance(arg.value.func, ast.Name)
            ):
                return_stmt = arg.value.func.id

        for decorator in node.decorator_list:
            if (
                isinstance(decorator, ast.Call)
                and isinstance(decorator.func, ast.Attribute)
                and decorator.func.attr in self.METHODS
            ):
                for keyword in decorator.keywords:
                    if (
                        keyword.arg == "status_code"
                        and isinstance(keyword.value, ast.Constant)
                        and keyword.value.value == 204
                    ):
                        if return_stmt == "Response":
                            return None

                        for inside_keyword in decorator.keywords:
                            if (
                                inside_keyword.arg == "response_class"
                                and isinstance(inside_keyword.value, ast.Name)
                                and inside_keyword.value.id == "Response"
                            ):
                                return None
                        self.error_from_node(NoContentResponseError, node)
