import os
import dj_database_url
from .settings import *
from dotenv import load_dotenv


load_dotenv()
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

DATABASES["default"] = dj_database_url.config(
    default=os.environ.get("DEFAULT_DB_URL"),
    conn_max_age=600,
    conn_health_checks=True,
)
ALLOWED_HOSTS = ["vetdatahub.tech", "www.vetdatahub.tech"]

STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]


STATIC_ROOT = "/var/www/sites/production/static"

AWS_ACCESS_KEY_ID = os.environ.get("DO_SPACES_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("DO_SPACES_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("DO_SPACES_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = os.environ.get("DO_SPACES_ENDPOINT_URL")  # Endpoint URL
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_LOCATION = os.environ.get("DO_SPACES_LOCATION")
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


MEDIA_URL = "/media/"
STORAGES["default"] = {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"}
