# apps/reportes/forms.py
from django import forms

class ReporteFechasForm(forms.Form):
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha inicio"
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha fin"
    )
    incluir_inactivas = forms.BooleanField(
        required=False,
        initial=False,
        label="Incluir desactivadas"
    )

# class ReporteOrdenesForm(forms.Form):
#     ESTADOS = [
#         ('pendiente', 'Pendientes'),
#         ('revisado', 'Revisadas'),
#         ('palletizado', 'Palletizadas'),
#     ]
#     estado = forms.ChoiceField(choices=ESTADOS)
#     fecha_inicio = forms.DateField(
#         widget=forms.DateInput(attrs={'type': 'date'}),
#         required=False
#     )
#     fecha_fin = forms.DateField(
#         widget=forms.DateInput(attrs={'type': 'date'}),
#         required=False
#     )
#     incluir_inactivas = forms.BooleanField(required=False, initial=False)


# apps/reportes/forms.py
from django import forms
from apps.ordenes.models import Ordenes

ESTADOS_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('completado', 'Completado'),
    ('averia', 'Avería'),
    ('destruccion', 'Destrucción'),
]

class OrdenesFiltroForm(forms.Form):
    modelo = forms.CharField(required=False, label="Modelo")
    estado = forms.ChoiceField(choices=[('', 'Todos')] + ESTADOS_CHOICES, required=False)
    tipo_accion = forms.ChoiceField(choices=[('', 'Todos'), ('nuevo','Nuevo'), ('averia','Avería'), ('destruccion','Destrucción')], required=False)
    fecha_inicio = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
