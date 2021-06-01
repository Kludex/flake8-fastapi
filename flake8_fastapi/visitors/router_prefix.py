import ast

from flake8_plugin_utils import Visitor

from flake8_fastapi.errors import RouterPrefixError


class RouterPrefix(Visitor):
    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Attribute) and node.func.attr == "include_router":
            if "prefix" in (kwd.arg for kwd in node.keywords):
                self.error_from_node(RouterPrefixError, node)
