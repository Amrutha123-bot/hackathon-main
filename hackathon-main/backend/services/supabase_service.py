from supabase import create_client, Client
from supabase.client import ClientOptions
from config.settings import (SUPABASE_URL, SUPABASE_SERVICE_KEY, SUPABASE_ANON_KEY)

class SupabaseService:

    def __init__(self):
        #server side client not exposed to the frontend
        self.admin_client: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY, options=ClientOptions(auto_refresh_token=False, persist_session=False))

    def get_client(self)->Client:
        """service side client for options require server-side privilege"""
        return self.admin_client

    def get_user_client(self, access_token: str)-> Client:
        """create supabase client whose requests are performed on behalf of the authenticated user"""
        client: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY, options=ClientOptions(auto_refresh_token=False, persist_session=False))        
        client.postgrest.auth(access_token)
        return client

    #now we have created 2 clients - the admin and the user with diff supabase keys 