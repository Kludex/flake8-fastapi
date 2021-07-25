from flake8_plugin_utils import assert_error, assert_not_error

from flake8_fastapi.errors import CORSMiddlewareOrderError
from flake8_fastapi.visitors import CORSMiddlewareOrder


def test_code_with_error(code: str):
    assert_error(CORSMiddlewareOrder, code, CORSMiddlewareOrderError)


def test_code_without_error(code: str):
    assert_not_error(CORSMiddlewareOrder, code)
