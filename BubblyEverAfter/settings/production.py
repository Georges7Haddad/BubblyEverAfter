from BubblyEverAfter.settings.common import *

DEBUG = False
ALLOWED_HOSTS = ["bea.kebbeblaban.com", "0.0.0.0"]
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator", },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]
