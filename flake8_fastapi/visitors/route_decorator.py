import ast

from flake8_plugin_utils import Visitor

from flake8_fastapi.errors import RouteDecoratorError


class RouteDecorator(Visitor):
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        for decorator in node.decorator_list:
            if (
                isinstance(decorator.func, ast.Attribute)
                and decorator.func.attr == "route"
            ):
                self.error_from_node(RouteDecoratorError, node)
