"""Modelos del inventario de Magnus SIS."""

from django.db import models

STOCK_BAJO = 5


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.nombre

    def crear(self) -> None:
        self.save()

    def actualizar(self) -> None:
        self.save()

    def eliminar(self) -> None:
        self.delete()

    def obtener_productos(self) -> list:
        return list(self.productos.all())


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

    # --- Datos derivados que usa la interfaz ---
    @property
    def sku(self) -> str:
        return f'PRD-{self.pk:04d}' if self.pk else '—'

    @property
    def estado(self) -> str:
        if self.cantidad <= 0:
            return 'out'
        if self.cantidad <= STOCK_BAJO:
            return 'low'
        return 'ok'

    @property
    def estado_etiqueta(self) -> str:
        return {'ok': 'Disponible', 'low': 'Stock bajo', 'out': 'Agotado'}[self.estado]

    @property
    def porcentaje_stock(self) -> int:
        return min(100, max(0, self.cantidad * 5))

    # --- Operaciones de negocio ---
    def crear(self) -> None:
        self.save()

    def actualizar(self) -> None:
        self.save()

    def eliminar(self) -> None:
        self.delete()

    def validar_datos(self) -> bool:
        return bool(
            self.nombre.strip()
            and self.categoria_id
            and self.precio is not None and self.precio > 0
            and self.cantidad >= 0
        )

    @staticmethod
    def buscar(termino: str) -> list:
        termino = (termino or '').strip()
        consulta = Producto.objects.select_related('categoria').order_by('-fecha_creacion', '-id')
        if termino:
            consulta = consulta.filter(
                models.Q(nombre__icontains=termino)
                | models.Q(descripcion__icontains=termino)
            )
        return list(consulta)
