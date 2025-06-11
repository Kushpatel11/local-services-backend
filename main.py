# main.py

from fastapi import FastAPI
from core.database import database
from routes.user_routes import router as user_router
from routes.provider_routes import router as provider_router
from routes.booking_routes import router as booking_router
from routes.admin_routes import router as admin_router
from routes.public_routes import router as public_router
from routes.service_routes import router as service_router
from routes.forgot_password import router as forgot_password_router
from routes.service_ratings_routes import router as ratings_router
from fastapi.openapi.utils import get_openapi


app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Local Services Booking API",
        version="1.0.0",
        description="API with user,admin and provider login flows",
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
        "ProviderOAuth2": {
            "type": "oauth2",
            "flows": {"password": {"tokenUrl": "/provider/login", "scopes": {}}},
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
app.include_router(booking_router, prefix="/user", tags=["User"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(public_router, prefix="/public", tags=["Public"])
app.include_router(service_router, prefix="/provider", tags=["Provider"])
app.include_router(forgot_password_router, tags=["OTP"])
app.include_router(ratings_router, prefix="/public/services", tags=["Service Reviews"])
