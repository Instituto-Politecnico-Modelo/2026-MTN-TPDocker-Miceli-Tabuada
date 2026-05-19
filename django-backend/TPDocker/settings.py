import os

# DEBUG debe estar en True porque si no está definido Django lo interpreta como False,
# y con DEBUG=False el servidor no arranca sin una configuración más estricta de seguridad.
DEBUG = True

# Con DEBUG=False Django exige que ALLOWED_HOSTS esté configurado explícitamente,
# de lo contrario lanza un CommandError al iniciar y el contenedor se cierra de inmediato.
ALLOWED_HOSTS = ['*']

SECRET_KEY = 'django-insecure-tpdocker-dev-key-cambiar-en-produccion'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ROOT_URLCONF = 'TPDocker.urls'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'TPDocker',  # Registrar la app para que Django detecte los modelos
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'db_tp_docker'),
        'USER': os.getenv('DB_USER', 'alumno26.miceli.francisco'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'jxPE3wgLnHu0LpJcwuQmoA=='),
        'HOST': os.getenv('DB_HOST', 'db_TPDocker'),
        'PORT': '3306',
    }
}

# dominios desde los cuales el servidor aceptará solicitudes HTTP que modifiquen datos
# como put delete y esos
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000']