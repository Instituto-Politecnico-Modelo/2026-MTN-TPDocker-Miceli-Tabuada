from django.db import models

class Item(models.Model):
    nombre = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True) # La fecha se guarda automáticamente al crear el item

    class Meta:
        db_table = 'items'  # Nombre de la tabla en la base de datos