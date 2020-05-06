from BubblyEverAfter.settings.common import *

DEBUG = False
ALLOWED_HOSTS = ["bea.kebbeblaban.com", "0.0.0.0"]
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "fNO4Vpy2pc",
        "HOST": "postgresql.postgresql.svc.cluster.local",
        "PORT": "5432",
        "OPTIONS": {"connect_timeout": 60,},
    }
}
