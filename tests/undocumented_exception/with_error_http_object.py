from fastapi import FastAPI, HTTPException

app = FastAPI()


class MyClass:
    def raise_here(self):
        raise HTTPException(status_code=400, detail="Bad Request")


@app.get("/")
def home():
    my_object = MyClass()
    my_object.raise_here()
