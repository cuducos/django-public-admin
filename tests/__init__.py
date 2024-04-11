import django
from django.conf import settings

settings.configure(
    SECRET_KEY="secret",
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.sites",
    ],
)


django.setup()
