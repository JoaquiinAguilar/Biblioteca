# Sistema de Gestión de Cubículos

## Descripción del Proyecto

Este proyecto es un sistema de gestión de cubículos desarrollado con Django, diseñado para facilitar la reserva, ocupación y liberación de cubículos en un entorno educativo o de oficina. Permite a los usuarios rentar cubículos, ver su estado, y a los administradores gestionar los cubículos y usuarios, así como generar reportes de uso.

## Características

*   **Autenticación de Usuarios:** Inicio de sesión y cierre de sesión para usuarios regulares y personal (bibliotecarios/administradores).
*   **Dashboard Interactivo:** Visualización del estado de todos los cubículos (disponible, ocupado, mantenimiento).
*   **Renta de Cubículos:** Los usuarios pueden rentar cubículos disponibles por un tiempo determinado.
*   **Búsqueda de Estudiantes (AJAX):** Al rentar, se puede buscar estudiantes por número de control o nombre completo con sugerencias en tiempo real.
*   **Liberación Anticipada:** Los usuarios pueden liberar sus cubículos antes del tiempo programado.
*   **Gestión de Cubículos (Admin):** Los administradores pueden añadir, editar, eliminar y liberar cubículos forzosamente.
*   **Reportes de Uso:** Generación de reportes en CSV sobre el uso de cubículos y carreras.
*   **Carga de Datos (Admin):** Importación de datos de estudiantes y cubículos mediante archivos CSV.
*   **Scheduler:** Un script separado para liberar automáticamente los cubículos expirados.
*   **Diseño Responsivo:** Interfaz adaptada para dispositivos móviles y de escritorio.
*   **Página de Login Estilizada:** Una página de inicio de sesión moderna y limpia.

## Configuración del Entorno

Sigue estos pasos para configurar y ejecutar el proyecto localmente.

### 1. Clonar el Repositorio

```bash
git clone https://github.com/JoaquiinAguilar/Biblioteca.git
cd Biblioteca
```

### 2. Crear y Activar el Entorno Virtual

Es altamente recomendable usar un entorno virtual para gestionar las dependencias del proyecto.

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```
*(Si el archivo `requirements.txt` no existe, puedes crearlo con `pip freeze > requirements.txt` después de instalar las dependencias manualmente como `Django`, `python-dotenv`, etc.)*

### 4. Configurar la Base de Datos

El proyecto utiliza SQLite por defecto.

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 5. Crear un Superusuario (Administrador)

Necesitarás un superusuario para acceder al panel de administración de Django y gestionar el sistema.

```bash
python3 manage.py createsuperuser
```
Sigue las instrucciones para crear tu usuario y contraseña.

### 6. Cargar Datos Iniciales (Opcional)

Puedes cargar carreras, estudiantes y cubículos de ejemplo usando los archivos `careers.json`, `students.csv` y `cubicles.csv`.

```bash
python3 manage.py loaddata rentals/fixtures/careers.json
python3 manage.py import_students students.csv
python3 manage.py import_cubicles cubicles.csv
```
**Nota:** Asegúrate de que los archivos `students.csv` y `cubicles.csv` estén en la raíz del proyecto o especifica la ruta correcta.

## Ejecutar la Aplicación

Para iniciar el servidor de desarrollo de Django:

```bash
source venv/bin/activate
python3 manage.py runserver
```
La aplicación estará disponible en `http://127.0.0.1:8000/` (o el puerto que indique Django).

## Ejecutar el Scheduler

El scheduler es un script separado que se encarga de liberar automáticamente los cubículos cuyas rentas han expirado. Debe ejecutarse en un terminal diferente y mantenerse activo.

```bash
source venv/bin/activate
python3 run_scheduler.py
```

## Roles de Usuario y Permisos

*   **Usuarios Regulares:**
    *   Pueden ver el dashboard de cubículos.
    *   Pueden rentar cubículos disponibles.
    *   Pueden ver sus reservas activas y liberar su propio cubículo anticipadamente.
    *   No tienen acceso a la gestión de cubículos ni a la carga de CSV.
*   **Personal (Bibliotecarios/Administradores - `is_staff=True`):**
    *   Pueden ver el dashboard de cubículos.
    *   Pueden rentar cubículos.
    *   Pueden acceder a la gestión de cubículos (añadir, editar, eliminar, liberar forzosamente).
    *   Pueden acceder a la carga de CSV.
    *   Pueden ver reportes de uso.

## URLs Clave

*   **Dashboard:** `/`
*   **Login:** `/login/`
*   **Logout:** `/logout/`
*   **Detalle de Cubículo:** `/cubicles/<id_del_cubículo>/`
*   **Gestión de Cubículos (Admin):** `/management/cubicles/`
*   **Reportes:** `/reports/`
*   **Subir CSV (Admin):** `/upload/`
*   **Mis Reservas:** `/my-rentals/`

## Tecnologías Utilizadas

*   **Backend:** Django (Python)
*   **Base de Datos:** SQLite (por defecto)
*   **Frontend:** HTML, Tailwind CSS, JavaScript
*   **Iconos:** Font Awesome

---
**Nota:** Reemplaza `<URL_DEL_REPOSITORIO>` con la URL real de tu repositorio Git.
