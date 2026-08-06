from supabase import create_client, Client
from config.settings import (SUPABASE_URL, SUPABASE_SERVICE_KEY)

class SupabaseService:

    def __init__(self):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

    def get_client(self):
        return self.client