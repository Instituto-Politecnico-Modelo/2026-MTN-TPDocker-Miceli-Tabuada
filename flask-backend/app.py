import os
import mysql.connector
from flask import Flask, jsonify, request

# En Django hacías: django-admin startproject / manage.py
# En Flask simplemente creás la app en una línea:
app = Flask(__name__)

# Las credenciales se leen desde variables de entorno (igual que en Django)
DB_CONFIG = {
    'host':     os.getenv('DB_HOST', 'db_TPDocker'),
    'database': os.getenv('DB_NAME', 'db_tp_docker'),
    'user':     os.getenv('DB_USER', 'alumno26.miceli.francisco'),
    'password': os.getenv('DB_PASSWORD', 'jxPE3wgLnHu0LpJcwuQmoA=='),
    'port':     3306,
}

def get_connection():
    """Abre y devuelve una conexión a MySQL."""
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    """Crea la tabla items si no existe. Se llama una vez al iniciar la app."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id         INT AUTO_INCREMENT PRIMARY KEY,
            nombre     VARCHAR(100) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# -------------------------------------------------------------------
# Endpoints
# En Flask los endpoints se definen con el decorador @app.route()
# En Django los definías en urls.py apuntando a funciones en views.py
# Acá la ruta y la función están juntas — más simple y directo
# -------------------------------------------------------------------

@app.route('/health')
def health():
    """GET /health — responde que la API está activa (sin consultar la DB)."""
    return jsonify({"status": "API Flask corriendo! hola bro nashe"})

@app.route('/db-status')
def db_status():
    """GET /db-status — consulta SELECT NOW() y devuelve si la conexión fue exitosa."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT NOW()")
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({"db_connection": "exitosa", "db_time": str(resultado[0])})
    except Exception as e:
        return jsonify({"db_connection": "fallida", "error": str(e)}), 500

@app.route('/items', methods=['GET'])
def items_list():
    """GET /items — devuelve todos los items de la tabla."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)  # dictionary=True → devuelve dicts en vez de tuplas
        cursor.execute("SELECT id, nombre, created_at FROM items")
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        # Convertimos created_at a string porque JSON no sabe serializar datetime
        for item in items:
            item['created_at'] = str(item['created_at'])
        return jsonify({"items": items})
    except Exception as e:
        return jsonify({"status": "ERROR", "mensaje": str(e)}), 500

@app.route('/items', methods=['POST'])
def create_item():
    """POST /items — crea un nuevo item con el nombre recibido en el body JSON."""
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (nombre, created_at) VALUES (%s, NOW())",(data["nombre"],))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "Item creado", "nombre": nombre}), 201
    except Exception as e:
        return jsonify({"status": "ERROR", "mensaje": str(e)}), 400

# -------------------------------------------------------------------
# Arranque de la app
# -------------------------------------------------------------------
if __name__ == '__main__':
    init_db()   # Crea la tabla si no existe
    app.run(host='0.0.0.0', port=5000, debug=True)
