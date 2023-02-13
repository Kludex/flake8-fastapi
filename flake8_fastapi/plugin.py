import ast
from typing import Iterable

from flake8_plugin_utils import Plugin
from flake8_plugin_utils.plugin import FLAKE8_ERROR

from flake8_fastapi import __version__
from flake8_fastapi.visitors import (
    CORSMiddlewareOrder,
    NoContentResponse,
    RouteDecorator,
    RouterPrefix,
    UndocumentedHTTPException,
)


class FastAPIPlugin(Plugin):
    name = "flake8-fastapi"
    version = __version__
    visitors = [
        RouteDecorator,
        RouterPrefix,
        CORSMiddlewareOrder,
        NoContentResponse,
        UndocumentedHTTPException,
    ]

    def __init__(self, tree: ast.AST, filename: str) -> None:
        super().__init__(tree)
        self._filename = filename

    def run(self) -> Iterable[FLAKE8_ERROR]:
        for visitor_cls in self.visitors:
            visitor = self._create_visitor(visitor_cls)
            visitor._filename = self._filename
            visitor.visit(self._tree)

            for error in visitor.errors:
                yield self._error(error)
