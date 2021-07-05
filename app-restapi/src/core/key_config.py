import os


class DatabaseEnv:
    """Sistem değişkenlerine eklenen verilerden veri alır."""
    NAME = os.getenv('POSTGRES_DB')
    USER = os.getenv('POSTGRES_USER')
    PASSWORD = os.getenv('POSTGRES_PASSWORD')
    HOST = os.getenv('DATABASE_HOST')
    PORT = os.getenv('DATABASE_PORT')


class SecretsEnv:
    """Sistem değişkenlerine eklenen SECRET_KEY verisini alır."""
    SECRET_KEY = os.getenv('SECRET_KEY')


class DebugEnv:
    DEDUG = int(os.getenv('DEBUG', 0))


class EpostaEnv:
    """.ENV Dosyası ile yüklenen sistem değişkenlerinden EPOSTA Ayarlarını alır..."""
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'seninepostaadresin')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'sifreniyaz')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_USE_TLS = int(os.getenv('EMAIL_USE_TLS', 1))
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'Klikya eCommerce <mailgonderen@gmail.com>')
    BASE_URL = os.getenv('BASE_URL', '127.0.0.1:8000')



class CeleryEnv:
    CELERY_BROKER = os.getenv('CELERY_BROKER', 'redis://redis:6379/0')
    CELERY_BACKEND = os.getenv('CELERY_BACKEND', 'redis://redis:6379/0')


class AllowedHostEnv:
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')

class CustomRedirectEnv:
    APP_SCHEME = os.getenv('APP_SCHEME', '')
    FRONTEND_URL = os.getenv('FRONTEND_URL', '')


class Internationalization:
    LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'tr')
    TIME_ZONE = os.getenv('TIME_ZONE', 'Europe/Istanbul')


class FolderRoots:
    """FolderRoots."""

    def get_template_dirs(base_dir):
        return [os.path.join(base_dir, 'templates'),]

    def get_media_root(base_dir):
        return os.path.join(os.path.dirname(base_dir), "static_cdn", "media_root")

    def get_static_root(base_dir):
        return os.path.join(os.path.dirname(base_dir), "static_cdn", "static_root")

    def get_protected_root(base_dir):
        return os.path.join(os.path.dirname(base_dir), "static_cdn", "protected_media")

    def get_staticfiles_root(base_dir):
        return os.path.join(base_dir, "static_webapp")
