# main.py

from fastapi import FastAPI
from core.database import database
from routes.user_routes import router as user_router
from routes.provider_routes import router as provider_router
from routes.booking_routes import router as booking_router
from routes.admin_routes import router as admin_router
from fastapi.openapi.utils import get_openapi


app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Local Services Booking API",
        version="1.0.0",
        description="API with user and admin login flows",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "UserOAuth2": {
            "type": "oauth2",
            "flows": {"password": {"tokenUrl": "/user/login", "scopes": {}}},
        },
        "AdminOAuth2": {
            "type": "oauth2",
            "flows": {"password": {"tokenUrl": "/admin/login", "scopes": {}}},
        },
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


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
app.include_router(booking_router, tags=["Bookings"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
