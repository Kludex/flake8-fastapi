import textwrap

from flake8_plugin_utils import assert_error, assert_not_error

from flake8_fastapi.errors import RouteDecoratorError
from flake8_fastapi.visitors import RouteDecorator


def test_code_with_error():
    assert_error(
        RouteDecorator,
        textwrap.dedent(
            """
            from fastapi import FastAPI

            app = FastAPI()


            @app.route("/", methods=["GET"])
            def home():
                ...
            """
        ),
        RouteDecoratorError,
    )


def test_code_without_error():
    assert_not_error(
        RouteDecorator,
        textwrap.dedent(
            """
            from fastapi import FastAPI

            app = FastAPI()


            @app.get("/")
            def home():
                ...
            """
        ),
    )
