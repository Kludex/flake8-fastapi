<h1 align="center">
    <strong>flake8-fastapi</strong>
</h1>
<p align="center">
    <a href="https://github.com/Kludex/flake8-fastapi" target="_blank">
        <img src="https://img.shields.io/github/last-commit/Kludex/flake8-fastapi" alt="Latest Commit">
    </a>
        <img src="https://img.shields.io/github/workflow/status/Kludex/flake8-fastapi/Test">
        <img src="https://img.shields.io/codecov/c/github/Kludex/flake8-fastapi">
    <br />
    <a href="https://pypi.org/project/flake8-fastapi" target="_blank">
        <img src="https://img.shields.io/pypi/v/flake8-fastapi" alt="Package version">
    </a>
    <img src="https://img.shields.io/pypi/pyversions/flake8-fastapi">
    <img src="https://img.shields.io/github/license/Kludex/flake8-fastapi">
</p>

A [flake8](https://flake8.pycqa.org/en/latest/index.html) plugin that helps you avoid simple FastAPI mistakes.

## Installation

First, install the package:

``` bash
pip install flake8-fastapi
```

Then, check if the plugin is installed using `flake8`:

``` bash
$ flake8 --version
3.9.2 (flake8-fastapi: 0.2.0, flake8-pytest-style: 1.4.2, mccabe: 0.6.1, pycodestyle: 2.7.0, pyflakes: 2.3.1) CPython 3.8.11 on Linux
```

## Rules

### Route Decorator Error (CF001)

Developers that were used to [flask](https://flask.palletsprojects.com/en/2.0.x/) can be persuaded or want to use the same pattern in FastAPI:

```python
from fastapi import FastAPI

app = FastAPI()


@app.route("/", methods=["GET"])
def home():
    return "Hello world!"
```

But on FastAPI, we have a simpler way to define this (and is the most known way to create endpoints):

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return "Hello world!"
```

### Route Prefix Error (CF002)

On old FastAPI versions, we were able to add a prefix only on the `include_router` method:

```python
from fastapi import APIRouter, FastAPI

router = APIRouter()


@router.get("/")
def home():
    ...


app = FastAPI()
app.include_router(router, prefix="/prefix")
```

Now, it's possible to add in the `Router` initialization:

```python
from fastapi import APIRouter, FastAPI

router = APIRouter(prefix="/prefix")


@router.get("/")
def home():
    ...


app = FastAPI()
app.include_router(router)
```


### CORSMiddleware Order (CF008)

There's a [tricky issue](https://github.com/tiangolo/fastapi/issues/1663) about [CORSMiddleware](https://www.starlette.io/middleware/#corsmiddleware) that people are usually unaware. Which is that this middleware should be the last one on the middleware stack. You can read more about it [here](https://github.com/tiangolo/fastapi/issues/1663).

Let's see an example of what doesn't work:

```python
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
```

As you see, the last middleware added is not `CORSMiddleware`, so it will not work as expected. On the other hand, if you change the order, it will:

```python
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
```

## License

This project is licensed under the terms of the MIT license.
