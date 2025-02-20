import jwt 
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Request
from fastapi.security import OAuth2PasswordBearer



from settings.settings import get_settings

setting = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")

def create_access_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(hours=8)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, 
                             algorithm=setting.ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, setting.SECRET_KEY,
                              algorithms=[setting.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(status_code=401, detail="Token not found")
    return verify_access_token(token)
