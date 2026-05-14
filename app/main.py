from fastapi import FastAPI
from app.routers import items

app = FastAPI(
    title="Demo FastAPI",
    version="1.0.0",
    description="Proyecto de ejemplo con FastAPI, tests y SonarCloud",
)

app.include_router(items.router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
