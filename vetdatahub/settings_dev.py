from  .settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    "jnodq38ru2rf3ufif3dp occ9ucn8m238nucc921c-_u%!6^k%&5*o5peu+27%w3fiamx_&%gd1l7!c!q0i((jzhh9)q"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "static/"


STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
MEDIA_URL = "media/"
MEDIA_ROOT = "/media/"

