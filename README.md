# 🐳 TP Docker — Miceli & Tabuada

> **Stack asignado:** Python + Django
> **Stack extra:** Python + Flask  

---

## 📌 Descripción del proyecto

Este proyecto consiste en dos backends independientes (**Django** y **Flask**) que corren en contenedores Docker y se conectan a una base de datos **MySQL** en un tercer contenedor, todos comunicados a través de una red Docker privada.

Cada backend expone los mismos endpoints:
- `GET /health` — confirma que la API está activa, sin tocar la base de datos
- `GET /db-status` — ejecuta una consulta simple a MySQL y devuelve si la conexión fue exitosa
- `GET /items` — devuelve todos los registros de la tabla `items`
- `POST /items` — crea un nuevo registro en la tabla `items`

---

## 📁 Estructura del repositorio

```
2026-MTN-TPDocker-Miceli-Tabuada/
├── django-backend/        ← Stack asignado (Grupo 5)
│   ├── Dockerfile
│   ├── manage.py
│   ├── requirements.txt
│   └── TPDocker/
│       ├── models.py      ← define la tabla items
│       ├── views.py       ← lógica de los endpoints
│       ├── urls.py        ← rutas
│       ├── settings.py    ← configuración general
│       └── migrations/    ← historial de cambios en la BD
│
├── flask-backend/         ← Stack extra (recuperatorio)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py             ← toda la app en un solo archivo
│
└── README.md              ← esta documentación
```

---

## 🧠 Concepto clave: redes en Docker

Los contenedores dentro de una red Docker se comunican entre sí usando el
**nombre del contenedor** como hostname. Pero desde afuera (tu PC, Workbench,
el navegador) **no podés acceder** a menos que el puerto esté expuesto con `-p`.

```
Lo que se expone
├── localhost:3307  →  db_TPDocker (MySQL en Docker)   ✅ expuesto con -p 3307:3306
├── localhost:8000  →  django_app_TPDocker              ✅ expuesto con -p 8000:8000
└── localhost:5000  →  flask_app_TPDocker               ✅ expuesto con -p 5000:5000

Red Docker interna (redTpDocker) - zona privada
├── db_TPDocker           →  escucha en puerto 3306
├── django_app_TPDocker   →  se conecta a db_TPDocker:3306 ✅
└── flask_app_TPDocker    →  se conecta a db_TPDocker:3306 ✅
```

> ⚠️ El puerto 3306 ya está ocupado por el MySQL local
> por eso mapeamos el contenedor MySQL al puerto **3307** en nuestra PC.

---

## 🚀 Setup desde cero

### 1. Clonar el repositorio

```bash
git clone https://github.com/fmicelii/2026-MTN-TPDocker-Miceli-Tabuada.git
cd 2026-MTN-TPDocker-Miceli-Tabuada
```

### 2. Crear la red Docker

```bash
docker network create redTpDocker
```

### 3. Crear el contenedor de MySQL

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

> ⏳ esperar ~10 segundos a que MySQL termine de iniciar antes del siguiente paso.

### 4.a. Buildear Django

```bash
docker build -t django-backend ./django-backend
```

### 4.b. levantar Django

```bash
docker run \
  --name django_app_TPDocker \
  --network redTpDocker \
  -e DB_HOST=db_TPDocker \
  -e DB_NAME=db_tp_docker \
  -e DB_USER=alumno26.miceli.francisco \
  -e DB_PASSWORD=jxPE3wgLnHu0LpJcwuQmoA== \
  -p 8000:8000 \
  -d \
  django-backend
```

> Al iniciar, Django corre automáticamente `makemigrations` + `migrate`
> y crea la tabla `items` en MySQL sin intervención manual.

### 5.a. Buildear Flask

```bash
docker build -t flask-backend ./flask-backend
```

### 5.b. levantar Flask

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

> Flask crea la tabla `items` automáticamente con `CREATE TABLE IF NOT EXISTS`
> al arrancar la app, sin necesidad de migraciones.

---

