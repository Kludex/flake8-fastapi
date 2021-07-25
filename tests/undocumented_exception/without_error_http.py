from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/", responses={400: {"description": "Bad Request"}})
def home():
    raise HTTPException(status_code=400, detail="Bad Request")
