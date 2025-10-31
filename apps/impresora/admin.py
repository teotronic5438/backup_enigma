from django.contrib import admin
from .models import ConfiguracionImpresora

@admin.register(ConfiguracionImpresora)
class ConfiguracionImpresoraAdmin(admin.ModelAdmin):
    list_display = ("nombre", "fecha_configuracion")
    ordering = ("-fecha_configuracion",)
    search_fields = ("nombre",)
