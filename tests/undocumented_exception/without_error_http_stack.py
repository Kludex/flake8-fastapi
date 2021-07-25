from fastapi import FastAPI, HTTPException

app = FastAPI()


def raise_here():
    raise HTTPException(status_code=400, detail="Bad Request")


@app.get("/", responses={400: {"description": "Bad Request"}})
def home():
    raise_here()
