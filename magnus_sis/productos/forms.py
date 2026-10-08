"""Formularios iniciales. Las validaciones de negocio están pendientes."""

from django import forms

from .models import Categoria, Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'categoria', 'precio', 'cantidad']

    def clean(self) -> dict:
        # Pendiente: nombre/categoría obligatorios, precio > 0, cantidad >= 0.
        return super().clean()


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
