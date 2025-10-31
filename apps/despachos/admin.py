# apps/despachos/admin.py

from django.contrib import admin
from .models import Pallet, DetallePallet
from django.utils.html import format_html 
from django.urls import reverse 
class DetallePalletInline(admin.TabularInline):
    model = DetallePallet
    extra = 1 

    fields = ['orden_id', 'get_orden_numero_serie', 'get_orden_modelo', 'get_orden_marca']
    readonly_fields = ['get_orden_numero_serie', 'get_orden_modelo', 'get_orden_marca']

    def get_orden_numero_serie(self, obj):

        return obj.orden_id.equipo_id.numero_serie if obj.orden_id and obj.orden_id.equipo_id else 'N/A'
    get_orden_numero_serie.short_description = 'Nro. Serie Equipo' 

    def get_orden_modelo(self, obj):
        if obj.orden_id and obj.orden_id.equipo_id and obj.orden_id.equipo_id.producto_id:
            return obj.orden_id.equipo_id.producto_id.modelo_id.nombre_modelo if obj.orden_id.equipo_id.producto_id.modelo_id else 'N/A'
        return 'N/A'
    get_orden_modelo.short_description = 'Modelo Equipo'

    def get_orden_marca(self, obj):
        if obj.orden_id and obj.orden_id.equipo_id and obj.orden_id.equipo_id.producto_id:
            return obj.orden_id.equipo_id.producto_id.marca_id.nombre_marca if obj.orden_id.equipo_id.producto_id.marca_id else 'N/A'
        return 'N/A'
    get_orden_marca.short_description = 'Marca Equipo'


@admin.register(Pallet)
class PalletAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nro_pallet', 
        'destino',
        'estado_pallet',
        'fecha_creacion',
        'fecha_despacho',
        'usuario',
        'usuario_despacho',
        'remito_salida',
        'get_cantidad_ordenes',
    )
    search_fields = (
        'nro_pallet',
        'nro_viaje',
        'destino__nombre_destino',
        'estado_pallet__nombre_estado', 
        'usuario__username', 
        'usuario_despacho__username',
        'detalles__orden_id__equipo_id__numero_serie',
    )

    list_filter = (
        'destino',
        'estado_pallet', 
        'fecha_creacion',
        'fecha_despacho',
        'usuario',
        'usuario_despacho',
    )
    inlines = [DetallePalletInline]
    readonly_fields = ['fecha_creacion']


    def get_cantidad_ordenes(self, obj):
        return obj.detalles.count()
    get_cantidad_ordenes.short_description = 'Órdenes' 


@admin.register(DetallePallet)
class DetallePalletAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'pallet',
        'orden_id',
        'get_orden_numero_serie', 
        'get_orden_modelo', 
        'get_orden_marca',
    )
    search_fields = (
        'pallet__nro_pallet',
        'orden_id__id',
        'orden_id__equipo_id__numero_serie', 
        'orden_id__equipo_id__producto_id__modelo_id__nombre_modelo',
        'orden_id__equipo_id__producto_id__marca_id__nombre_marca', 
    )

    list_filter = (
        'pallet__destino',
        'pallet__estado_pallet', 
    )

    def get_orden_numero_serie(self, obj):
        return obj.orden_id.equipo_id.numero_serie if obj.orden_id and obj.orden_id.equipo_id else 'N/A'
    get_orden_numero_serie.short_description = 'Nro. Serie Equipo'

    def get_orden_modelo(self, obj):
        if obj.orden_id and obj.orden_id.equipo_id and obj.orden_id.equipo_id.producto_id:
            return obj.orden_id.equipo_id.producto_id.modelo_id.nombre_modelo if obj.orden_id.equipo_id.producto_id.modelo_id else 'N/A'
        return 'N/A'
    get_orden_modelo.short_description = 'Modelo Equipo'

    def get_orden_marca(self, obj):
        if obj.orden_id and obj.orden_id.equipo_id and obj.orden_id.equipo_id.producto_id:
            return obj.orden_id.equipo_id.producto_id.marca_id.nombre_marca if obj.orden_id.equipo_id.producto_id.marca_id else 'N/A'
        return 'N/A'
    get_orden_marca.short_description = 'Marca Equipo'