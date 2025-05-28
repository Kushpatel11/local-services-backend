# main.py

from fastapi import FastAPI
from core.database import database
from routes.user_routes import router as user_router
from routes.provider_routes import router as provider_router
from routes.booking_routes import router as booking_router


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
app.include_router(provider_router, prefix="/provider", tags=["Provider"])
app.include_router(booking_router, prefix="/bookings", tags=["Bookings"])
# app.include_router(admin_router, prefix="/admin", tags=["Admin"])
# app.include_router(service_provider_router, prefix="/servant", tags=["Servant"])
