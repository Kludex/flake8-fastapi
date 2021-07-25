from flake8_plugin_utils import assert_error, assert_not_error

from flake8_fastapi.errors import RouteDecoratorError
from flake8_fastapi.visitors import RouteDecorator


def test_code_with_error(code: str):
    assert_error(RouteDecorator, code, RouteDecoratorError)


def test_code_without_error(code: str):
    assert_not_error(RouteDecorator, code)
