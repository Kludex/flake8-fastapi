from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

app = FastAPI()


class NewException(Exception):
    ...


@app.exception_handler(NewException)
async def new_exception_handler(request: Request, exc: NewException):
    return JSONResponse(status_code=200, content="It works!")


@app.get("/")
async def home():
    raise NewException()
