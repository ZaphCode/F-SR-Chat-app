from fastapi import UploadFile
import cloudinary.uploader
from database.user_model import User
import cloudinary
import config
import time

cloudinary.config( 
  cloud_name = config.cloudinary_db_name, 
  api_key = config.cloudinary_api_key, 
  api_secret = config.cloudinary_secret_key 
)

def upload_profile_img(user_pk: str, file: UploadFile):
    user = User.get(user_pk)
    result = cloudinary.uploader.upload(
      file.file, 
      public_id = f"{file.filename}-{time.time()}",
      folder="users/profile_img",
      unique_filename = True
    )
    user.image_url = result.get('url')
    user.save()
    