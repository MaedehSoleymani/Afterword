from .base import *
from gitignore.email_config import (
    email_host_pass,
    email_host_user,
    default_from_email
)

from gitignore.secret_key import secret_key

SECRET_KEY = secret_key

DEBUG = True

ALLOWED_HOSTS = []

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = email_host_user
EMAIL_HOST_PASSWORD = email_host_pass
DEFAULT_FROM_EMAIL = default_from_email

#Celery Configuration
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'