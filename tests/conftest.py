import os
from pathlib import Path
from typing import List

import pytest


def filter_files(parent: Path, pattern: str) -> List[str]:
    codes = []
    for file in os.listdir(parent):
        if file.startswith(pattern):
            codes.append((parent / file).read_text())
    return codes


def pytest_generate_tests(metafunc: pytest.Function):
    if "code" in metafunc.fixturenames:
        parent = Path(metafunc.module.__file__).parent
        if metafunc.function.__name__ == "test_code_with_error":
            files = filter_files(parent, "with_")
            metafunc.parametrize("code", files)
        elif metafunc.function.__name__ == "test_code_without_error":
            files = filter_files(parent, "without_")
            metafunc.parametrize("code", files)
