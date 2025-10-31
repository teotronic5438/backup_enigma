# apps/despachos/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def replace_chars(value, arg):
    """
    Reemplaza todas las ocurrencias de una subcadena (old_value) por otra (new_value).
    Uso: {{ valor|replace_chars:"old_value:new_value" }}
    Ejemplo: {{ "Hola Mundo"|replace_chars:" :-" }}  # Salida: Hola-Mundo
    """
    if not isinstance(value, str):
        return value
    try:
        old_value, new_value = arg.split(':')
    except ValueError:
        return value
    return value.replace(old_value, new_value)