from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import ModeloBaseConUsuario

User = get_user_model()

class Estados(models.Model):
    nombre_estado = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre_estado


class Destinos(models.Model):
    nombre_destino = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre_destino


class Equipos(models.Model):
    producto_id = models.ForeignKey('ingresos.Productos', on_delete=models.CASCADE)
    numero_serie = models.CharField(max_length=20, unique=True, null=True, blank=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    observaciones = models.CharField(max_length=100, null=True, blank=True)

    # def __str__(self):
    #     return f"{self.numero_serie}"
    def __str__(self):
        if self.numero_serie:
            return self.numero_serie
        elif self.producto_id:
            return f"{str(self.producto_id)}"
        else:
            return "Equipo sin datos"

class HistorialOrdenes(models.Model):
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Historial de Orden {self.descripcion} - Fecha {self.fecha_modificacion}"


def get_estado_pendiente():
    return Estados.objects.get_or_create(nombre_estado="Pendiente")[0].id


''' modelo anterior Ordenes 
# class Ordenes(models.Model):
    remito_id = models.ForeignKey('ingresos.Remitos', on_delete=models.CASCADE)
    equipo_id = models.ForeignKey(Equipos, on_delete=models.CASCADE)
    # estado_id = models.ForeignKey(Estados, on_delete=models.CASCADE)
    estado_id = models.ForeignKey(Estados, on_delete=models.CASCADE, default=get_estado_pendiente)
    falla_detectada = models.CharField(max_length=50, null=True, blank=True)
    reparacion = models.CharField(max_length=50, null=True, blank=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)
    # usuario_id = models.ForeignKey('usuarios.Usuarios', on_delete=models.CASCADE)
    # editado_por = models.ForeignKey(
    #     'usuarios.Usuarios', on_delete=models.SET_NULL, null=True, blank=True,
    #     related_name='ordenes_editando'
    # )
    orden_activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    modificacion_id = models.ForeignKey(HistorialOrdenes, on_delete=models.CASCADE, null=True, blank=True)
    destino = models.ForeignKey(Destinos, on_delete=models.CASCADE, null=True, blank=True)
    equipo_palletizado = models.BooleanField(default=False)

    def __str__(self):
        return f"Orden {self.id} - Modelo {self.equipo_id.numero_serie} - Estado {self.estado_id.nombre_estado}"

'''

class Ordenes(ModeloBaseConUsuario):  # HEREDA el usuario y el save()
    remito_id = models.ForeignKey('ingresos.Remitos', on_delete=models.CASCADE)
    equipo_id = models.ForeignKey('Equipos', on_delete=models.CASCADE)
    estado_id = models.ForeignKey('Estados', on_delete=models.CASCADE)
    falla_detectada = models.CharField(max_length=50, null=True, blank=True)
    reparacion = models.CharField(max_length=50, null=True, blank=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)

    editado_por = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_editadas'
    )
    palletizado_por = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_palletizadas'
    )

    orden_activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    modificacion_id = models.ForeignKey('HistorialOrdenes', on_delete=models.CASCADE, null=True, blank=True)
    destino = models.ForeignKey('Destinos', on_delete=models.CASCADE, null=True, blank=True)
    equipo_palletizado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        request = getattr(self, "_request", None)

        if request and hasattr(request, 'user'):
            user = request.user

            self.editado_por = user  # siempre se actualiza al editar

            if self.pk:
                original = Ordenes.objects.filter(pk=self.pk).first()
                if original and not original.equipo_palletizado and self.equipo_palletizado:
                    self.palletizado_por = user

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Orden {self.id} - Modelo {self.equipo_id.numero_serie} - Estado {self.estado_id.nombre_estado}"