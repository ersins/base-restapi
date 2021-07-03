# Yeni uygulamaları bu repodan oluşturuyorum.

### app/.env dosyası

DEBUG=1
SECRET_KEY=
ALLOWED_HOSTS=0.0.0.0 localhost 127.0.0.1

CELERY_BROKER=redis://redis:6379/0
CELERY_BACKEND=redis://redis:6379/0

EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_PORT=587
EMAIL_USE_TLS=1
DEFAULT_FROM_EMAIL=
BASE_URL=127.0.0.1:8000

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE=postgres


### app/.env.db dosyası

POSTGRES_USER=dbuser
POSTGRES_PASSWORD=gizlisifre
POSTGRES_DB=base_db

### app/.env.prod dosyası

DEBUG=1
SECRET_KEY=
ALLOWED_HOSTS=0.0.0.0 localhost 127.0.0.1

CELERY_BROKER=redis://redis:6379/0
CELERY_BACKEND=redis://redis:6379/0

EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_PORT=587
EMAIL_USE_TLS=1
DEFAULT_FROM_EMAIL=
BASE_URL=127.0.0.1:8000

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE=postgres

### app/.env.db.prod dosyası

POSTGRES_USER=dbuser
POSTGRES_PASSWORD=gizlisifre
POSTGRES_DB=base_db


## Django uygulaması SECRET_KEY nasıl oluşturulu

from django.core.management.utils import get_random_secret_key

print(get_random_secret_key())

import secrets

length = 50
chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
secret_key = ''.join(secrets.choice(chars) for i in range(length))
print(secret_key)
