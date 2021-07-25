from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def home():
    raise HTTPException(400, detail="Bad Request")
