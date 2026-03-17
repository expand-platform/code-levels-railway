from os import getenv
from dataclasses import dataclass

@dataclass
class Dotenv:
    allowed_hosts = getenv("ALLOWED_HOSTS", "*")
    csrf_trusted_origins = getenv("CSRF_TRUSTED_ORIGINS", "http://localhost,http://127.0.0.1")
    django_secret_key = getenv("DJANGO_SECRET_KEY", "")
    django_settings_module = getenv("DJANGO_SETTINGS_MODULE", "code_levels.settings.dev")
    google_auth_client_id = getenv("GOOGLE_AUTH_CLIENT_ID", "")
    google_auth_client_secret = getenv("GOOGLE_AUTH_CLIENT_SECRET", "")
    pgdatabase = getenv("PGDATABASE", "")
    pghost = getenv("PGHOST", "localhost")
    pgpassword = getenv("PGPASSWORD", "")
    pgport = getenv("PGPORT", "5432")
    pguser = getenv("PGUSER", "")
    port = getenv("PORT", "8000")
    drf_secret_key = getenv("DRF_SECRET_KEY", "")
    
    aws_access_key_id = getenv("R2_ACCESS_KEY_ID", "")
    aws_secret_access_key = getenv("R2_SECRET_ACCESS_KEY", "")
    aws_storage_bucket_name = getenv("R2_BUCKET_NAME", "")
    aws_s3_endpoint_url = getenv("R2_ENDPOINT", "")
    aws_s3_custom_domain = getenv("R2_CUSTOM_DOMAIN", "")

dotenv = Dotenv()