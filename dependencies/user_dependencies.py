from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from core.security import verify_access_token
from sqlalchemy.orm import Session
from models import User


oauth2_user_scheme = OAuth2PasswordBearer(
    tokenUrl="user/login", scheme_name="UserOAuth2"
)


def get_current_user(token: str = Depends(oauth2_user_scheme)):
    payload = verify_access_token(token)
    email = payload.get("sub")
    role = payload.get("role")
    print(role)
    if email is None or role is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    if role != "user":
        raise HTTPException(status_code=403, detail="Not authorized as user")
    return payload


def get_user_from_payload(db: Session, payload: dict) -> User:
    user = db.query(User).filter(User.email == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
