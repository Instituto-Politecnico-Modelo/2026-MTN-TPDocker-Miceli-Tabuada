FROM python:3.9

WORKDIR /app

# Copiamos e instalamos dependencias primero
# (Docker cachea esta capa si requirements.txt no cambió → builds más rápidos)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Variables de entorno con valores por defecto
# (se pueden sobreescribir con -e al hacer docker run)
ENV DB_HOST=db_TPDocker
ENV DB_NAME=db_tp_docker
ENV DB_USER=alumno26.miceli.francisco
ENV DB_PASSWORD=jxPE3wgLnHu0LpJcwuQmoA==

# Flask usa el puerto 5000 por convención (Django usaba 8000)
EXPOSE 5000

# A diferencia de Django, Flask no necesita makemigrations ni migrate
# porque nosotros creamos la tabla directamente con SQL en init_db()
CMD ["python", "app.py"]