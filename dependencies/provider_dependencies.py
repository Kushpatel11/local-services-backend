from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from core.security import verify_access_token


oauth2_provider_scheme = OAuth2PasswordBearer(
    tokenUrl="provider/login", scheme_name="ProviderOAuth2"
)


def get_current_provider(token: str = Depends(oauth2_provider_scheme)):
    payload = verify_access_token(token)
    email = payload.get("sub")
    role = payload.get("role")
    print(role)
    if email is None or role is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    if role != "provider":
        raise HTTPException(status_code=403, detail="Not authorized as provider")
    return payload
