from pathlib import Path

import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_fastapi.errors import GenericExceptionHandlerError
from flake8_fastapi.visitors import GenericExceptionHandler


def test_code_with_error(code: str):
    assert_error(GenericExceptionHandler, code, GenericExceptionHandlerError)


def test_code_without_error(code: str):
    assert_not_error(GenericExceptionHandler, code)
