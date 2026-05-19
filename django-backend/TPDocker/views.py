from django.http import JsonResponse
from django.db import connection
from TPDocker.models import Item
import os

def health(request):
    return JsonResponse({"status": "la API esta corriendo! hola bro nashe"})

def db_status(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        return JsonResponse({"db_connection": "exitosa", "status": "La base de datos es accesible"})
    except Exception as e:
        return JsonResponse({"db_connection": "fallido", "status": str(e)})

# Opcional: Endpoints para /items
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import json

@csrf_exempt  # Para simplificar (evita problemas con CSRF)
@require_POST
def create_item(request):
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre')
        Item.objects.create(nombre=nombre)
        return JsonResponse({"status": "Item creado", "nombre": nombre})
    except Exception as e:
        return JsonResponse({"status": "ERROR", "mensaje": str(e)}, status=400)

@require_GET
def items_list(request):
    try:
        items = Item.objects.all().values('id', 'nombre', 'created_at')
        return JsonResponse({"items": list(items)})
    except Exception as e:
        return JsonResponse({"status": "ERROR", "mensaje": str(e)}, status=500)