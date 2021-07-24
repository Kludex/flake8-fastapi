from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/", status_code=204)
def home():
    return Response(status_code=204)
