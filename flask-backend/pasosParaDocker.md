# 🐳 Flask Backend — Miceli & Tabuada

> Stack extra elegido para el recuperatorio: **Python + Flask**

---

## 🧠 Concepto clave: redes en Docker

Los contenedores dentro de una red Docker se comunican entre sí usando el **nombre del contenedor** como hostname. Pero desde afuera (tu PC, Workbench, el navegador) **no podés acceder** a menos que el puerto esté explícitamente expuesto con `-p`.

```
Tu PC
├── localhost:3307  →  db_TPDocker (contenedor)     ✅ (con -p 3307:3306)
└── localhost:5000  →  flask_app_TPDocker            ✅ (con -p 5000:5000)

Red Docker interna (redTpDocker)
├── db_TPDocker            →  escucha en puerto 3306
└── flask_app_TPDocker     →  se conecta a db_TPDocker:3306 ✅
```

> ⚠️ Flask usa el puerto **5000** por convención, a diferencia de Django que usa 8000.

---

## 🚀 Setup desde cero

### 1. Clonar el repositorio *(solo en una PC nueva)*

```bash
git clone https://github.com/fmicelii/2026-MTN-TPDocker-Miceli-Tabuada.git
cd 2026-MTN-TPDocker-Miceli-Tabuada
```

### 2. Crear la red Docker *(si no existe ya)*

```bash
docker network create redTpDocker
```

### 3. Crear el contenedor de MySQL *(si no existe ya)*

> ⚠️ Se usa `-p 3307:3306` y **no** `3306:3306` porque el puerto 3306 ya lo ocupa el MySQL local instalado en la computadora del laboratorio.  
> El formato es: `-p PUERTO_EN_TU_PC:PUERTO_EN_EL_CONTENEDOR`

```bash
docker run \
  --name db_TPDocker \
  -e MYSQL_ROOT_PASSWORD=jxPE3wgLnHu0LpJcwuQmoA== \
  -e MYSQL_DATABASE=db_tp_docker \
  -e MYSQL_USER=alumno26.miceli.francisco \
  -e MYSQL_PASSWORD=jxPE3wgLnHu0LpJcwuQmoA== \
  --network redTpDocker \
  -v mysql_data:/var/lib/mysql \
  -p 3307:3306 \
  -d \
  mysql:8.0
```

> ⏳ Esperá ~10 segundos a que MySQL termine de iniciar antes del siguiente paso.

### 4. Buildear la imagen de Flask

```bash
docker build -t flask-backend ./flask-backend
```

> 🔁 Cada vez que modifiques el código hay que **rebuildar** la imagen con este mismo comando.  
> A diferencia de Django, Flask **no usa migraciones** — crea la tabla `items` directamente
> con `CREATE TABLE IF NOT EXISTS` al arrancar la app.

### 5. Crear el contenedor de Flask

```bash
docker run \
  --name flask_app_TPDocker \
  --network redTpDocker \
  -e DB_HOST=db_TPDocker \
  -e DB_NAME=db_tp_docker \
  -e DB_USER=alumno26.miceli.francisco \
  -e DB_PASSWORD=jxPE3wgLnHu0LpJcwuQmoA== \
  -p 5000:5000 \
  -d \
  flask-backend
```

---

## ✅ Verificar que todo funciona

```bash
# La API responde (sin consultar la BD)
curl http://localhost:5000/health

# La conexión a la base de datos es exitosa
curl http://localhost:5000/db-status

# Lista de items (vacía al principio)
curl http://localhost:5000/items
```

### Crear un item de prueba

```bash
curl -X POST http://localhost:5000/items \
  -H "Content-Type: application/json" \
  -d '{"nombre": "nombre de prueba"}'
```

> 📝 Nota: en Flask el endpoint es `POST /items` (sin `/create/`),
> a diferencia de Django que usa `POST /items/create/`.

---

## 🗄️ Ver la base de datos con MySQL Workbench

| Campo    | Valor                      |
|----------|----------------------------|
| Host     | `127.0.0.1`                |
| Port     | `3307`                     |
| User     | `root`                     |
| Password | `jxPE3wgLnHu0LpJcwuQmoA==` |

> La base de datos se llama **`db_tp_docker`** y la tabla principal es **`items`**.  
> Flask y Django **comparten la misma base de datos y la misma tabla**.

---

## 🔄 Uso diario (contenedores ya creados)

### Levantar

```bash
docker start db_TPDocker
docker start flask_app_TPDocker
```

### Detener

```bash
docker stop flask_app_TPDocker
docker stop db_TPDocker
```

---

## 🛠️ Comandos útiles para debuggear

```bash
# Ver los logs de Flask
docker logs flask_app_TPDocker

# Ver los logs en tiempo real (Ctrl+C para salir)
docker logs -f flask_app_TPDocker

# Entrar a la terminal de MySQL directamente
docker exec -it db_TPDocker mysql -u root -pjxPE3wgLnHu0LpJcwuQmoA==
```

Una vez dentro de MySQL:
```sql
USE db_tp_docker;
SHOW TABLES;
SELECT * FROM items;
```

---

## 🔥 Recrear todo desde cero

```bash
# 1. Parar y eliminar los contenedores
docker stop flask_app_TPDocker db_TPDocker
docker rm flask_app_TPDocker db_TPDocker

# 2. Eliminar la imagen de Flask (para forzar rebuild limpio)
docker rmi flask-backend
```

> 💾 Los datos de MySQL se conservan en el volumen `mysql_data`.  
> Para borrar los volúmenes también:
> ```bash
> docker volume rm mysql_data
> ```
