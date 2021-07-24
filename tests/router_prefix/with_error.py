from fastapi import APIRouter, FastAPI

router = APIRouter()


@router.get("/")
def home():
    ...


app = FastAPI()
app.include_router(router, prefix="/prefix")
