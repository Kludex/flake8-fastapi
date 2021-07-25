import ast
from typing import Optional, Set, Union

from flake8_plugin_utils import Visitor
from flake8_plugin_utils.plugin import TConfig

from flake8_fastapi.errors import UndocumentedHTTPExceptionError

ASTCallable = Union[ast.AsyncFunctionDef, ast.FunctionDef]


class UndocumentedHTTPException(Visitor):
    METHODS = ("get", "post", "put", "patch", "delete", "head", "options", "trace")

    def __init__(self, config: Optional[TConfig] = None) -> None:
        super().__init__(config=config)

    def generic_visit(self, node: ast.AST) -> None:
        self.parent = node
        for child in ast.walk(self.parent):
            if isinstance(child, (ast.AsyncFunctionDef, ast.FunctionDef)):
                for decorator in child.decorator_list:
                    if (
                        isinstance(decorator, ast.Call)
                        and isinstance(decorator.func, ast.Attribute)
                        and decorator.func.attr in self.METHODS
                    ):
                        self._visit_func(child)

    def _visit_func(self, node: ASTCallable) -> None:
        documented_status = set()
        excepted_status = set()

        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                for keyword in decorator.keywords:
                    if keyword.arg == "responses" and isinstance(
                        keyword.value, ast.Dict
                    ):
                        for key in keyword.value.keys:
                            if isinstance(key, ast.Constant):
                                documented_status.add(int(key.value))

        excepted_status = self.find_exceptions_in_body(node)

        if documented_status != excepted_status:
            self.error_from_node(UndocumentedHTTPExceptionError, node)

    def find_exceptions_in_body(self, node: ASTCallable) -> Set[int]:
        excepted_status = set()

        for element in node.body:
            if isinstance(element, ast.Raise):
                if isinstance(element.exc, ast.Call):
                    if element.exc.args and isinstance(
                        element.exc.args[0], ast.Constant
                    ):
                        excepted_status.add(element.exc.args[0].value)

                    for keyword in element.exc.keywords:
                        if keyword.arg == "status_code":
                            if isinstance(keyword.value, ast.Constant):
                                excepted_status.add(keyword.value.value)

            if isinstance(element, ast.Expr) and isinstance(element.value, ast.Call):
                func_name = None
                if isinstance(element.value.func, ast.Attribute):
                    func_name = element.value.func.attr
                elif isinstance(element.value.func, ast.Name):
                    func_name = element.value.func.id

                if func_name is not None:
                    body = self.find_function(func_name)
                    _excepted_status = self.find_exceptions_in_body(body)
                    excepted_status.update(_excepted_status)

        return excepted_status

    def find_function(self, func_name: str) -> ASTCallable:  # type: ignore[return]
        for child in ast.walk(self.parent):
            if (
                isinstance(child, (ast.AsyncFunctionDef, ast.FunctionDef))
                and child.name == func_name
            ):
                return child
