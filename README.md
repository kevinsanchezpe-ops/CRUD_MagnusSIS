# Sistema Web de Gestión de Inventario · Magnus SIS

Propuesta académica para administrar productos y categorías de un inventario. El proyecto incluye un prototipo visual estático en HTML/CSS y el proyecto base de Django. El CRUD de inventario todavía no está implementado.

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

- **Mockups:** seis pantallas estáticas en `mockups/`: listado y búsqueda, registro, edición con validaciones de ejemplo, detalle, categorías y confirmación de eliminación. Los datos que aparecen son ilustrativos; los controles no ejecutan operaciones.
- **Django:** proyecto base bajo `magnus_sis/`, con la configuración predeterminada de SQLite y la ruta del administrador en `/admin/`.
- **Pendiente:** app de inventario, modelos `Categoria` y `Producto`, formularios y validaciones, vistas y rutas CRUD, plantillas, migraciones, persistencia, configuración de MySQL y pruebas.

## Tecnologías

- Prototipo: HTML5 y CSS3.
- Backend previsto: Python y Django con arquitectura MVT.
- Base de datos actual: SQLite para desarrollo local.
- Base de datos objetivo: MySQL mediante Django ORM.

## Ver el prototipo

Abre `mockups/mockups-inventario.html` en un navegador. El archivo usa `mockups-inventario.css` y el logotipo ubicado en la raíz del repositorio.

## Ejecutar el proyecto base de Django

Desde la raíz del repositorio, crea y activa un entorno virtual e instala Django:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install Django
```

Luego inicia el servidor:

```powershell
cd magnus_sis
python manage.py migrate
python manage.py runserver
```

La ruta disponible actualmente es `/admin/`. El CRUD descrito en los mockups aún no tiene una app Django asociada.

## Estructura actual

```text
CRUD_MagnusSIS/
├── README.md
├── documento_Sistema.pdf
├── Logotipo corporativo Magnus SIS.png
├── mockups/
│   ├── mockups-inventario.html
│   └── mockups-inventario.css
└── magnus_sis/
    ├── manage.py
    └── magnus_sis/
        ├── settings.py
        ├── urls.py
        ├── asgi.py
        └── wsgi.py
```

