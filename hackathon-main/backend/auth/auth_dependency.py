from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer#to extract the token from the request
from services.supabase_service import SupabaseService
from services.auth_service import AuthService
from supabase import Client

security = HTTPBearer()
auth_service = AuthService()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = auth_service.verify_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    return user
#we use Depends because we want to protect all the endpoints but we don't wanna verify the token for each endpoint so we make it first in the order

def get_user_supabase_client(credentials: HTTPAuthorizationCredentials = Depends(security), user=Depends(get_current_user))->Client:
    access_token = credentials.credentials
    supabase_service = SupabaseService()
    return supabase_service.get_user_client(access_token)

#user=Depends(get_current_user) - ensures that the user is already authenticated before we construct user-scoped database client