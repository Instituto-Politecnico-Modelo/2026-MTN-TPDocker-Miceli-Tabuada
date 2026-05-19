FROM python:3.9

WORKDIR /app
# Copiar el archivo de requisitos
COPY requirements.txt .
# Instalar las dependencias listadas en el archivo de requisitos
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# configuramos variables de entorno aca en vez de pasarlas en `docker run`
ENV DB_HOST=db_TPDocker
ENV DB_NAME=db_tp_docker
ENV DB_USER=alumno26.miceli.francisco
ENV DB_PASSWORD=jxPE3wgLnHu0LpJcwuQmoA==

#comando para iniciar el servidor django
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]