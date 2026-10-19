from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Producto


class CrudProductosTests(TestCase):
    def setUp(self):
        self.cat = Categoria.objects.create(nombre='Periféricos', descripcion='Teclados y ratones')

    def _producto(self, **kw):
        datos = dict(nombre='Teclado USB', categoria=self.cat, precio=Decimal('45000'), cantidad=20)
        datos.update(kw)
        return Producto.objects.create(**datos)

    def test_paginas_responden(self):
        p = self._producto()
        for nombre, args in [('lista', []), ('crear', []), ('categorias', []), ('categoria_crear', []),
                             ('detalle', [p.pk]), ('editar', [p.pk]), ('eliminar', [p.pk])]:
            with self.subTest(nombre):
                self.assertEqual(self.client.get(reverse(f'productos:{nombre}', args=args)).status_code, 200)

    def test_crear_producto(self):
        r = self.client.post(reverse('productos:crear'), {
            'nombre': 'Mouse', 'descripcion': '', 'categoria': self.cat.pk, 'precio': '25000.50', 'cantidad': '3'})
        self.assertRedirects(r, reverse('productos:lista'))
        self.assertEqual(Producto.objects.get().precio, Decimal('25000.50'))

    def test_validaciones(self):
        r = self.client.post(reverse('productos:crear'), {
            'nombre': '  ', 'categoria': self.cat.pk, 'precio': '0', 'cantidad': '-1'})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Producto.objects.count(), 0)
        self.assertContains(r, 'El precio debe ser mayor que cero.')

    def test_editar_precarga_y_guarda(self):
        p = self._producto()
        r = self.client.get(reverse('productos:editar', args=[p.pk]))
        self.assertContains(r, 'value="Teclado USB"')
        self.assertContains(r, 'value="45000.00"')
        r = self.client.post(reverse('productos:editar', args=[p.pk]), {
            'nombre': 'Teclado Pro', 'descripcion': 'x', 'categoria': self.cat.pk, 'precio': '50000', 'cantidad': '7'})
        self.assertRedirects(r, reverse('productos:detalle', args=[p.pk]))
        p.refresh_from_db()
        self.assertEqual((p.nombre, p.cantidad), ('Teclado Pro', 7))

    def test_eliminar_producto_por_post(self):
        p = self._producto()
        self.assertEqual(self.client.get(reverse('productos:eliminar', args=[p.pk])).status_code, 200)
        self.assertEqual(Producto.objects.count(), 1)
        self.client.post(reverse('productos:eliminar', args=[p.pk]))
        self.assertEqual(Producto.objects.count(), 0)

    def test_producto_inexistente_404(self):
        self.assertEqual(self.client.get(reverse('productos:detalle', args=[999])).status_code, 404)

    def test_busqueda_filtros_y_paginacion(self):
        for i in range(7):
            self._producto(nombre=f'Item {i}', cantidad=0 if i == 0 else 3 if i == 1 else 50)
        r = self.client.get(reverse('productos:lista'))
        self.assertEqual(len(r.context['pagina']), 5)
        self.assertEqual(r.context['total_productos'], 7)
        self.assertEqual(len(self.client.get(reverse('productos:lista') + '?page=2').context['pagina']), 2)
        self.assertEqual(len(self.client.get(reverse('productos:buscar') + '?q=Item 3').context['pagina']), 1)
        self.assertEqual(len(self.client.get(reverse('productos:lista') + '?existencias=out').context['pagina']), 1)
        self.assertEqual(len(self.client.get(reverse('productos:lista') + '?existencias=low').context['pagina']), 1)
        self.assertEqual(len(self.client.get(reverse('productos:lista') + f'?categoria={self.cat.pk}').context['pagina']), 5)

    def test_sin_categorias_redirige(self):
        Categoria.objects.all().delete()
        self.assertRedirects(self.client.get(reverse('productos:crear')), reverse('productos:categoria_crear'))


class CrudCategoriasTests(TestCase):
    def test_crear_y_nombre_repetido(self):
        self.client.post(reverse('productos:categoria_crear'), {'nombre': 'Audio', 'descripcion': ''})
        r = self.client.post(reverse('productos:categoria_crear'), {'nombre': 'audio', 'descripcion': ''})
        self.assertContains(r, 'Ya existe una categoría con ese nombre.')
        self.assertEqual(Categoria.objects.count(), 1)

    def test_editar(self):
        c = Categoria.objects.create(nombre='Audio')
        self.client.post(reverse('productos:categoria_editar', args=[c.pk]), {'nombre': 'Sonido', 'descripcion': 'd'})
        c.refresh_from_db()
        self.assertEqual(c.nombre, 'Sonido')

    def test_no_elimina_con_productos(self):
        c = Categoria.objects.create(nombre='Audio')
        Producto.objects.create(nombre='P', categoria=c, precio=1, cantidad=1)
        self.client.post(reverse('productos:categoria_eliminar', args=[c.pk]))
        self.assertTrue(Categoria.objects.filter(pk=c.pk).exists())

    def test_elimina_vacia_solo_por_post(self):
        c = Categoria.objects.create(nombre='Audio')
        self.assertEqual(self.client.get(reverse('productos:categoria_eliminar', args=[c.pk])).status_code, 405)
        self.client.post(reverse('productos:categoria_eliminar', args=[c.pk]))
        self.assertFalse(Categoria.objects.exists())

    def test_busqueda_y_orden(self):
        for n in ('Beta', 'Alfa'):
            Categoria.objects.create(nombre=n)
        r = self.client.get(reverse('productos:categorias') + '?orden=desc')
        self.assertEqual([c.nombre for c in r.context['categorias']], ['Beta', 'Alfa'])
        r = self.client.get(reverse('productos:categorias') + '?q=alf')
        self.assertEqual(len(r.context['categorias']), 1)
