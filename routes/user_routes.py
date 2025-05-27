from schemas.user_schemas import UserCreate, UserLogin
from sqlalchemy.orm import Session
from fastapi import Depends, status, APIRouter
from core.database import get_db
from crud.crud_user import create_user, login_user, logout_user


router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)


@router.post("/login", status_code=status.HTTP_200_OK)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(user, db)


@router.post("logout")
def logout(response):
    return logout_user(response)
