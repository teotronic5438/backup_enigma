# utils/models.py o en un archivo shared como core/models.py
from django.db import models
from django.contrib.auth import get_user_model

class ModeloBaseConUsuario(models.Model):
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        editable=False,
        related_name="%(class)s_creadas"
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        request = getattr(self, "_request", None)
        if request and hasattr(request, 'user'):
            if not self.usuario_id:
                self.usuario = request.user
        super().save(*args, **kwargs)
