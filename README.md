# 🧠 Enigma ERP - Backend

Este es el backend del sistema Enigma, un ERP modular desarrollado con Django y Django REST Framework. Gestiona productos, equipos, remitos, órdenes de reparación, logística y stock.

## 👨‍💻 Integrantes del equipo

- Néstor Díaz  
- Melvin Farias
- Elías Orihuela Torres  
- Matías Otero

---

## ⚙️ Tecnologías utilizadas

- Django (Python Web Framework)
- Python y vistas CBV
- Herencia de Layout, archivos estaticos (CSS / JS)
- HTML5 + Django Templates
- SQLite3 (Base de datos)
- ORM de Django (CRUD)
- Busqueda por multiples campos y filtros
- Bootstrap (para diseño frontend)
---

## 🔄 Flujo principal del sistema

1. **Recepción de Equipos:** Se registran los equipos devueltos por los clientes.
2. **Ingreso al Stock:** Los equipos son ingresados a inventario.
3. **Revisión Técnica:** Se revisan uno por uno para evaluar su estado.
4. **Clasificación Final:** Se les asigna un destino (por ejemplo, Nuevo, Averia, Destruccion, etc.).

---


## Estructura del Proyecto

    comercio/
    │
    ├── apps/ # Contiene las aplicaciones divididas por etapas
    │   ├── core/       # Funcionalidades base o comunes
    │   ├── usuarios/   # Etapa 1: Roles y usuarios
    │   ├── ingresos/   # Etapa 2: Remitos y productos ingresados
    │   ├── stock/      # Etapa 3: Stock de productos
    │   ├── ordenes/    # Etapa 4: Órdenes, estados y equipos
    │   └── despachos/  # Etapa 5: Pallets y DetallePallets
    │
    ├── seting/ # Configuración principal de Django (settings, urls, wsgi)
    │   ├── init.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    │
    ├── templates/      # Template's globales al proyecto
    │      ├── includes/
    │      │      ├── footer.html
    │      │      ├── header.html
    │      │      └── navbar.html
    │      ├── base.html
    │      └── dashboard.html
    │
    │
    ├── manage.py # Script principal para administrar el proyecto
    │
    └── requirements.txt # Dependencias del proyecto


###  🚀 Pasos para levantar el proyecto

###  1. Clonar el repositorio

    git clone https://github.com/teotronic5438/comercio.git
    cd comercio

### 2. Crear un entorno virtual

    python -m venv env
    source env/bin/activate  # Linux/macOS
    env\Scripts\activate     # Windows

### 3. Instalar dependencias

    pip install -r requirements.txt

### 4. Migrar la base de datos

    python manage.py makemigrations usuarios
    python manage.py makemigrations
    python manage.py migrate

### 5. Ejecutar el servidor

    python manage.py runserver

Luego accedé al sistema desde tu navegador en:

👉 http://127.0.0.1:8000

### 📌 Notas adicionales

    Se debe crear un superusuario para acceder al panel de admninistracion.

    Para mejor experiencia de usuario, la base se envia con datos de prueba para entorno de desarrollo.

    Para entorno productivo se habilito la base en MYSQL, por lo que se debe crear primero el superusuario y generar las tablas lokup necesarias (Estados, Depositos, Destinos y Productos).