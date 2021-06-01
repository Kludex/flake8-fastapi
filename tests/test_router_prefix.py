import textwrap

from flake8_plugin_utils import assert_error, assert_not_error

from flake8_fastapi.errors import RouterPrefixError
from flake8_fastapi.visitors import RouterPrefix


def test_code_with_error():
    assert_error(
        RouterPrefix,
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
        RouterPrefixError,
    )


def test_code_without_error():
    assert_not_error(
        RouterPrefix,
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
    )
