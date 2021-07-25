from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/", responses={400: {"description": "Bad Request"}})
def home():
    raise HTTPException(400, detail="Bad Request")
