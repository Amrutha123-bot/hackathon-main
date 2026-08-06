#react - supabase auth - jwt - fastapi middleware - current user - rag service
from services.supabase_service import SupabaseService

class AuthService:

    def __init__(self):
        self.supabase = SupabaseService().get_client()

    def verify_token(self, access_token: str):
        """verify the incoming jwt token"""
        try:
            response = self.supabase.auth.get_user(access_token)
            return response.user

        except Exception:
            return None