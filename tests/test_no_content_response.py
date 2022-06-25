import textwrap

import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_fastapi.errors import NoContentResponseError
from flake8_fastapi.visitors import NoContentResponse


@pytest.mark.parametrize(
    "code",
    (
        pytest.param(
            textwrap.dedent(
                """
                from fastapi import FastAPI

                app = FastAPI()


                @app.get("/", status_code=204)
                def home():
                    ...
                """
            ),
            id="int",
        ),
    ),
)
def test_code_with_error(code: str):
    assert_error(NoContentResponse, code, NoContentResponseError)


@pytest.mark.parametrize(
    "code",
    (
        pytest.param(
            textwrap.dedent(
                """
                from fastapi import FastAPI, Response

                app = FastAPI()


                @app.get("/", status_code=204)
                def home():
                    return Response(status_code=204)
                """
            ),
            id="return",
        ),
        pytest.param(
            textwrap.dedent(
                """
                from fastapi import FastAPI, Response

                app = FastAPI()


                @app.get("/", status_code=204, response_class=Response)
                def home():
                    ...
                """
            ),
            id="response_class",
        ),
    ),
)
def test_code_without_error(code: str):
    assert_not_error(NoContentResponse, code)
