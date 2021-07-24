from fastapi import APIRouter, FastAPI

router = APIRouter(prefix="/prefix")


@router.get("/")
def home():
    ...


app = FastAPI()
app.include_router(router)
