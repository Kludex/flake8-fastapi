from fastapi import FastAPI, HTTPException

app = FastAPI()


def raise_here():
    raise HTTPException(status_code=400, detail="Bad Request")


@app.get("/")
def home():
    raise_here()
