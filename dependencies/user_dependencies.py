from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from core.security import verify_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    return payload
