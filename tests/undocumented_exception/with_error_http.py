from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def home():
    raise HTTPException(status_code=400, detail="Bad Request")
