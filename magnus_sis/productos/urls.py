"""Rutas de la app de inventario."""

from django.urls import path

from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.lista_productos, name='lista'),
    path('buscar/', views.buscar_producto, name='buscar'),
    path('productos/nuevo/', views.crear_producto, name='crear'),
    path('productos/<int:pk>/', views.detalle_producto, name='detalle'),
    path('productos/<int:pk>/editar/', views.editar_producto, name='editar'),
    path('productos/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar'),
    path('categorias/', views.lista_categorias, name='categorias'),
    path('categorias/nueva/', views.crear_categoria, name='categoria_crear'),
    path('categorias/<int:pk>/editar/', views.editar_categoria, name='categoria_editar'),
    path('categorias/<int:pk>/eliminar/', views.eliminar_categoria, name='categoria_eliminar'),
]
