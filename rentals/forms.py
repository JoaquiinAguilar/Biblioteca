from django import forms
from .models import Student, Cubicle, Career

class RentalForm(forms.Form):
    control_number = forms.CharField(label="Número de Control", max_length=20)
    full_name = forms.CharField(label="Nombre Completo", max_length=255)
    career = forms.ModelChoiceField(
        queryset=Career.objects.all(),
        label="Carrera",
        empty_label="Selecciona una carrera",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    requested_duration = forms.IntegerField(label="Duración (minutos)", min_value=60, max_value=360, help_text="Duración en minutos (entre 60 y 360)")

class CubicleForm(forms.ModelForm):
    class Meta:
        model = Cubicle
        fields = ['name', 'capacity', 'status']
        labels = {
            'name': 'Nombre del Cubículo',
            'capacity': 'Capacidad',
            'status': 'Estado',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
