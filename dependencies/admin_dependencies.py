from fastapi import Depends, HTTPException
from core.security import verify_access_token
from fastapi.security import OAuth2PasswordBearer


oauth2_admin_scheme = OAuth2PasswordBearer(
    tokenUrl="admin/login", scheme_name="AdminOAuth2"
)


def get_current_admin(token: str = Depends(oauth2_admin_scheme)):
    payload = verify_access_token(token)
    email = payload.get("sub")
    role = payload.get("role")
    if email is None or role is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized as admin")
    return payload
