from passlib.context import CryptContext
import cryptocode
import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def encrypt_message(message: str):
    return cryptocode.encrypt(message, config.encryption_secret)

def decrypt_message(message: str):
    return cryptocode.decrypt(message, config.encryption_secret)


    
