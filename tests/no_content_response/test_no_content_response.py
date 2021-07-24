from pathlib import Path

import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_fastapi.errors import NoContentResponseError
from flake8_fastapi.visitors import NoContentResponse


def test_code_with_error():
    code = (Path(__file__).parent / "with_error.py").read_text()
    assert_error(NoContentResponse, code, NoContentResponseError)


@pytest.mark.parametrize(
    "code",
    [
        (Path(__file__).parent / "without_error.py").read_text(),
        (Path(__file__).parent / "without_error_return.py").read_text(),
    ],
)
def test_code_without_error(code: str):
    assert_not_error(NoContentResponse, code)
