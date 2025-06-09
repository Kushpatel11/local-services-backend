from typing import List, Optional
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, Response, status, APIRouter, Security, Query
from sqlalchemy.orm import Session
from schemas.user_schemas import (
    UserCreate,
    UserProfileUpdate,
    ServiceProviderOut,
    UserProfile,
)
from core.database import get_db
from crud.crud_user import (
    create_user,
    get_approved_providers,
    get_provider_by_id,
    login_user,
    logout_user,
    update_user_profile,
    user_profile,
)
from dependencies.user_dependencies import get_current_user, oauth2_user_scheme

router = APIRouter()


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreate,
    summary="Sign up as a new user",
)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    return create_user(user, db)


@router.post("/login", status_code=status.HTTP_200_OK, summary="User login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Log in a user and return a JWT token.
    """
    return login_user(form_data, db)


@router.post(
    "/logout",
    summary="Logout current user",
    dependencies=[Security(oauth2_user_scheme)],
)
def logout(response: Response, user: dict = Depends(get_current_user)):
    """
    Log out the current user (invalidate token on client side).
    """
    return logout_user(response)


@router.get(
    "/profile",
    status_code=status.HTTP_200_OK,
    response_model=UserProfile,
    summary="Get current user profile",
    dependencies=[Security(oauth2_user_scheme)],
)
def get_profile(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Get the profile of the currently authenticated user.
    """
    return user_profile(db, user)


@router.put(
    "/profile",
    status_code=status.HTTP_200_OK,
    response_model=UserProfileUpdate,
    summary="Update current user profile",
    dependencies=[Security(oauth2_user_scheme)],
)
def update_profile(
    payload: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update the profile of the currently authenticated user.
    """
    return update_user_profile(payload, db, current_user)


@router.get(
    "/providers",
    response_model=List[ServiceProviderOut],
    summary="List service providers",
    dependencies=[Security(oauth2_user_scheme)],
)
def list_service_providers(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Records to skip (for pagination)"),
    limit: int = Query(10, ge=1, le=50, description="Records per page (max 50)"),
    city: Optional[str] = Query(None, description="Filter by city"),
    category: Optional[str] = Query(None, description="Filter by service category"),
):
    """
    List approved service providers, with optional filtering and pagination.
    """
    return get_approved_providers(
        db, skip=skip, limit=limit, city=city, category=category
    )


@router.get(
    "/providers/{provider_id}",
    response_model=ServiceProviderOut,
    summary="Get service provider details",
    dependencies=[Security(oauth2_user_scheme)],
)
def get_service_provider(provider_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific service provider by ID.
    """
    return get_provider_by_id(db, provider_id)
