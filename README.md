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


## License

This project is licensed under the terms of the MIT license.
