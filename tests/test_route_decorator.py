import textwrap

import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_fastapi.errors import RouteDecoratorError
from flake8_fastapi.visitors import RouteDecorator


@pytest.fixture(params=("async def", "def"))
def function_type(request) -> str:
    return request.param


def test_code_with_error(function_type: str):
    assert_error(
        RouteDecorator,
        textwrap.dedent(
            f"""
            from fastapi import FastAPI

            app = FastAPI()


            @app.route("/", methods=["GET"])
            {function_type} home():
                ...
            """
        ),
        RouteDecoratorError,
    )


def test_code_without_error(function_type: str):
    assert_not_error(
        RouteDecorator,
        textwrap.dedent(
            f"""
            from fastapi import FastAPI

            app = FastAPI()


            @app.get("/")
            {function_type} home():
                ...
            """
        ),
    )
