from .settings import  *

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
ALLOWED_HOSTS = ALLOWED_HOSTS + ["pythonanywhere.com"]

STATIC_URL = "static/"


STATICFILES_DIRS = [
    BASE_DIR +'/static'
]
MEDIA_URL = "media/"
MEDIA_ROOT = "/media/"


STATIC_ROOT = "/var/www/sites/production/static"
