from django.contrib import admin
from .models import Usuarios, Roles

# Register your models here.
# admin.site.register(Usuarios)

# Register your models here.
admin.site.register(Usuarios)
admin.site.register(Roles)


"""
@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'nombre_usuario', 'rol', 'activo')
    search_fields = ('nombre', 'apellido', 'nombre_usuario')
    list_filter = ('rol', 'activo')


# admin.site.register(Roles)
@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    list_filter = ('nombre',)

"""