## ✅ Verificar que todo funciona

### Django (puerto 8000)

```bash
curl http://localhost:8000/health/
# → {"status": "la API esta corriendo! hola bro nashe"}

curl http://localhost:8000/db-status/
# → {"db_connection": "exitosa", "status": "La base de datos es accesible"}

curl http://localhost:8000/items/
# → {"items": [...]}

curl -X POST http://localhost:8000/items/create/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "item desde django"}'
```

### Flask (puerto 5000)

```bash
curl http://localhost:5000/health
# → {"status": "API Flask corriendo! hola bro nashe"}

curl http://localhost:5000/db-status
# → {"db_connection": "exitosa", "db_time": "2026-05-19 ..."}

curl http://localhost:5000/items
# → {"items": [...]}

curl -X POST http://localhost:5000/items \
  -H "Content-Type: application/json" \
  -d '{"nombre": "item desde flask"}'
```

---

## 🗄️ Ver la base de datos con MySQL Workbench

| Campo    | Valor                      |
|----------|----------------------------|
| Host     | `127.0.0.1`                |
| Port     | `3307`                     |
| User     | `root`                     |
| Password | depende la compu           |

> La base de datos se llama **`db_tp_docker`** y la tabla principal es **`items`**.  
> Workbench es solo para visualizar — la base y las tablas las crea Docker solo.

---

## 🔄 Uso diario (contenedores ya creados)

### Detener todo

```bash
docker stop flask_app_TPDocker
docker stop django_app_TPDocker
docker stop db_TPDocker
```

### Levantar todo

```bash
docker start db_TPDocker
docker start django_app_TPDocker
docker start flask_app_TPDocker
```

---

## 🛠️ Comandos útiles para debuggear

```bash
# Ver logs de Django
docker logs django_app_TPDocker

# Ver logs de Flask
docker logs flask_app_TPDocker

# Ver logs en tiempo real (Ctrl+C para salir)
docker logs -f flask_app_TPDocker

# Entrar a MySQL directamente desde terminal
docker exec -it db_TPDocker mysql -u root -pjxPE3wgLnHu0LpJcwuQmoA==
```

Una vez dentro de MySQL:
```sql
USE db_tp_docker;
SHOW TABLES;
SELECT * FROM items;
```

---

## ⚖️ Comparación: Django vs Flask

| | **Django** | **Flask** |
|---|---|---|
| **Tipo** | Framework completo ("batteries included") | Microframework minimalista |
| **Archivos para este TP** | `models.py`, `views.py`, `urls.py`, `settings.py`, `migrations/` | Un solo `app.py` |
| **ORM** | ✅ Incluido (maneja la BD con clases Python) | ❌ No incluye (SQL manual o librería externa) |
| **Migraciones** | ✅ `makemigrations` + `migrate` automático | ❌ Manual con `CREATE TABLE IF NOT EXISTS` |
| **Rutas** | Definidas en `urls.py` separado | Definidas con `@app.route()` encima de cada función |
| **Curva de aprendizaje** | Mayor (más conceptos, más estructura) | Menor (más directo y simple) |
| **Ideal para** | Apps grandes con muchos modelos y lógica | APIs pequeñas, prototipos, microservicios |
| **Puerto por convención** | 8000 | 5000 |
| **Líneas de código para este TP** | ~80 líneas distribuidas en 4 archivos | ~70 líneas en 1 archivo |

### ¿Cuándo usar cada uno?

**Elegí Django si:**
- La app tiene muchos modelos de base de datos relacionados
- Necesitás panel admin, autenticación, permisos
- El equipo es grande y querés estructura forzada

**Elegí Flask si:**
- Es una API simple o un microservicio
- Querés control total sobre cada decisión
- El equipo es chico o es un prototipo rápido

---

## 📌 Datos del grupo

| | |
|---|---|
| **Integrantes** | Miceli, Tabuada |
| **Stack asignado** | Python + Django |
| **Stack extra** | Python + Flask |
| **Curso** | 4° CSTC |
