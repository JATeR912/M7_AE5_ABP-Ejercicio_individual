from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100, db_index=True)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    disponible = models.BooleanField()

    def __str__(self):
        return f"Producto:{self.nombre} - Precio:{self.precio} - Disponible:{self.disponible}"
