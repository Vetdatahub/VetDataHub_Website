import os
from .settings import *
from dotenv import load_dotenv


load_dotenv(os.path.join(BASE_DIR, '.env'))
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
ALLOWED_HOSTS = ALLOWED_HOSTS + ["pythonanywhere.com"]

STATIC_URL = "static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "/static")]
MEDIA_URL = "media/"
MEDIA_ROOT = "/media/"

STATIC_ROOT = "/var/www/sites/production/static"
