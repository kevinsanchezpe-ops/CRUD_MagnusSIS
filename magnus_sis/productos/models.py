"""Modelos iniciales del inventario; las operaciones de negocio quedan pendientes."""

from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.nombre

    def crear(self) -> None:
        pass

    def actualizar(self) -> None:
        pass

    def eliminar(self) -> None:
        pass

    def obtener_productos(self) -> list:
        return []


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name='productos'
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.nombre

    def crear(self) -> None:
        pass

    def actualizar(self) -> None:
        pass

    def eliminar(self) -> None:
        pass

    def validar_datos(self) -> bool:
        return False

    @staticmethod
    def buscar(termino: str) -> list:
        return []
