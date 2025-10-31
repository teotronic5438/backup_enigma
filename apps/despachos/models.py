# apps/despachos/models.py

from django.db import models
from apps.ordenes.models import Ordenes, Destinos, Estados
from apps.ingresos.models import Remitos 
from django.contrib.auth import get_user_model 


from apps.core.models import ModeloBaseConUsuario 

User = get_user_model() 


class Pallet(ModeloBaseConUsuario):
    """
    Modelo para representar un Pallet en el sistema de despachos.
    Un pallet agrupa órdenes para su posterior despacho.
    """
    destino = models.ForeignKey(Destinos, on_delete=models.PROTECT, related_name='pallets_despacho', verbose_name="Destino")
    
    nro_pallet = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="Número de Pallet") 
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Última Modificación")
    nro_viaje = models.CharField(max_length=50, null=True, blank=True, verbose_name="Número de Viaje")
    fecha_despacho = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Despacho")
    
    usuario_despacho = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pallets_despachados_por_usuario',
        verbose_name="Usuario que Despachó"
    )
    
    remito_salida = models.ForeignKey(Remitos, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Remito de Salida")
    
    estado_pallet = models.ForeignKey(Estados, on_delete=models.PROTECT, related_name='pallets_por_estado', null=True, blank=True, verbose_name="Estado del Pallet")

    class Meta:
        verbose_name = "Pallet de Despacho"
        verbose_name_plural = "Pallets de Despacho"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Pallet {self.nro_pallet if self.nro_pallet else self.id} - Destino: {self.destino.nombre_destino if self.destino else 'N/A'}"

    def save(self, *args, **kwargs):
        request = getattr(self, "_request", None)

        if request and hasattr(request, 'user'):

            if self.estado_pallet and self.estado_pallet.nombre_estado.lower() == 'despachado':
                self.usuario_despacho = request.user

        super().save(*args, **kwargs)

class DetallePallet(models.Model):
    """
    Modelo para los detalles de un Pallet, conectando Pallets con Órdenes.
    """
    pallet = models.ForeignKey(Pallet, on_delete=models.CASCADE, related_name='detalles', verbose_name="Pallet")
    orden_id = models.OneToOneField(Ordenes, on_delete=models.CASCADE, related_name='detalle_pallet_asociado', verbose_name="Orden") 
    
    class Meta:
        verbose_name = "Detalle de Pallet"
        verbose_name_plural = "Detalles de Pallet"
        unique_together = ('pallet', 'orden_id')

    def __str__(self):
        return f"Detalle de Pallet {self.pallet.nro_pallet} - Orden {self.orden_id.id}"