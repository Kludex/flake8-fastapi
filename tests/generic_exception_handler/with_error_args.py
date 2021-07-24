from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

app = FastAPI()


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=200, content="It doesn't work!")


@app.get("/")
async def home():
    raise Exception()
