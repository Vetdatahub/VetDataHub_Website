import os
from .settings import *
from dotenv import load_dotenv

load_dotenv()
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
ALLOWED_HOSTS = ALLOWED_HOSTS + [os.environ.get("ALLOWED_HOSTS")]

STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]


STATIC_ROOT = "/var/www/sites/production/static"

DO_SPACES_ACCESS_KEY_ID = os.environ.get('DO_SPACES_ACCESS_KEY_ID')
DO_SPACES_SECRET_ACCESS_KEY = os.environ.get('DO_SPACES_SECRET_ACCESS_KEY')
DO_SPACES_BUCKET_NAME = os.environ.get('DO_SPACES_BUCKET_NAME')
DO_SPACES_ENDPOINT_URL = os.environ.get('DO_SPACES_ENDPOINT_URL')
DO_SPACES_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
DO_SPACES_LOCATION = os.environ.get('DO_SPACES_LOCATION')

MEDIA_URL = DO_SPACES_ENDPOINT_URL
STORAGES['default'] = {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage"
    }
