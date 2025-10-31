from django.db import models


# Create your models here.
class Depositos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class StockProductos(models.Model):
    id = models.AutoField(primary_key=True)
    producto_id = models.ForeignKey('ingresos.Productos', on_delete=models.CASCADE)
    deposito_id = models.ForeignKey('stock.Depositos', on_delete=models.CASCADE)
    cantidad_total = models.IntegerField()
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.producto_id} en {self.deposito_id}: {self.cantidad_total}"