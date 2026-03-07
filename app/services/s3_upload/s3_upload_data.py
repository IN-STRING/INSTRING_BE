from app.core.s3.connect_s3 import s3_client
from app.core.config import settings

class S3UploadData:
    def __init__(self):
        self.s3_client = s3_client
        self.BASE_URL = f"https://{settings.S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com"

    def upload_record_song(self, file_path: str, file_name: str) -> str:
        s3_key = f"user_record_songs/{file_name}"
        self.s3_client.upload_file(
            file_path,
            settings.S3_BUCKET_NAME,
            s3_key,
            ExtraArgs={"ContentType": "audio/wav"},
        )
        return f"{self.BASE_URL}/{s3_key}"

    def upload_record_image(self, file_path: str, file_name: str) -> str:
        s3_key = f"user_record_images/{file_name}"
        self.s3_client.upload_file(
            file_path,
            settings.S3_BUCKET_NAME,
            s3_key,
            ExtraArgs={"ContentType": "image/png"},
        )
        return f"{self.BASE_URL}/{s3_key}"

upload_s3 = S3UploadData()