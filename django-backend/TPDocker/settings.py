import os

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

#dominios desde los cuales el servidor aceptará solicitudes HTTP que modifiquen datos
#como put delete y esos
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000"]