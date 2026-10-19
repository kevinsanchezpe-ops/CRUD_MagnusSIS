"""Vistas del inventario: CRUD de productos y categorías sobre la base de datos."""

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CategoriaForm, ProductoForm
from .models import STOCK_BAJO, Categoria, Producto

POR_PAGINA = 5


def lista_productos(request: HttpRequest) -> HttpResponse:
    q = request.GET.get('q', '').strip()
    categoria = request.GET.get('categoria', '').strip()
    existencias = request.GET.get('existencias', '').strip()

    productos = Producto.objects.select_related('categoria').order_by('-fecha_creacion', '-id')
    if q:
        productos = productos.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))
    if categoria.isdigit():
        productos = productos.filter(categoria_id=int(categoria))
    if existencias == 'out':
        productos = productos.filter(cantidad__lte=0)
    elif existencias == 'low':
        productos = productos.filter(cantidad__gt=0, cantidad__lte=STOCK_BAJO)
    elif existencias == 'ok':
        productos = productos.filter(cantidad__gt=STOCK_BAJO)

    pagina = Paginator(productos, POR_PAGINA).get_page(request.GET.get('page'))

    # Conserva los filtros al cambiar de página.
    params = request.GET.copy()
    params.pop('page', None)

    contexto = {
        'pagina': pagina,
        'q': q,
        'categoria_sel': categoria,
        'existencias_sel': existencias,
        'categorias': Categoria.objects.order_by('nombre'),
        'querystring': params.urlencode(),
        'hay_filtros': bool(q or categoria or existencias),
        'total_productos': Producto.objects.count(),
        'total_categorias': Categoria.objects.count(),
        'total_stock_bajo': Producto.objects.filter(
            cantidad__gt=0, cantidad__lte=STOCK_BAJO
        ).count(),
    }
    return render(request, 'productos/lista.html', contexto)


def buscar_producto(request: HttpRequest) -> HttpResponse:
    return lista_productos(request)


def detalle_producto(request: HttpRequest, pk: int) -> HttpResponse:
    producto = get_object_or_404(Producto.objects.select_related('categoria'), pk=pk)
    return render(request, 'productos/detalle.html', {'producto': producto})


def crear_producto(request: HttpRequest) -> HttpResponse:
    if not Categoria.objects.exists():
        messages.warning(request, 'Primero crea una categoría para clasificar los productos.')
        return redirect('productos:categoria_crear')
    form = ProductoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        producto = form.save()
        messages.success(request, f'Producto “{producto.nombre}” creado correctamente.')
        return redirect('productos:lista')
    return render(request, 'productos/form.html', {'form': form, 'editando': False})


def editar_producto(request: HttpRequest, pk: int) -> HttpResponse:
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, instance=producto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Producto “{producto.nombre}” actualizado correctamente.')
        return redirect('productos:detalle', pk=producto.pk)
    return render(
        request, 'productos/form.html',
        {'form': form, 'editando': True, 'producto': producto},
    )


def eliminar_producto(request: HttpRequest, pk: int) -> HttpResponse:
    producto = get_object_or_404(Producto.objects.select_related('categoria'), pk=pk)
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto “{nombre}” eliminado.')
        return redirect('productos:lista')
    return render(request, 'productos/confirmar_eliminar.html', {'producto': producto})


# ---------------------------- Categorías ----------------------------

def lista_categorias(request: HttpRequest) -> HttpResponse:
    q = request.GET.get('q', '').strip()
    orden = 'desc' if request.GET.get('orden') == 'desc' else 'asc'

    categorias = Categoria.objects.annotate(total=Count('productos'))
    if q:
        categorias = categorias.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))
    categorias = categorias.order_by('-nombre' if orden == 'desc' else 'nombre')

    return render(request, 'productos/categorias.html', {
        'categorias': categorias,
        'q': q,
        'orden': orden,
        'hay_categorias': Categoria.objects.exists(),
    })


def crear_categoria(request: HttpRequest) -> HttpResponse:
    form = CategoriaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        categoria = form.save()
        messages.success(request, f'Categoría “{categoria.nombre}” creada correctamente.')
        return redirect('productos:categorias')
    return render(request, 'productos/categoria_form.html', {'form': form, 'editando': False})


def editar_categoria(request: HttpRequest, pk: int) -> HttpResponse:
    categoria = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Categoría “{categoria.nombre}” actualizada.')
        return redirect('productos:categorias')
    return render(
        request, 'productos/categoria_form.html',
        {'form': form, 'editando': True, 'categoria': categoria},
    )


@require_POST
def eliminar_categoria(request: HttpRequest, pk: int) -> HttpResponse:
    categoria = get_object_or_404(Categoria, pk=pk)
    if categoria.productos.exists():
        messages.error(
            request,
            'No puedes eliminar una categoría que todavía tiene productos. '
            'Cambia primero esos productos a otra categoría.',
        )
    else:
        nombre = categoria.nombre
        categoria.delete()
        messages.success(request, f'Categoría “{nombre}” eliminada.')
    return redirect('productos:categorias')
