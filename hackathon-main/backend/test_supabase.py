from services.supabase_service import SupabaseService
supabase = SupabaseService().get_client()

print("Supabase client created successfully")

response = (supabase.table('documents').select("*").execute())

print("Database connection successful")
print("Documents: ", response.data)