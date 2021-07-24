import textwrap

from flake8_plugin_utils import assert_error, assert_not_error

from flake8_fastapi.errors import CORSMiddlewareOrderError
from flake8_fastapi.visitors import CORSMiddlewareOrder


def test_code_with_error():
    # With arguments
    assert_error(
        CORSMiddlewareOrder,
        textwrap.dedent(
            """
            from fastapi import FastAPI

            app = FastAPI()

            app.add_middleware(
                CORSMiddleware,
                allow_origins=['*'],
                allow_credentials=True,
                allow_methods=['*'],
                allow_headers=['*']
            )
            app.add_middleware(GZipMiddleware)
            """
        ),
        CORSMiddlewareOrderError,
    )

    # With keywords
    assert_error(
        CORSMiddlewareOrder,
        textwrap.dedent(
            """
            from fastapi import FastAPI

            app = FastAPI()

            app.add_middleware(
                middleware_class=CORSMiddleware,
                allow_origins=['*'],
                allow_credentials=True,
                allow_methods=['*'],
                allow_headers=['*']
            )
            app.add_middleware(middleware_class=GZipMiddleware)
            """
        ),
        CORSMiddlewareOrderError,
    )


def test_code_without_error():
    # With arguments
    assert_not_error(
        CORSMiddlewareOrder,
        textwrap.dedent(
            """
            from fastapi import FastAPI

            app = FastAPI()

            app.add_middleware(GZipMiddleware)
            app.add_middleware(
                CORSMiddleware,
                allow_origins=['*'],
                allow_credentials=True,
                allow_methods=['*'],
                allow_headers=['*']
            )
            """
        ),
    )

    # With keywords
    assert_not_error(
        CORSMiddlewareOrder,
        textwrap.dedent(
            """
            from fastapi import FastAPI

            app = FastAPI()

            app.add_middleware(middleware_class=GZipMiddleware)
            app.add_middleware(
                middleware_class=CORSMiddleware,
                allow_origins=['*'],
                allow_credentials=True,
                allow_methods=['*'],
                allow_headers=['*']
            )
            """
        ),
    )
