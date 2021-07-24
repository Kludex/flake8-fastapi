import ast
from typing import List, Optional

from flake8_plugin_utils import Visitor
from flake8_plugin_utils.plugin import TConfig

from flake8_fastapi.errors import CORSMiddlewareOrderError


class CORSMiddlewareOrder(Visitor):
    def __init__(self, config: Optional[TConfig] = None) -> None:
        super().__init__(config=config)
        self._application_name: Optional[str] = None
        self._middlewares: List[str] = []

    def generic_visit(self, node: ast.AST):
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Assign):
                self.visit_Assign(stmt)
            if isinstance(stmt, ast.Call):
                self.visit_Call(stmt)

    def visit_Call(self, node: ast.Call) -> None:
        if (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == self._application_name
            and node.func.attr == "add_middleware"
        ):
            for arg in node.args:
                if isinstance(arg, ast.Name):
                    self._middlewares.append(arg.id)
            for keyword in node.keywords:
                if keyword.arg == "middleware_class" and isinstance(
                    keyword.value, ast.Name
                ):
                    self._middlewares.append(keyword.value.id)

        if (
            "CORSMiddleware" in self._middlewares
            and self._middlewares[-1] != "CORSMiddleware"
        ):
            self.error_from_node(CORSMiddlewareOrderError, node)

    def visit_Assign(self, node: ast.Assign):
        if (
            isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name)
            and node.value.func.id == "FastAPI"
        ):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self._application_name = target.id
