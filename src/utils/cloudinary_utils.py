# src/utils/cloudinary_utils.py
import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

def upload_to_cloudinary(local_path, folder='videos', resource_type='video'):
    result = cloudinary.uploader.upload(
        local_path,
        folder=folder,
        resource_type=resource_type,
        use_filename=True,
        unique_filename=False,
        overwrite=True
    )
    return result['secure_url']
