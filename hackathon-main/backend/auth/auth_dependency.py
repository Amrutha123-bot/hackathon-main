from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer#to extract the token from the request

from services.auth_service import AuthService

security = HTTPBearer()
auth_service = AuthService()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = auth_service.verify_token(credentials.credentials)
    token = credentials.credentials
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    return user
#we use Depends because we want to protect all the endpoints but we don't wanna verify the token for each endpoint so we make it first in the order