#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
    echo "PostgreSQL bekleniyor..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL başlatıldı"
fi

echo "makemigrations, migrate ve collectstatic işlemleri yapılıyor. "
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
