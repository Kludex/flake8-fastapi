import textwrap

import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_fastapi.errors import RouterPrefixError
from flake8_fastapi.visitors import RouterPrefix


@pytest.mark.parametrize(
    "code",
    (
        pytest.param(
            textwrap.dedent(
                """
            from fastapi import APIRouter, FastAPI

            router = APIRouter()


            @router.get("/")
            def home():
                ...


            app = FastAPI()
            app.include_router(router, prefix="/prefix")
            """
            ),
        ),
    ),
)
def test_code_with_error(code: str):
    assert_error(RouterPrefix, code, RouterPrefixError)


@pytest.mark.parametrize(
    "code",
    (
        pytest.param(
            textwrap.dedent(
                """
            from fastapi import APIRouter, FastAPI

            router = APIRouter(prefix="/prefix")


            @router.get("/")
            def home():
                ...


            app = FastAPI()
            app.include_router(router)
            """
            ),
        ),
    ),
)
def test_code_without_error(code: str):
    assert_not_error(RouterPrefix, code)
