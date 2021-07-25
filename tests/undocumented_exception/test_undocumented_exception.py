from flake8_plugin_utils import assert_error, assert_not_error

from flake8_fastapi.errors import UndocumentedHTTPExceptionError
from flake8_fastapi.visitors import UndocumentedHTTPException


def test_code_with_error(code: str):
    assert_error(UndocumentedHTTPException, code, UndocumentedHTTPExceptionError)


def test_code_without_error(code: str):
    assert_not_error(UndocumentedHTTPException, code)
