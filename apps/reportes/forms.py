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

class ReporteOrdenesForm(forms.Form):
    ESTADOS = [
        ('pendiente', 'Pendientes'),
        ('revisado', 'Revisadas'),
        ('palletizado', 'Palletizadas'),
    ]
    estado = forms.ChoiceField(choices=ESTADOS)
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    incluir_inactivas = forms.BooleanField(required=False, initial=False)
