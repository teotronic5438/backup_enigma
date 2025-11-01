from django.db import models

class ConfiguracionImpresora(models.Model):
    nombre = models.CharField(max_length=255)
    fecha_configuracion = models.DateTimeField(auto_now=True)
    
    # Campos opcionales para configuración avanzada
    ancho_etiqueta = models.IntegerField(default=200, blank=True, null=True)
    alto_etiqueta = models.IntegerField(default=100, blank=True, null=True)
    densidad = models.IntegerField(default=8, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Configuración de Impresora"
        verbose_name_plural = "Configuraciones de Impresoras"