# main.py

from fastapi import FastAPI
from core.database import database
from routes.user_routes import router as user_router


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
def read_root():
    return {"message": "Hello, database connected!"}


app.include_router(user_router, prefix="/user", tags=["User"])
# app.include_router(admin_router, prefix="/admin", tags=["Admin"])
# app.include_router(service_provider_router, prefix="/servant", tags=["Servant"])
