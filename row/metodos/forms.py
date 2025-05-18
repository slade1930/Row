from django import forms
from .models import FalsaPosicion, GaussEliminacion, GaussJordan

class FalsaPosicionForm(forms.ModelForm):
    class Meta:
        model = FalsaPosicion
        fields = ['funcion', 'x0', 'x1', 'tolerancia', 'max_iteraciones']
        widgets = {
            'funcion': forms.TextInput(attrs={
                'placeholder': 'x**3 - x - 2',
                'class': 'function-input'
            }),
            'x0': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Ej. 1.0'}),
            'x1': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Ej. 2.0'}),
            'tolerancia': forms.NumberInput(attrs={'step': 'any', 'min': '0', 'value': '0.0001'}),
            'max_iteraciones': forms.NumberInput(attrs={'min': '1', 'value': '100'})
        }
        help_texts = {
            'funcion': 'Use x como variable. Operadores: +, -, *, /, **',
            'tolerancia': 'Precisión deseada para el resultado',
        }

class GaussEliminacionForm(forms.ModelForm):
    class Meta:
        model = GaussEliminacion
        fields = ['matriz_a', 'vector_b']
        widgets = {
            'matriz_a': forms.Textarea(attrs={
                'placeholder': '[[2, 1], [5, 7]]',
                'rows': 4
            }),
            'vector_b': forms.Textarea(attrs={
                'placeholder': '[11, 13]',
                'rows': 2
            }),
        }

class GaussJordanForm(forms.ModelForm):
    class Meta:
        model = GaussJordan
        fields = ['matriz_a', 'vector_b']
        widgets = {
            'matriz_a': forms.Textarea(attrs={
                'placeholder': '[[2, 1], [5, 7]]',
                'rows': 4
            }),
            'vector_b': forms.Textarea(attrs={
                'placeholder': '[11, 13]',
                'rows': 2
            }),
        }
