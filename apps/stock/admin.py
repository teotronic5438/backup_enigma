from django.contrib import admin

# Register your models here.
# traigo la tabla que quiero registrar
from .models import StockProductos, Depositos

# registro la tabla para que me aparezca en el panel
# admin.site.register(StockProductos)
@admin.register(StockProductos)
class StockProductosAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto_id', 'deposito_id', 'cantidad_total', 'ubicacion', 'precio_unitario')
    search_fields = ('producto_id__marca', 'producto_id__modelo', 'deposito_id__nombre')
    list_filter = ('deposito_id',)

    # def has_add_permission(self, request):
    #     return False



# admin.site.register(Depositos)
@admin.register(Depositos)
class DepositosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    
    # def has_add_permission(self, request):
    #     return False
