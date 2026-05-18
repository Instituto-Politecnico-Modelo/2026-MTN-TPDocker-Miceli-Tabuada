from django.http import JsonResponse
from django.db import connection
import os

def health(request):
    return JsonResponse({"status": "API is running"})

def db_status(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        return JsonResponse({"db_connection": "success", "message": "Database is reachable"})
    except Exception as e:
        return JsonResponse({"db_connection": "failed", "error": str(e)})

# Opcional: Endpoints para /items
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import json

@csrf_exempt
@require_POST
def create_item(request):
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre')
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO items (nombre) VALUES (%s)", [nombre])
        return JsonResponse({"status": "Item created", "nombre": nombre})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@require_GET
def items_list(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM items")
            items = [{"id": row[0], "nombre": row[1], "created_at": row[2]} for row in cursor.fetchall()]
        return JsonResponse({"items": items})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)