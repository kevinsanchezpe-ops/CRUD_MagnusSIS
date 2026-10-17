# Magnus SIS

Sistema académico de gestión de inventario desarrollado por el equipo del curso. En esta etapa se está adelantando la interfaz frontend; el backend se encuentra en construcción y todavía no está conectado a las operaciones de la interfaz.

## Estado del sistema

- **Frontend:** interfaz servida con plantillas Django y construida con HTML, CSS y JavaScript. Incluye listado y detalle de productos, formularios, categorías, búsqueda, filtros, ordenamiento y navegación por páginas. Se han ajustado los espacios, formularios, controles y acciones sobre la interfaz existente.
- **Datos de prueba:** la interfaz inicia sin productos ni categorías precargados. Las operaciones disponibles en el navegador guardan sus datos en `localStorage`; estos quedan en el navegador y equipo donde se crean.
- **Backend:** proyecto Django 6.1 y aplicación `productos` con estructura de modelos, formularios, rutas y administración. Las vistas aún no implementan el CRUD ni están conectadas al almacenamiento del frontend.
- **Base de datos:** SQLite está configurada para desarrollo. Los datos de `localStorage` no se guardan en SQLite ni aparecen en el panel `/admin/`.
- **Mockups y documentos:** los mockups se conservan en `mockups/` como material de referencia. La planeación y los entregables están organizados en `docs/planeacion/`.

## Tecnologías

- Interfaz: HTML5, CSS3 y JavaScript, sin framework de frontend.
- Servidor y backend: Python y Django, con arquitectura MVT, Django Forms y ORM.
- Base de datos local: SQLite. La conexión con MySQL queda para una etapa posterior.

## Requisitos

- Windows y PowerShell.
- Python instalado.
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

### Crear o actualizar las tablas

Ejecuta las migraciones desde la raíz del repositorio:

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

### Si el puerto 8000 está ocupado

Indica otro puerto al iniciar el servidor; por ejemplo, el 8001:

```powershell
.\venv\Scripts\python.exe .\magnus_sis\manage.py runserver 8001
```

En ese caso, abre <http://127.0.0.1:8001/>.

### Acceder al panel de administración

El superusuario de Django ya está creado. Con el servidor iniciado, entra a <http://127.0.0.1:8000/admin/> e inicia sesión con las credenciales configuradas para ese usuario. Si en el futuro necesitas crear otro administrador, ejecuta desde la raíz:

```powershell
.\venv\Scripts\python.exe .\magnus_sis\manage.py createsuperuser
```

El panel administra los datos del backend Django; no muestra los registros guardados en `localStorage` por la interfaz.

## Rutas principales

- `/` — listado de productos.
- `/productos/nuevo/` — formulario de creación.
- `/productos/<id>/` — detalle de producto.
- `/productos/<id>/editar/` — formulario de edición.
- `/productos/<id>/eliminar/` — confirmación de eliminación.
- `/categorias/` — gestión de categorías.
- `/admin/` — administración de Django.

## Estructura del proyecto

```text
CRUD_MagnusSIS/
├── assets/branding/             # Recursos de marca
├── docs/planeacion/             # Entregas, revisión y scripts de documentación
├── magnus_sis/
│   ├── manage.py                # Comandos de Django
│   ├── magnus_sis/              # Configuración y rutas del proyecto
│   └── productos/
│       ├── templates/productos/ # Plantillas de la interfaz
│       └── static/productos/    # CSS y JavaScript
├── mockups/                     # Mockups conservados como referencia
├── requirements.txt             # Dependencias Python
└── README.md
```

Los entornos virtuales (`venv/` o `.venv/`), la base de datos SQLite local y los archivos compilados de Python se excluyen del control de versiones.
