from BubblyEverAfter.settings.common import *

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key")
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.path.join(PROJECT_ROOT_DIR, "db.sqlite3"),}}
