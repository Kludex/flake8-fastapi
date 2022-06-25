import textwrap

import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_fastapi.errors import UndocumentedHTTPExceptionError
from flake8_fastapi.visitors import UndocumentedHTTPException


@pytest.mark.parametrize(
    "code",
    (
        pytest.param(
            textwrap.dedent(
                """
                from fastapi import FastAPI, HTTPException

                app = FastAPI()


                @app.get("/")
                def home():
                    raise HTTPException(400, detail="Bad Request")
                """
            ),
            id="arg",
        ),
        pytest.param(
            textwrap.dedent(
                """
                from fastapi import FastAPI, HTTPException

                app = FastAPI()


                class MyClass:
                    def raise_here(self):
                        raise HTTPException(status_code=400, detail="Bad Request")


                @app.get("/")
                def home():
                    my_object = MyClass()
                    my_object.raise_here()
                """
            ),
            id="object",
        ),
        pytest.param(
            textwrap.dedent(
                """
                from fastapi import FastAPI, HTTPException

                app = FastAPI()


                def raise_here():
                    raise HTTPException(status_code=400, detail="Bad Request")


                @app.get("/")
                def home():
                    raise_here()
                """
            ),
            id="stack",
        ),
        pytest.param(
            textwrap.dedent(
                """
                from fastapi import FastAPI, HTTPException

                app = FastAPI()


                @app.get("/")
                def home():
                    raise HTTPException(status_code=400, detail="Bad Request")
                """
            )
        ),
    ),
)
def test_code_with_error(code: str):
    assert_error(UndocumentedHTTPException, code, UndocumentedHTTPExceptionError)


@pytest.mark.parametrize(
    "code",
    (
        pytest.param(
            textwrap.dedent(
                """
                from fastapi import FastAPI, HTTPException

                app = FastAPI()


                @app.get("/", responses={400: {"description": "Bad Request"}})
                def home():
                    raise HTTPException(400, detail="Bad Request")
                """
            ),
            id="arg",
        ),
        pytest.param(
            textwrap.dedent(
                """
                from fastapi import FastAPI, HTTPException

                app = FastAPI()


                class MyClass:
                    def raise_here(self):
                        raise HTTPException(status_code=400, detail="Bad Request")


                @app.get("/", responses={400: {"description": "Bad Request"}})
                def home():
                    my_object = MyClass()
                    my_object.raise_here()
                """
            ),
            id="object",
        ),
        pytest.param(
            textwrap.dedent(
                """
                from fastapi import FastAPI, HTTPException

                app = FastAPI()


                def raise_here():
                    raise HTTPException(status_code=400, detail="Bad Request")


                @app.get("/", responses={400: {"description": "Bad Request"}})
                def home():
                    raise_here()
                """
            ),
            id="stack",
        ),
        pytest.param(
            textwrap.dedent(
                """
                from fastapi import FastAPI, HTTPException

                app = FastAPI()


                @app.get("/", responses={"400": {"description": "Bad Request"}})
                def home():
                    raise HTTPException(status_code=400, detail="Bad Request")
                """
            ),
            id="str",
        ),
        pytest.param(
            textwrap.dedent(
                """
                from fastapi import FastAPI, HTTPException

                app = FastAPI()


                @app.get("/", responses={400: {"description": "Bad Request"}})
                def home():
                    raise HTTPException(status_code=400, detail="Bad Request")
                """
            )
        ),
    ),
)
def test_code_without_error(code: str):
    assert_not_error(UndocumentedHTTPException, code)
