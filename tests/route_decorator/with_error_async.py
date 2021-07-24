from fastapi import FastAPI

app = FastAPI()


@app.route("/", methods=["GET"])
async def home():
    ...
