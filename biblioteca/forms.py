from django import forms
from .models import Autor, Libro, Prestamo

# FORMULARIO PARA AGREGAR EDITAR AUTORES
class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'biografia']


# FORMULARIO PARA AGREGAR EDITAR LIBROS
class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['nombre', 'genero_musical', 'descripcion', 'autor']


# FORMULARIO PARA REGISTRAR PRÉSTAMOS
class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['nombre_lector', 'fecha_prestamo', 'fecha_devolucion', 'libro']
        widgets ={
            'fecha_prestamo': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_devolucion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }