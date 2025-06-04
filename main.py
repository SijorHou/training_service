from fastapi import FastAPI
from api.endpoints import router

app = FastAPI(
    title="RL Training Service",
    description="Resolve JSON request body"
)

app.include_router(router, prefix="/api")


