from django.contrib import admin

# Register your models here.

from .models import Productos, Remitos, RemitoProducto

# admin.site.register(Productos)
@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('id', 'marca', 'modelo')
    search_fields = ('marca', 'descmodelo')
    list_filter = ('marca',)

# admin.site.register(Remitos)
class RemitosAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_ingreso', 'usuario')
    exclude = ('usuario',)  # oculta el campo en el formulario
    list_display = ('numero_remito', 'deposito_id', 'usuario', 'fecha_ingreso')

    def save_model(self, request, obj, form, change):
        if not obj.usuario_id:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Remitos, RemitosAdmin)


admin.site.register(RemitoProducto)


