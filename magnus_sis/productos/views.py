"""Vistas iniciales sin lógica de negocio."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def lista_productos(request: HttpRequest) -> HttpResponse:
    return render(request, 'productos/lista.html', {})


def buscar_producto(request: HttpRequest) -> HttpResponse:
    return render(request, 'productos/lista.html', {})


def detalle_producto(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'productos/detalle.html', {})


def crear_producto(request: HttpRequest) -> HttpResponse:
    return render(request, 'productos/form.html', {})


def editar_producto(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'productos/form.html', {})


def eliminar_producto(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'productos/confirmar_eliminar.html', {})


def lista_categorias(request: HttpRequest) -> HttpResponse:
    return render(request, 'productos/categorias.html', {})
