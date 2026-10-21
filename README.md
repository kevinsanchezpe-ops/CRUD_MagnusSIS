# Magnus SIS

Sistema académico de gestión de inventario desarrollado por el equipo del curso. El repositorio contiene el MVP de consola solicitado para la entrega 2 y, aparte, un prototipo web en Django que el equipo adelantó.

## Entrega 2: MVP por consola

La guía del profesor para esta entrega pide un programa interactivo por consola que use una estructura en memoria. **Este MVP no usa Django ni una base de datos**: los productos se pierden al cerrar el programa.

Desde PowerShell, estando en la raíz del proyecto, ejecútalo con Python:

```powershell
py .\backend_consola\inventario.py
```

El menú permite agregar productos, mostrar el inventario, buscar por nombre y salir. Cada producto tiene nombre, cantidad en stock y precio.

## Estado del sistema

- **MVP de la entrega 2:** `backend_consola/inventario.py`, con inventario en RAM, menú interactivo, agregar/listar/buscar y salida.
- **Prototipo web adicional:** `magnus_sis/` contiene una interfaz Django con CRUD de productos y categorías sobre SQLite local. Este prototipo no equivale a una base de datos central del equipo ni cambia el alcance sin persistencia de la entrega 2.
- **Interfaz web:** plantillas Django, HTML, CSS y JavaScript; incluye listado, detalle, búsqueda, filtros y paginación.
- **Tailwind CSS:** instalado (v4) y compilado a los estáticos de Django; el diseño web actual continúa usando principalmente su CSS existente.
- **Pruebas del prototipo web:** hay pruebas automáticas de las rutas, formularios, CRUD y filtros en `magnus_sis/productos/tests.py`.
- **Mockups y documentos:** los mockups se conservan en `mockups/` como material de referencia. La planeación y los entregables están organizados en `docs/planeacion/`.

## Organización y límites actuales

La estructura separa el MVP de consola, el prototipo web y los documentos del curso. Dentro de `magnus_sis/`, `manage.py` inicia Django, `productos/` contiene la aplicación de inventario y `magnus_sis/` (la carpeta interior) contiene la configuración del proyecto Django. `frontend/` guarda la entrada de Tailwind que compila a los estáticos de `productos/`.

El MVP de consola se ajusta al alcance temporal de esta entrega y no persiste información. El prototipo web Django es trabajo adicional: utiliza una base SQLite local por computadora, excluida de Git; no hay una base de datos compartida/configurada para todo el equipo.

El prototipo web está preparado para desarrollo local, no para despliegue: sus vistas CRUD no requieren iniciar sesión, `DEBUG` está activado y `SECRET_KEY` está configurada en `settings.py`. Las validaciones de precio y nombre de categoría se aplican en los formularios web, pero todavía no son restricciones globales del modelo/base de datos. Estos puntos deben revisarse si el equipo decide avanzar el prototipo web en una fase posterior.

## Tecnologías

- MVP de consola: Python y estructuras de datos en memoria; no requiere paquetes externos.
- Prototipo web adicional: HTML5, CSS3, JavaScript, Tailwind CSS 4, Python y Django con arquitectura MVT, Django Forms y ORM.
- SQLite solo está configurada para el prototipo Django local. La base de datos compartida del equipo pertenece a una fase posterior.

## Requisitos

- Windows y PowerShell.
- Python instalado.
- Para el MVP de consola: solo Python; no hay dependencias externas.
- Para el prototipo web: dependencias de `requirements.txt`; Node.js y npm para compilar Tailwind CSS.

## Prototipo web Django adicional

El MVP de consola es el ejecutable que corresponde a la entrega 2. Esta sección sirve para ejecutar el prototipo web Django que existe aparte. Abre PowerShell en la raíz del proyecto.

### Primera ejecución o instalación de dependencias web

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

### Base local del prototipo web

Solo para ejecutar el prototipo web, aplica sus migraciones. Esto crea `magnus_sis/db.sqlite3` localmente; no configura una base de datos compartida ni es parte del MVP de consola:

```powershell
.\venv\Scripts\python.exe .\magnus_sis\manage.py migrate
```

### Arrancar el prototipo web

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
├── .agents/skills/ui-ux-pro-max/ # Guía local para diseño de interfaz
├── backend_consola/
│   └── inventario.py            # MVP de entrega 2, solo memoria RAM
├── docs/planeacion/
│   ├── entrega_0/                # Planeación inicial
│   ├── entrega_1/                # Documento de sistema de fase 1
│   ├── entrega_2/                # Instrucciones y documentos de la siguiente entrega
│   ├── revision/                 # PDF y capturas de revisión documental
│   └── scripts/                  # Generación y revisión de documentos
├── magnus_sis/
│   ├── frontend/tailwind.css    # Entrada de Tailwind para el prototipo web
│   ├── manage.py                # Punto de entrada de comandos Django
│   ├── magnus_sis/              # Configuración y rutas del proyecto
│   └── productos/
│       ├── migrations/          # Historial del esquema de datos
│       ├── admin.py              # Registro de modelos en Django Admin
│       ├── models.py            # Categoria y Producto
│       ├── forms.py             # Formularios y validaciones
│       ├── views.py             # Vistas del CRUD
│       ├── urls.py              # Rutas de la app
│       ├── tests.py             # Pruebas automáticas
│       ├── templates/productos/ # Plantillas de la interfaz
│       ├── static/branding/     # Logos SVG
│       └── static/productos/    # CSS, JavaScript y CSS compilado de Tailwind
├── mockups/                     # Mockups conservados como referencia
├── package.json                 # Dependencias y comandos de Tailwind
├── package-lock.json            # Versiones fijadas de dependencias npm
├── requirements.txt             # Dependencias Python
└── README.md
```

Los entornos virtuales (`venv/` o `.venv/`), `node_modules/`, la base SQLite local y los archivos compilados de Python se excluyen del control de versiones.
