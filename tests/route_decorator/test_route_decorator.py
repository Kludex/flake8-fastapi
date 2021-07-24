from pathlib import Path

import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_fastapi.errors import RouteDecoratorError
from flake8_fastapi.visitors import RouteDecorator


@pytest.mark.parametrize(
    "code",
    [
        (Path(__file__).parent / "with_error_async.py").read_text(),
        (Path(__file__).parent / "with_error_sync.py").read_text(),
    ],
)
def test_code_with_error(code: str):
    assert_error(RouteDecorator, code, RouteDecoratorError)


@pytest.mark.parametrize(
    "code",
    [
        (Path(__file__).parent / "without_error_async.py").read_text(),
        (Path(__file__).parent / "without_error_sync.py").read_text(),
    ],
)
def test_code_without_error(code: str):
    assert_not_error(RouteDecorator, code)
