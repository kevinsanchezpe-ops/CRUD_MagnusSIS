# Magnus SIS · Sistema de gestión de inventario

Proyecto académico para gestionar productos y categorías. El repositorio reúne el prototipo visual, una interfaz Django con interacciones de navegador y el esqueleto del backend.

## Estado actual

- **Interfaz:** plantillas Django basadas en los mockups, con estilos HTML/CSS y comportamiento JavaScript. El inventario inicia vacío; las operaciones de productos y categorías se guardan en `localStorage` del navegador.
- **Persistencia:** la interfaz de navegador todavía no usa Django ORM. Sus productos y categorías no aparecen en SQLite ni en `/admin/`; el almacenamiento también es distinto entre navegadores y equipos.
- **Backend:** Django 6.1, app `productos`, modelos, formularios, rutas y administración registrados. Las vistas siguen siendo stubs y no realizan CRUD ni consultas.
- **Base de datos:** SQLite configurado para desarrollo y migrado localmente. MySQL es una opción futura, aún sin conector ni configuración.
- **Mockups:** seis pantallas de referencia estáticas en `mockups/`; sus datos y controles son ilustrativos.
- **Documentación:** el PDF de especificación y el DOCX de planeación se conservan como entregables de la fase inicial; el árbol incluido en el PDF refleja la organización anterior del repositorio.

## Reglas de negocio propuestas

- Un producto requiere nombre, categoría, precio mayor que cero y cantidad igual o superior a cero.
- Cada producto pertenece a una categoría; una categoría puede tener cero o muchos productos.
- El backend aún no aplica las validaciones personalizadas ni las operaciones descritas.
- El frontend calcula el estado de stock con un umbral de cinco unidades. Ese umbral no está configurado en el modelo ni en el backend.
- SKU, contadores y paginación no forman parte del modelo Django actual.

## Tecnologías

- Frontend: HTML5, CSS3 y JavaScript sin framework.
- Backend: Python y Django con arquitectura MVT, Django Forms y ORM.
- Base de datos: SQLite local; MySQL queda como trabajo futuro.

## Ejecutar en Windows

Desde la raíz del repositorio, prepara el entorno una vez:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Aplica migraciones y crea las tablas:

```powershell
python .\magnus_sis\manage.py migrate
```

Inicia el servidor:

```powershell
python .\magnus_sis\manage.py runserver
```

Abre <http://127.0.0.1:8000/>. Para acceder al panel administrativo, crea un superusuario con `python .\magnus_sis\manage.py createsuperuser` y entra a <http://127.0.0.1:8000/admin/>.

Si ya existe el entorno `venv/` de este equipo, se puede usar su Python directamente desde la raíz:

```powershell
.\venv\Scripts\python.exe .\magnus_sis\manage.py migrate
.\venv\Scripts\python.exe .\magnus_sis\manage.py runserver
```

## Estructura

```text
CRUD_MagnusSIS/
├── assets/branding/              # Logotipo compartido
├── docs/
│   ├── especificacion/           # Documento de sistema
│   └── planeacion/
│       ├── entrega_0/            # Entregable de planeación
│       ├── scripts/              # Generador del DOCX y utilidades archivadas
│       └── revision/             # Versiones y capturas de revisión del PDF
├── magnus_sis/
│   ├── manage.py
│   ├── magnus_sis/               # Configuración Django
│   └── productos/                # Modelos, vistas, rutas, templates y static
├── mockups/                      # Prototipo HTML/CSS de referencia
├── .gitignore
├── README.md
└── requirements.txt
```

Los directorios locales `venv/` o `.venv/`, la base SQLite y los archivos Python compilados se excluyen del control de versiones.
