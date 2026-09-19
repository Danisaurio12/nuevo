# Inventario Tienda de Tecnología

Aplicación web CRUD para administrar el inventario de productos de una tienda
de tecnología, desarrollada con **Flask** y **PostgreSQL**.

Permite registrar, listar, buscar, editar y eliminar productos desde una
interfaz con Bootstrap.

## Estructura del proyecto

```
inventario-tienda-tecnologia/
├── app.py                  # Rutas de la aplicación (listado, alta, edicion, eliminacion)
├── config.py                # Lectura de variables de entorno
├── db.py                    # Conexión a PostgreSQL (psycopg2)
├── requirements.txt
├── .env.example              # Plantilla de variables de entorno (copiar a .env)
├── .gitignore
├── database/
│   └── schema.sql            # Creación de la BD, tabla productos y datos de prueba
├── templates/
│   ├── base.html
│   ├── listado.html
│   └── formulario.html       # Reutilizado para registrar y editar
└── static/
    └── css/
        └── estilos.css
```

## Modelo de datos

Tabla `productos`:

| Campo       | Tipo            | Detalle                          |
|-------------|-----------------|-----------------------------------|
| id          | SERIAL          | Clave primaria                    |
| codigo      | VARCHAR(20)     | Único                              |
| nombre      | VARCHAR(100)    |                                    |
| categoria   | VARCHAR(50)     |                                    |
| precio      | NUMERIC(10,2)   | Admite decimales                  |
| existencia  | INTEGER         | Cantidad en inventario             |
| activo      | BOOLEAN         | Estado del producto                |

## Requisitos previos

- Python 3.10+
- PostgreSQL instalado y en ejecución
- pip / venv

## Instalación y ejecución local

1. **Clonar el repositorio**
   ```bash
   git clone <URL-de-tu-repositorio>
   cd inventario-tienda-tecnologia
   ```

2. **Crear y activar un entorno virtual**
   ```bash
   python -m venv venv
   # Windows (PowerShell):
   venv\Scripts\Activate.ps1
   # Linux / macOS:
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las variables de entorno**
   ```bash
   cp .env.example .env
   ```
   Edita `.env` con las credenciales reales de tu PostgreSQL local.
   Este archivo **no se sube al repositorio** (está en `.gitignore`).

5. **Crear la base de datos y las tablas**
   ```bash
   # Crea la base de datos (conectado al servidor, p. ej. a "postgres")
   psql -U postgres -c "CREATE DATABASE inventario_db;"

   # Crea la tabla y carga los datos de prueba
   psql -U postgres -d inventario_db -f database/schema.sql
   ```
   (El script también incluye el `CREATE DATABASE`; si tu cliente lo
   ejecuta todo en una sola conexión, créala primero manualmente y
   luego corre el resto del script ya conectado a `inventario_db`.)

6. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```
   Abre http://localhost:5000 en el navegador.

## Funcionalidades

- **Listado**: tabla con código, nombre, categoría, precio, existencia, estado y acciones.
- **Búsqueda**: filtro por código, nombre o categoría (`?q=` en la URL).
- **Registro**: formulario de alta con validación de campos y de código duplicado.
- **Edición**: mismo formulario, precargado con los datos del producto.
- **Eliminación**: solicita confirmación en el navegador antes de enviar la petición.

## Subir el proyecto a GitHub

Este repositorio ya tiene el historial de commits del desarrollo (los
commits se hicieron con una identidad de marcador de posición). Antes de
seguir trabajando o de hacer push, configura tu propia identidad:

```bash
git config user.name "Tu Nombre"
git config user.email "tu_correo@ejemplo.com"
```

1. Crea un repositorio vacío en GitHub (sin README, sin .gitignore).
2. Conéctalo como remoto y sube el historial:
   ```bash
   git remote add origin https://github.com/<tu-usuario>/<tu-repositorio>.git
   git branch -M main
   git push -u origin main
   ```
3. Comparte el enlace público del repositorio como entrega.

> Si vas a usar GitHub Desktop, simplemente añade esta carpeta como
> repositorio local existente ("Add local repository") y luego
> "Publish repository".

## Validaciones

- Campos obligatorios: código, nombre, categoría, precio y existencia.
- El **precio** debe ser mayor que cero (validado en el formulario con `min="0.01"` y en el servidor).
- La **existencia** no puede ser negativa (validado en el formulario con `min="0"` y en el servidor).
- El **código** debe ser único; si ya existe, se muestra un mensaje de error específico.
- Cada acción (registrar, editar, eliminar) muestra un mensaje `flash` de éxito o error, visible en la parte superior de la página.

## Notas de seguridad

- Ninguna credencial de PostgreSQL está en el código: todo se lee desde `.env` mediante `python-dotenv`.
- `.env` está excluido por `.gitignore`; solo `.env.example` (sin datos reales) se versiona.
- Todas las consultas que reciben datos del usuario (listado con búsqueda, registro, edición, eliminación) usan **consultas parametrizadas** de psycopg2 (`%s` + tupla de valores), nunca concatenación ni f-strings dentro del SQL. Esto evita inyección SQL.
