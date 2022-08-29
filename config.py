from dotenv import load_dotenv
from os import getenv

load_dotenv()

#* Enviroments
node_env = str(getenv("NODE_ENV", "development"))
app_domain = str(getenv("APP_DOMAIN", "localhost:8000"))

#* Encrypt
session_secret = str(getenv('SESSION_SECRET', "super_secret"))
encryption_secret = str(getenv('ENCRYPTION_SECRET', "encryption_super_secret"))

#* Database credentials
redis_db_url = str(getenv('REDIS_DB_URL', "redis://localhost:6300"))
redis_db_password = str(getenv('REDIS_DB_PASSWORD', None))

#* Cloudinary credentials
cloudinary_db_name=str(getenv('CLOUDINARY_DB_NAME', None))
cloudinary_api_key=str(getenv('CLOUDINARY_API_KEY', None))
cloudinary_secret_key=str(getenv('CLOUDINARY_SECRET_KEY', None))