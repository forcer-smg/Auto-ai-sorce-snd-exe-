"""
Supabase Configuration for Auto_Punch IDE
"""
import os
from supabase import create_client, Client

# Supabase Configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')  # anon key
SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY', '')  # service_role key

def get_supabase_client(use_service_key=False) -> Client:
    """Get Supabase client"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase URL and KEY must be set in environment variables")
    
    key = SUPABASE_SERVICE_KEY if use_service_key else SUPABASE_KEY
    return create_client(SUPABASE_URL, key)

# Example usage in your app:
# supabase = get_supabase_client()
# result = supabase.table('your_table').select('*').execute()


