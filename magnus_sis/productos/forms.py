"""Formularios con las validaciones de negocio del inventario."""

from django import forms

from .models import Categoria, Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'categoria', 'precio', 'cantidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.order_by('nombre')

    def clean_nombre(self) -> str:
        nombre = self.cleaned_data['nombre'].strip()
        if not nombre:
            raise forms.ValidationError('El nombre del producto es obligatorio.')
        return nombre

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio is None or precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor que cero.')
        return precio

    def clean_cantidad(self) -> int:
        cantidad = self.cleaned_data['cantidad']
        if cantidad is None or cantidad < 0:
            raise forms.ValidationError('La cantidad no puede ser negativa.')
        return cantidad


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

    def clean_nombre(self) -> str:
        nombre = self.cleaned_data['nombre'].strip()
        if not nombre:
            raise forms.ValidationError('El nombre de la categoría es obligatorio.')
        repetida = Categoria.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:
            repetida = repetida.exclude(pk=self.instance.pk)
        if repetida.exists():
            raise forms.ValidationError('Ya existe una categoría con ese nombre.')
        return nombre
