from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/", status_code=204, response_class=Response)
def home():
    ...
