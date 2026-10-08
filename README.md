# Sistema Web de Gestión de Inventario · Magnus SIS

Proyecto académico para diseñar y preparar un sistema web de inventario de productos y categorías. Incluye diagramas, un prototipo visual estático HTML/CSS y un esqueleto ejecutable en Django. Las operaciones CRUD y la lógica de negocio están pendientes.

## Asignatura

Lenguaje de Programación 1 · 2026-2

## Integrantes

- Kevin Julian Sanchez Perez
- Juan Jose Osorio Quitian
- Luis Esteban Medina
- Brayan Steven Sanchez
- Sergio Neira
- Hilver Galindo

## Repositorio

[github.com/kevinsanchezpe-ops/CRUD_MagnusSIS](https://github.com/kevinsanchezpe-ops/CRUD_MagnusSIS)

## Estado actual

- **Mockups:** seis pantallas estáticas en `mockups/`. Productos, categorías, precios, cantidades y estados son datos de ejemplo; los controles no ejecutan operaciones.
- **Django:** proyecto y app `productos` creados. Incluye modelos `Categoria` y `Producto`, ModelForms, rutas, vistas stub, plantillas placeholder, administración Django, migración inicial y dos pruebas de humo.
- **Base de datos:** SQLite configurado para desarrollo local. Los modelos están listos para migrarse.
- **Pendiente:** lógica CRUD, consultas y búsqueda, validación de precio mayor que cero, gestión funcional de categorías, interfaz Django integrada y configuración de MySQL.

## Tecnologías

- Prototipo: HTML5 y CSS3.
- Backend: Python y Django con arquitectura MVT.
- Desarrollo local: SQLite mediante Django ORM.
- Base de datos objetivo: MySQL (pendiente de configuración).

## Ver el prototipo

Abre `mockups/mockups-inventario.html` en un navegador. El HTML carga `mockups-inventario.css` y el logotipo de la raíz del repositorio.

## Ejecutar el esqueleto Django

Desde la raíz del repositorio, crea y activa un entorno virtual e instala las dependencias:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Después, inicia Django:

```powershell
cd magnus_sis
python manage.py migrate
python manage.py runserver
```

Las rutas de productos y categorías responden con plantillas placeholder; todavía no guardan, consultan ni modifican registros. Para acceder a `/admin/`, crea un usuario administrador con `python manage.py createsuperuser`.

## Comprobaciones

El esqueleto pasa `python manage.py check` y sus dos pruebas de humo (`python manage.py test productos`).

## Estructura

```text
CRUD_MagnusSIS/
├── .gitignore
├── README.md
├── requirements.txt
├── documento_Sistema.pdf
├── Logotipo corporativo Magnus SIS.png
├── mockups/
│   ├── mockups-inventario.html
│   └── mockups-inventario.css
└── magnus_sis/
    ├── manage.py
    ├── magnus_sis/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    └── productos/
        ├── admin.py
        ├── apps.py
        ├── forms.py
        ├── models.py
        ├── tests.py
        ├── urls.py
        ├── views.py
        ├── migrations/
        │   └── 0001_initial.py
        └── templates/productos/
            ├── base.html
            ├── categorias.html
            ├── confirmar_eliminar.html
            ├── detalle.html
            ├── form.html
            └── lista.html
```
