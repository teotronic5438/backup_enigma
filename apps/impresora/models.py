from django.db import models

# Create your models here.
class ConfiguracionImpresora(models.Model):
    nombre = models.CharField(max_length=255)
    fecha_configuracion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
