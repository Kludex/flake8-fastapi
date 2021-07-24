from pathlib import Path

from flake8_plugin_utils import assert_error, assert_not_error

from flake8_fastapi.errors import RouterPrefixError
from flake8_fastapi.visitors import RouterPrefix


def test_code_with_error():
    code = (Path(__file__).parent / "with_error.py").read_text()
    assert_error(RouterPrefix, code, RouterPrefixError)


def test_code_without_error():
    code = (Path(__file__).parent / "without_error.py").read_text()
    assert_not_error(RouterPrefix, code)
