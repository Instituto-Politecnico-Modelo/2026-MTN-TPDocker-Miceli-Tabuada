#usar  la imagen de python oficial, todo se ejecuta sobre esta imagen
FROM python:3.9

#directorio de trabajo dentro del contenedor
WORKDIR /app


# Instalar las dependencias listadas en el archivo de requisitos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copia todo el codigo del proyecto al contenedor
COPY . .

# configuramos VARIABLES DE ENTORNO aca en vez de pasarlas en `docker run`
ENV DB_HOST=db_TPDocker
ENV DB_NAME=db_tp_docker
ENV DB_USER=alumno26.miceli.francisco
ENV DB_PASSWORD=jxPE3wgLnHu0LpJcwuQmoA==

#comando para iniciar el servidor django
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
#makemigrations detecta cambios en models ycrea archivos de migracion. 
#migrate aplica las migraciones.
#levanta servidor django en 8000.