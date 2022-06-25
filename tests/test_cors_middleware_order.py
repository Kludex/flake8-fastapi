import textwrap

import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_fastapi.errors import CORSMiddlewareOrderError
from flake8_fastapi.visitors import CORSMiddlewareOrder


@pytest.mark.parametrize(
    "code",
    (
        pytest.param(
            textwrap.dedent(
                """
                from fastapi import FastAPI
                from fastapi.middleware.cors import CORSMiddleware
                from fastapi.middleware.gzip import GZipMiddleware

                app = FastAPI()

                app.add_middleware(
                    CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                )
                app.add_middleware(GZipMiddleware)
                """
            ),
            id="args",
        ),
        pytest.param(
            textwrap.dedent(
                """
                from fastapi import FastAPI
                from fastapi.middleware.cors import CORSMiddleware
                from fastapi.middleware.gzip import GZipMiddleware

                app = FastAPI()

                app.add_middleware(
                    middleware_class=CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                )
                app.add_middleware(middleware_class=GZipMiddleware)
                """
            ),
            id="kwargs",
        ),
    ),
)
def test_code_with_error(code: str):
    assert_error(CORSMiddlewareOrder, code, CORSMiddlewareOrderError)


@pytest.mark.parametrize(
    "code",
    (
        pytest.param(
            textwrap.dedent(
                """
                from fastapi import FastAPI
                from fastapi.middleware.cors import CORSMiddleware
                from fastapi.middleware.gzip import GZipMiddleware

                app = FastAPI()

                app.add_middleware(GZipMiddleware)
                app.add_middleware(
                    CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                )
                """
            ),
            id="args",
        ),
        pytest.param(
            textwrap.dedent(
                """
                from fastapi import FastAPI
                from fastapi.middleware.cors import CORSMiddleware
                from fastapi.middleware.gzip import GZipMiddleware

                app = FastAPI()

                app.add_middleware(middleware_class=GZipMiddleware)
                app.add_middleware(
                    middleware_class=CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                )
                """
            ),
            id="kwargs",
        ),
    ),
)
def test_code_without_error(code: str):
    assert_not_error(CORSMiddlewareOrder, code)
