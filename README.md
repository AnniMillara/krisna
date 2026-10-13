# Cinepedia — proyecto Flask

Aplicación académica de películas con registro, inicio/cierre de sesión, CRUD de películas y comentarios.

## Requisitos previos

- Python 3.10 o superior.
- MySQL Server en ejecución.
- Acceso a una consola (PowerShell en Windows funciona).

## 1. Descomprimir y abrir el proyecto

Descomprime el ZIP y abre una terminal dentro de la carpeta `cinepedia_proyecto`, donde están `server.py` y `requirements.txt`.

## 2. Crear un entorno virtual

Windows (PowerShell):

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, puedes usar CMD:

```bat
venv\Scripts\activate.bat
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Instalar dependencias

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Crear la base de datos

Abre MySQL Workbench o una consola de MySQL y ejecuta el archivo `esquema.sql`.

El archivo crea la base de datos `esquema_peliculas` y las tablas `usuarios`, `peliculas` y `comentarios`.

**Importante:** si ya tienes una base de datos con tablas o datos, no ejecutes el esquema a ciegas. Revisa primero el esquema existente y haz una copia de seguridad. Este SQL usa `CREATE TABLE IF NOT EXISTS`, pero no modifica tablas antiguas que ya existan.

## 5. Configurar las credenciales

Copia `.env.example` y crea un archivo llamado `.env` en la misma carpeta que `server.py`.

Windows:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Edita `.env` y coloca las credenciales de tu MySQL:

```dotenv
SECRET_KEY=pon-aqui-una-clave-larga-y-aleatoria
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_contraseña_mysql
DB_NAME=esquema_peliculas
DB_PORT=3306
```

No compartas el archivo `.env` ni subas contraseñas reales a repositorios públicos.

## 6. Ejecutar la aplicación

Con el entorno virtual activado:

```bash
python server.py
```

Abre en el navegador la dirección que muestre Flask, normalmente:

http://127.0.0.1:5000/

Regístrate desde el formulario y luego podrás iniciar sesión, crear películas, ver detalles, editar y borrar las películas propias, y comentar películas creadas por otras cuentas.

## 7. Pruebas recomendadas

1. Registra dos usuarios diferentes.
2. Entra con el primer usuario y crea una película.
3. Comprueba que en la lista aparezcan `Ver`, `Editar` y `Borrar` para esa película.
4. Cierra sesión y entra con el segundo usuario.
5. Comprueba que ese usuario solo vea `Ver` para la película del primero.
6. Abre el detalle de la película y publica un comentario.
7. Comprueba que el segundo usuario pueda borrar su comentario.
8. Comprueba que el primer usuario no pueda comentar su propia película.
9. Intenta acceder a una ruta de edición con la cuenta equivocada; la operación debe rechazarse.
10. Prueba los campos vacíos, títulos duplicados y datos demasiado cortos.

## Notas

- Este ZIP se ha construido a partir del código compartido en la conversación y de un esquema SQL coherente con esos modelos. No se ha conectado a tu MySQL ni se han ejecutado pruebas de integración en tu equipo.
- Si el proyecto original usa otros nombres de columnas, una configuración distinta o una versión diferente del esquema, ajusta `mysqlconnection.py` y `esquema.sql` para que coincidan con la base real antes de ejecutar.
- La clave secreta de `.env.example` es solo una muestra; cámbiala para cualquier despliegue.
- Para producción, desactiva `debug=True` en `server.py` y configura HTTPS y una clave secreta segura.
