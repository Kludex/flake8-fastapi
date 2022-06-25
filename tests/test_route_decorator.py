import textwrap

import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_fastapi.errors import RouteDecoratorError
from flake8_fastapi.visitors import RouteDecorator


@pytest.mark.parametrize(
    "code",
    (
        pytest.param(
            textwrap.dedent(
                """
            from fastapi import FastAPI

            app = FastAPI()


            @app.route("/", methods=["GET"])
            async def home():
                ...
            """
            ),
            id="async",
        ),
        pytest.param(
            textwrap.dedent(
                """
            from fastapi import FastAPI

            app = FastAPI()


            @app.route("/", methods=["GET"])
            def home():
                ...
            """
            ),
            id="sync",
        ),
    ),
)
def test_code_with_error(code: str):
    assert_error(RouteDecorator, code, RouteDecoratorError)


@pytest.mark.parametrize(
    "code",
    (
        pytest.param(
            textwrap.dedent(
                """
            from fastapi import FastAPI

            app = FastAPI()


            @app.get("/")
            async def home():
                ...
            """
            ),
            id="async",
        ),
        pytest.param(
            textwrap.dedent(
                """
            from fastapi import FastAPI

            app = FastAPI()


            @app.get("/")
            def home():
                ...
            """
            ),
            id="sync",
        ),
    ),
)
def test_code_without_error(code: str):
    assert_not_error(RouteDecorator, code)
