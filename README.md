<h1 align="center">
    <strong>flake8-fastapi</strong>
</h1>
<p align="center">
    <a href="https://github.com/Kludex/flake8-fastapi" target="_blank">
        <img src="https://img.shields.io/github/last-commit/Kludex/flake8-fastapi" alt="Latest Commit">
    </a>
    <a href="https://github.com/Kludex/flake8-fastapi/actions/workflows/test.yml" target="_blank">
        <img src="https://github.com/Kludex/flake8-fastapi/actions/workflows/test.yml/badge.svg" alt="Test workflow action">
    </a>
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
6.0.0 (flake8-fastapi: 0.7.0, mccabe: 0.7.0, pycodestyle: 2.10.0, pyflakes: 3.0.1) CPython 3.8.11 on Linux
```

## Rules

<!-- prettier-ignore-start -->
  - [CF001 - Route Decorator Error](#cf001---route-decorator-error)
  - [CF002 - Router Prefix Error](#cf002---router-prefix-error)
  - [CF008 - CORSMiddleware Order](#cf008---corsmiddleware-order)
  - [CF009 - Undocumented HTTPException](#cf009---undocumented-httpexception)
  - [CF011 - No Content Response](#cf011---no-content-response)
<!-- prettier-ignore-end -->

### CF001 - Route Decorator Error

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

### CF002 - Router Prefix Error

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


### CF008 - CORSMiddleware Order

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

### CF009 - Undocumented HTTPException

Currently, there's no automatic solution to document the `HTTPException`s, besides the experimental package [`fastapi-responses`](https://github.com/Kludex/fastapi-responses).

For that reason, it's easy to forget the documentation, and have a lot of undocumented endpoints. Let's see an example:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def home():
    raise HTTPException(status_code=400, detail="Bad Request")
```

The above endpoint doesn't have a `responses` field, even if it's clear that the response will have a `400` status code.

### CF011 - No Content Response

Currently, if you try to send a response with no content (204), FastAPI will send a 204 status with a non-empty body.
It will send a body content-length being 4 bytes.

You can verify this statement running the following code:

```python
# main.py
from fastapi import FastAPI

app = FastAPI()


@app.get("/", status_code=204)
def home():
    ...
```

Now feel free to run with your favorite server implementation:

```bash
uvicorn main:app
```

Then use curl or any other tool to send a request:

```bash
$ curl localhost:8000
*   Trying 127.0.0.1:8000...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 8000 (#0)
> GET / HTTP/1.1
> Host: localhost:8000
> User-Agent: curl/7.68.0
> Accept: */*
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 204 No Content
< date: Sat, 24 Jul 2021 19:21:24 GMT
< server: uvicorn
< content-length: 4
< content-type: application/json
<
* Connection #0 to host localhost left intact
```

This goes against the [RFC](https://tools.ietf.org/html/rfc7231#section-6.3.5), which specifies that a 204 response should have no body.

## License

This project is licensed under the terms of the MIT license.
