# Magnus SIS

Sistema académico de gestión de inventario desarrollado por el equipo del curso. La interfaz está conectada al backend Django: los productos y las categorías se crean, consultan, editan y eliminan sobre una base de datos SQLite local.

## Inicio rápido

En PowerShell, desde cualquier carpeta, ejecuta:

```powershell
cd C:\Users\Julian\Documents\CRUD_MagnusSIS
.\venv\Scripts\python.exe .\magnus_sis\manage.py runserver
```

Abre <http://127.0.0.1:8000/>. Para detener el servidor, presiona `Ctrl+C` en la terminal. Si es la primera ejecución, sigue primero los pasos de instalación y migración de la sección [Iniciar el sistema en Windows](#iniciar-el-sistema-en-windows).

## Estado del sistema

- **Frontend:** interfaz servida con plantillas Django y construida con HTML, CSS y JavaScript. Incluye listado y detalle de productos, formularios, categorías, búsqueda, filtros por categoría y existencias, y paginación. Los datos se muestran desde la base de datos; el JavaScript solo aplica los filtros y confirma las eliminaciones.
- **Tailwind CSS:** instalado como herramienta de desarrollo (v4) con compilación local a los estáticos de Django. Queda listo para adoptar sus utilidades gradualmente; los estilos actuales siguen en uso.
- **Backend:** proyecto Django 6.1 y aplicación `productos` con CRUD completo de productos y categorías mediante el ORM, formularios con validaciones (nombre obligatorio, precio mayor que cero, cantidad no negativa, nombre de categoría único), mensajes de confirmación y administración en `/admin/`.
- **Base de datos:** SQLite configurada para desarrollo (`magnus_sis/db.sqlite3`, excluida del control de versiones). Los datos que se crean en la interfaz aparecen también en el panel `/admin/`.
- **Pruebas:** el repositorio incluye pruebas automáticas del CRUD, la búsqueda, los filtros y las validaciones (`python manage.py test`).
- **Mockups y documentos:** los mockups se conservan en `mockups/` como material de referencia. La planeación y los entregables están organizados en `docs/planeacion/`.

## Tecnologías

- Interfaz: HTML5, CSS3 y JavaScript; Tailwind CSS 4 está instalado como framework de utilidades, sin framework JavaScript de frontend.
- Servidor y backend: Python y Django, con arquitectura MVT, Django Forms y ORM.
- Base de datos local: SQLite. La conexión con MySQL queda para una etapa posterior.

## Requisitos

- Windows y PowerShell.
- Python instalado.
- Node.js y npm, para compilar Tailwind CSS.
- Dependencias del proyecto instaladas desde `requirements.txt`.

## Iniciar el sistema en Windows

Abre PowerShell y entra en la carpeta raíz del proyecto. Ajusta la ruta si guardaste el proyecto en otra ubicación:

```powershell
cd C:\Users\Julian\Documents\CRUD_MagnusSIS
```

### Primera ejecución o instalación de dependencias

Si aún no existe el entorno virtual, créalo. Después instala las dependencias:

```powershell
py -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Si el entorno `venv` ya existe, no hace falta volver a crearlo. Puedes activar ese entorno en PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Instala las dependencias de frontend y genera la hoja de estilos de Tailwind:

```powershell
npm install
npm run css:build
```

### Crear o actualizar las tablas

Ejecuta las migraciones desde la raíz del repositorio. Esto crea el archivo `db.sqlite3` la primera vez:

```powershell
.\venv\Scripts\python.exe .\magnus_sis\manage.py migrate
```

### Arrancar el servidor

```powershell
.\venv\Scripts\python.exe .\magnus_sis\manage.py runserver
```

El servidor de desarrollo corre por defecto en el **puerto 8000**. Abre estas direcciones en el navegador:

- Inicio del sistema: <http://127.0.0.1:8000/>
- Administración de Django: <http://127.0.0.1:8000/admin/>

Para detener el servidor, vuelve a la terminal y presiona `Ctrl+C`.

Mientras desarrollas estilos con Tailwind, puedes dejar la compilación en modo observación en una terminal y ejecutar Django en otra:

```powershell
npm run css:watch
```

La hoja compilada se guarda en `magnus_sis/productos/static/productos/tailwind.generated.css`. El diseño actual sigue usando su CSS existente; Tailwind queda instalado para incorporar utilidades gradualmente.

### Si el puerto 8000 está ocupado

Indica otro puerto al iniciar el servidor; por ejemplo, el 8001:

```powershell
.\venv\Scripts\python.exe .\magnus_sis\manage.py runserver 8001
```

En ese caso, abre <http://127.0.0.1:8001/>.

### Acceder al panel de administración

La base de datos no se sube al repositorio, así que cada integrante crea su propio superusuario después de aplicar las migraciones. Ejecuta desde la raíz:

```powershell
.\venv\Scripts\python.exe .\magnus_sis\manage.py createsuperuser
```

Escribe el nombre de usuario, el correo (opcional) y la contraseña. La contraseña no se muestra mientras la escribes. Después, con el servidor iniciado, entra a <http://127.0.0.1:8000/admin/>. El panel administra las mismas categorías y productos que muestra la interfaz.

### Ejecutar las pruebas

```powershell
.\venv\Scripts\python.exe .\magnus_sis\manage.py test
```

## Rutas principales

- `/` — listado de productos.
- `/productos/nuevo/` — formulario de creación.
- `/productos/<id>/` — detalle de producto.
- `/productos/<id>/editar/` — formulario de edición.
- `/productos/<id>/eliminar/` — confirmación de eliminación.
- `/categorias/` — listado, búsqueda y orden de categorías.
- `/categorias/nueva/` — formulario de creación de categoría.
- `/categorias/<id>/editar/` — formulario de edición de categoría.
- `/categorias/<id>/eliminar/` — eliminación de categoría (solo por POST, y solo si no tiene productos).
- `/admin/` — administración de Django.

## Estructura del proyecto

```text
CRUD_MagnusSIS/
├── assets/branding/             # Recursos de marca
├── docs/planeacion/             # Entregas, revisión y scripts de documentación
├── frontend/tailwind.css        # Entrada de estilos Tailwind
├── magnus_sis/
│   ├── manage.py                # Comandos de Django
│   ├── magnus_sis/              # Configuración y rutas del proyecto
│   └── productos/
│       ├── models.py            # Categoria y Producto
│       ├── forms.py             # Formularios y validaciones
│       ├── views.py             # Vistas del CRUD
│       ├── urls.py              # Rutas de la app
│       ├── tests.py             # Pruebas automáticas
│       ├── templates/productos/ # Plantillas de la interfaz
│       └── static/productos/    # CSS, JavaScript y CSS compilado de Tailwind
├── mockups/                     # Mockups conservados como referencia
├── package.json                 # Dependencias y comandos de Tailwind
├── requirements.txt             # Dependencias Python
└── README.md
```

Los entornos virtuales (`venv/` o `.venv/`), la base de datos SQLite local y los archivos compilados de Python se excluyen del control de versiones.
