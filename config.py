from dotenv import load_dotenv
from os import getenv

load_dotenv()

session_secret = str(getenv('SESSION_SECRET', "super_secret"))
redis_db_host = str(getenv('REDIS_DB_HOST', "localhost"))
redis_db_port = int(getenv('REDIS_DB_PORT', 6300))
redis_db_password = str(getenv('REDIS_DB_PASSWORD', None))
cloudinary_db_name=str(getenv('CLOUDINARY_DB_NAME', None))
cloudinary_api_key=str(getenv('CLOUDINARY_API_KEY', None))
cloudinary_secret_key=str(getenv('CLOUDINARY_SECRET_KEY', None))