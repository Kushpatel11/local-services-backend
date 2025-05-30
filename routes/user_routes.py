from fastapi.security import OAuth2PasswordRequestForm
from schemas.user_schemas import UserCreate, UserProfileUpdate
from sqlalchemy.orm import Session
from fastapi import Depends, Response, status, APIRouter, Security
from core.database import get_db
from crud.crud_user import (
    create_user,
    login_user,
    logout_user,
    update_user_profile,
    user_profile,
)
from dependencies.user_dependencies import get_current_user, oauth2_user_scheme


router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)


@router.post("/login", status_code=status.HTTP_200_OK)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    return login_user(form_data, db)


@router.post(
    "/logout",
    dependencies=[Security(oauth2_user_scheme)],
)
def logout(response: Response, user: dict = Depends(get_current_user)):
    return logout_user(response)


@router.get(
    "/profile",
    status_code=status.HTTP_200_OK,
    dependencies=[Security(oauth2_user_scheme)],
)
def get_profile(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return user_profile(db, user)


@router.put(
    "/profile",
    status_code=status.HTTP_200_OK,
    dependencies=[Security(oauth2_user_scheme)],
)
def update_profile(
    payload: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return update_user_profile(payload, db, current_user)
