# 🚀 Delicaté - Plataforma de Productos Gourmet

<div align="center">
  <h3>Una solución completa para la gestión de productos gourmet</h3>
</div>

Delicaté es una plataforma integral con dos componentes principales:

1. **Panel de Administración (Django)**: Backend robusto con Django REST Framework para la gestión completa de productos, usuarios, inventario y ventas.
2. **Tienda Online (FastAPI)**: Frontend público que permite a los clientes navegar por el catálogo, registrarse, gestionar su carrito y realizar compras.

## 👥 Equipo de Desarrollo

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/juancmacias">
        <img src="https://avatars.githubusercontent.com/u/53483587?v=4" width="100px;" alt="Juan Carlos"/>
        <br />
        <sub><b>Juan Carlos</b></sub>
      </a>
      <br />
      <sub>Scrum Master</sub>
    </td>
    <td align="center">
      <a href="https://github.com/jruizndev">
        <img src="https://avatars.githubusercontent.com/u/174449292?v=4" width="100px;" alt="Pepe"/>
        <br />
        <sub><b>Pepe</b></sub>
      </a>
      <br />
      <sub>Product Owner</sub>
    </td>
    <td align="center">
      <a href="https://github.com/marie-adi">
        <img src="https://avatars.githubusercontent.com/u/174536305?v=4" width="100px;" alt="Mariela"/>
        <br />
        <sub><b>Mariela</b></sub>
      </a>
      <br />
      <sub>Developer</sub>
    </td>
    <td align="center">
      <a href="https://github.com/jdomdev">
        <img src="https://avatars.githubusercontent.com/u/49209302?v=4" width="100px;" alt="Juan"/>
        <br />
        <sub><b>Juan</b></sub>
      </a>
      <br />
      <sub>Developer</sub>
    </td>
  </tr>
</table>

## 📑 Índice

-   [Descripción del Proyecto](#-descripción-del-proyecto)
-   [Tecnologías Utilizadas](#️-tecnologías-utilizadas)
-   [Estructura del Proyecto](#-estructura-del-proyecto)
-   [Estructura de la Base de Datos](#-estructura-de-la-base-de-datos)
-   [Configuración del Entorno de Desarrollo](#️-configuración-del-entorno-de-desarrollo)
-   [Ejecución del Proyecto](#-ejecución-del-proyecto)
    -   [Backend (Django Admin)](#backend-administrativo-django)
    -   [Frontend (FastAPI Public)](#frontend-tienda-pública-fastapi)
-   [Ejecución de Pruebas](#-ejecución-de-pruebas)
-   [API REST](#-api-rest)
-   [Roles de Usuario](#-roles-de-usuario)
-   [Despliegue](#-despliegue)
-   [Gestión del Proyecto](#-gestión-del-proyecto)
-   [Próximos Pasos](#-próximos-pasos)
-   [Cómo Contribuir](#-cómo-contribuir)
-   [Licencia](#-licencia)

## 📋 Descripción del Proyecto

El proyecto se enfoca en desarrollar una plataforma integral para la empresa Delicaté que desea comercializar sus productos gourmet. El desarrollo se ha planificado en fases:

1. **Fase 1**: Dar a conocer sus mejores productos (Nacional/Internacional)
2. **Fase 2**: Distribuir los productos en un bar-restaurante para catas
3. **Fase 3**: Expandirse a otras provincias para degustación de productos

## 🛠️ Tecnologías Utilizadas

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white" alt="JWT">
  <img src="https://img.shields.io/badge/Cloudinary-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white" alt="Cloudinary">
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git">
</div>

### Backend Administrativo (Django)

-   **Framework principal**: Django 5.1.6
-   **API REST**: Django REST Framework 3.15.2
-   **Autenticación**: JWT (JSON Web Tokens)
-   **Base de Datos**: PostgreSQL / SQLite (configurable)
-   **Almacenamiento de imágenes**: Cloudinary
-   **Gestión de dependencias**: pip/uv

### Frontend Tienda Pública (FastAPI)

-   **Framework principal**: FastAPI
-   **Plantillas**: Jinja2
-   **Estilos**: CSS3 personalizado
-   **Interactividad**: JavaScript
-   **Acceso a datos**: SQLAlchemy
-   **Autenticación**: JWT con PassLib y Python-JWT
-   **Gestión de sesiones**: Cookies seguras
-   **Generación de PDF**: xhtml2pdf

### Herramientas Comunes

-   **Control de versiones**: Git y GitHub Projects
-   **Despliegue**: Vercel, Render
-   **Pruebas**: pytest (FastAPI), Django test framework
-   **Documentación**: Markdown

## 📦 Estructura del Proyecto

El proyecto está organizado en dos componentes principales:

```
delicate/
├── admin/                       # Backend administrativo (Django)
│   ├── delicate_manager/        # Configuración principal de Django
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   ├── delicate_apps/           # Aplicaciones modulares de Django
│   │   ├── users/               # Gestión de usuarios y autenticación
│   │   ├── company/             # Administración de empresas
│   │   ├── store/               # Gestión de productos e inventario
│   │   ├── invoices/            # Facturación y exportación a CSV
│   │   ├── basket/              # Carrito de compras
│   │   └── type/                # Clasificación de tipos de comercio
│   ├── manage.py                # Script de gestión de Django
│   └── requirements.txt         # Dependencias del backend
│
├── app/                        # Frontend público (FastAPI)
│   ├── main.py                 # Punto de entrada de FastAPI
│   ├── auth.py                 # Autenticación JWT
│   └── models/                 # Modelos para SQLAlchemy
│       ├── crud.py             # Operaciones CRUD
│       ├── database.py         # Configuración de la base de datos
│       └── models.py           # Definición de modelos
│
├── static/                     # Archivos estáticos para FastAPI
│   ├── css/                    # Estilos CSS
│   ├── img/                    # Imágenes
│   └── js/                     # Scripts JavaScript
│
├── templates/                  # Plantillas Jinja2 para FastAPI
│   ├── include/                # Fragmentos reutilizables
│   │   ├── header.html
│   │   ├── footer.html
│   │   └── ...
│   ├── index.html
│   ├── login.html
│   └── ...
│
├── tests/                      # Pruebas unitarias y de integración
│   └── test_main.py            # Pruebas para FastAPI
│
├── main.py                     # Script para ejecutar FastAPI
├── requirements.txt            # Dependencias completas del proyecto
├── .env_example                # Plantilla para variables de entorno
└── vercel.json                 # Configuración para despliegue en Vercel
```

## 📊 Estructura de la Base de Datos

El proyecto utiliza una estructura de base de datos relacional optimizada para la gestión de productos gourmet, usuarios y ventas:

### Tablas Principales

| Tabla               | Descripción                                                                             |
| ------------------- | --------------------------------------------------------------------------------------- |
| **company**         | Almacena información de las empresas registradas con su nombre, CIF y datos de contacto |
| **type**            | Categoriza los tipos de comercio o categorías de negocio                                |
| **users**           | Gestiona usuarios del sistema con diferentes roles (admin, manager, employee, customer) |
| **products**        | Catálogo de productos con precios, impuestos, stock y relaciones con empresa y tipo     |
| **basket**          | Carrito de compras temporal con productos seleccionados por los usuarios                |
| **invoices**        | Registro de ventas con información de pago, fecha y montos                              |
| **invoice_items**   | Detalle de productos incluidos en cada factura                                          |
| **stock_movements** | Historial de cambios en el inventario (entradas, salidas, ajustes)                      |
| **django_session**  | Almacena información de sesiones de usuario                                             |

La estructura permite un seguimiento completo desde la adición de productos al inventario hasta la venta y facturación, manteniendo un registro de todos los movimientos.

Diagrama completo disponible en: [DBDiagram.io](https://dbdiagram.io/d/Copy-of-Untitled-Diagram-67cc7c6b263d6cf9a0b0ec13)

## ⚙️ Configuración del Entorno de Desarrollo

### Requisitos Previos

-   Python 3.12 o superior
-   PostgreSQL (opcional, también puede usar SQLite)
-   pip o uv (gestor de paquetes)

### Instalación

1. **Clonar el repositorio**:

    ```bash
    git clone https://github.com/tu-usuario/delicate.git
    cd delicate
    ```

2. **Crear un entorno virtual**:

    ```bash
    python -m venv env
    ```

3. **Activar el entorno virtual**:

    - En Windows:
        ```bash
        env\Scripts\activate
        ```
    - En macOS/Linux:
        ```bash
        source env/bin/activate
        ```

4. **Instalar dependencias**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Configurar variables de entorno**:
   Crea un archivo `.env` en la raíz del proyecto basándote en el archivo `.env_example`:

    ```
    # ==== Variables compartidas para ambos componentes =====
    # Configuración general
    DEBUG=True
    SECURITY_KEY=tu_clave_segura_generada

    # ==== Configuración para Django (Backend Admin) =====
    # Configuración de base de datos para Django
    USE_LOCAL_DB=True
    USE_SQLITE=False
    LOCAL_DB_NAME=delicate_local
    LOCAL_DB_USER=postgres
    LOCAL_DB_PASSWORD=tu_contraseña_local
    LOCAL_DB_HOST=localhost
    LOCAL_DB_PORT=5432

    # Base de datos remota (opcional)
    DB_NAME=your_remote_db_name
    DB_USER=your_remote_db_user
    DB_PASSWORD=your_remote_db_password
    DB_HOST=your_remote_db_host
    DB_PORT=5432

    # Cloudinary
    CLOUDINARY_CLOUD_NAME=tu_cloud_name
    CLOUDINARY_API_KEY=tu_api_key
    CLOUDINARY_API_SECRET=tu_api_secret
    CLOUDINARY_URL_PREFIX=https://res.cloudinary.com/tu_cloud_name/

    # ==== Configuración para FastAPI (Frontend Public) =====
    # JWT
    SECRET_KEY=hash_secreto
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

    # Conexión a base de datos para FastAPI (utiliza la misma BD que Django)
    DATABASE_URL=postgresql://postgres:tu_contraseña_local@localhost:5432/delicate_local

    # Correo (opcional para recuperación de contraseña)
    MAIL_USER=correo_electronico_al_que_se_envia
    MAIL_PASS=password
    MAIL_SMTP=smtp.correo.es
    MAIL_PORT=587
    ```

## 🚀 Ejecución del Proyecto

### Backend Administrativo (Django)

1. **Aplicar migraciones**:

    ```bash
    cd admin
    python manage.py migrate
    ```

2. **Crear una compañía y un usuario administrador**:

    Primero, crear una compañía:

    ```bash
    python manage.py shell
    ```

    En el shell de Python:

    ```python
    from delicate_apps.company.models import Company

    company = Company.objects.create(
        name="Mi Empresa",
        direction="Calle Principal 123",
        cif="B12345678",
        phone="123456789",
        mail="info@miempresa.com"
    )
    print(f"Compañía creada con ID: {company.id}")
    exit()
    ```

    Luego, crear un usuario administrador:

    ```bash
    python manage.py customcreateuser
    ```

    Sigue las instrucciones en la terminal.

3. **Iniciar el servidor de administración**:

    ```bash
    python manage.py runserver
    ```

4. **Acceder al panel de administración**:
   Visita [http://localhost:8000/admin/](http://localhost:8000/admin/) e ingresa con las credenciales del usuario administrador creado.

### Frontend Tienda Pública (FastAPI)

1. **Iniciar el servidor FastAPI**:

    ```bash
    # Desde la raíz del proyecto
    python main.py
    ```

    O alternativamente:

    ```bash
    uvicorn app.main:app --reload --port=8081
    ```

2. **Acceder a la tienda pública**:
   Visita [http://localhost:8081/](http://localhost:8081/) para ver la tienda online.

## 🧪 Ejecución de Pruebas

### Backend (Django)

```bash
cd admin
python manage.py test
```

Para verificar la cobertura de código de las pruebas (requiere instalar `coverage`):

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Frontend (FastAPI)

```bash
pytest tests/
```

## 📝 API REST

### Endpoints del Backend (Django)

-   **Autenticación**:

    -   `POST /v1/api/token/`: Obtener token JWT
    -   `POST /v1/api/token/refresh/`: Refrescar token JWT

-   **Usuarios**:

    -   `GET /v1/api/users/users/`: Listar usuarios
    -   `POST /v1/api/users/users/`: Crear usuario
    -   `GET /v1/api/users/users/{id}/`: Obtener usuario por ID

-   **Productos**:

    -   `GET /v1/api/store/`: Listar productos
    -   `POST /v1/api/store/create/`: Crear producto
    -   `GET /v1/api/store/{id}/`: Obtener producto por ID

-   **Carrito de Compras**:

    -   `GET /v1/api/basket/basket/`: Listar items del carrito
    -   `POST /v1/api/basket/basket/add/`: Añadir producto al carrito
    -   `POST /v1/api/basket/basket/checkout/`: Procesar compra

-   **Facturas**:
    -   `GET /v1/api/invoices/`: Listar facturas
    -   `GET /v1/api/invoices/{id}/`: Obtener factura por ID
    -   `GET /v1/api/invoices/{id}/export-csv/`: Exportar factura a CSV

### Endpoints del Frontend (FastAPI)

-   **Autenticación**:

    -   `POST /v1/token`: Obtener token JWT
    -   `GET /v1/protected`: Verificar autenticación

-   **Páginas Públicas**:

    -   `GET /`: Página principal
    -   `GET /login`: Página de inicio de sesión
    -   `GET /register`: Página de registro
    -   `GET /details/{id}`: Detalles de producto

-   **Perfil de Usuario**:

    -   `GET /users`: Ver perfil
    -   `POST /users`: Actualizar perfil

-   **Carrito y Compra**:
    -   `GET /cart`: Ver carrito
    -   `POST /v1/buy`: Añadir al carrito
    -   `GET /invoice`: Ver factura
    -   `GET /pay`: Procesar pago
    -   `GET /generate-invoice`: Generar PDF de factura

## 🔐 Roles de Usuario

El sistema implementa un modelo de gestión de permisos basado en roles para garantizar la seguridad y la correcta segregación de responsabilidades:

<div align="center">
  <table>
    <thead>
      <tr>
        <th align="center">Rol</th>
        <th align="center">Descripción</th>
        <th align="center">Permisos</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td align="center"><b>👑 Admin</b></td>
        <td>Administrador del sistema</td>
        <td>
          <ul>
            <li>Acceso completo a todas las funcionalidades</li>
            <li>Gestión de usuarios y permisos</li>
            <li>Configuración global del sistema</li>
            <li>Análisis de datos y reportes</li>
          </ul>
        </td>
      </tr>
      <tr>
        <td align="center"><b>🔑 Manager</b></td>
        <td>Gestor de negocio</td>
        <td>
          <ul>
            <li>Administración de productos e inventario</li>
            <li>Gestión de usuarios de nivel inferior</li>
            <li>Acceso a informes de ventas</li>
            <li>Aprobación de operaciones críticas</li>
          </ul>
        </td>
      </tr>
      <tr>
        <td align="center"><b>👔 Employee</b></td>
        <td>Personal de tienda</td>
        <td>
          <ul>
            <li>Procesamiento de ventas</li>
            <li>Consulta de productos e inventario</li>
            <li>Atención al cliente</li>
            <li>Informes básicos de operaciones</li>
          </ul>
        </td>
      </tr>
      <tr>
        <td align="center"><b>🛒 Customer</b></td>
        <td>Cliente final</td>
        <td>
          <ul>
            <li>Navegación por el catálogo de productos</li>
            <li>Gestión del carrito de compras</li>
            <li>Seguimiento de pedidos</li>
            <li>Acceso a historial de compras personal</li>
          </ul>
        </td>
      </tr>
    </tbody>
  </table>
</div>

## 🌐 Despliegue

### Opciones de Base de Datos

El proyecto soporta múltiples opciones de base de datos:

#### SQLite (Desarrollo)

Para utilizar SQLite, configura en el archivo `.env`:

```
USE_LOCAL_DB=False
USE_SQLITE=True
```

#### PostgreSQL Local

Para utilizar PostgreSQL local, configura en el archivo `.env`:

```
USE_LOCAL_DB=True
USE_SQLITE=False
LOCAL_DB_NAME=delicate_local
LOCAL_DB_USER=postgres
LOCAL_DB_PASSWORD=tu_contraseña
```

#### PostgreSQL Remoto

Para utilizar una base de datos PostgreSQL remota, configura en el archivo `.env`:

```
USE_LOCAL_DB=False
USE_SQLITE=False
DB_NAME=tu_bd_remota
DB_USER=tu_usuario_remoto
DB_PASSWORD=tu_contraseña_remota
DB_HOST=tu_host_remoto
DB_PORT=5432
```

### Despliegue de FastAPI (Frontend Público)

El proyecto está configurado para despliegue en Vercel mediante el archivo `vercel.json`:

```json
{
    "devCommand": "uvicorn main:app --host 0.0.0.0 --port 3000",
    "builds": [
        {
            "src": "app/main.py",
            "use": "@vercel/python"
        }
    ],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "app/main.py"
        }
    ]
}
```

La aplicación ya está desplegada en:
[Delicaté en Render](https://delicate-yxth.onrender.com/)

## 📊 Gestión del Proyecto

El desarrollo de Delicaté se ha gestionado utilizando GitHub Projects, implementando metodologías ágiles (SCRUM) para organizar el trabajo, realizar seguimiento de tareas y planificar sprints. Cada funcionalidad ha sido implementada siguiendo el flujo de trabajo de Git-flow, con ramas específicas para características, correcciones y versiones.

## 🔮 Próximos Pasos

## 👐 Cómo Contribuir

¡Agradecemos las contribuciones que ayuden a mejorar Delicaté! Si estás interesado en contribuir, sigue estos pasos:

1. **Fork** el repositorio
2. **Crea una rama** para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. **Realiza tus cambios** y documéntalos adecuadamente
4. **Ejecuta las pruebas** para asegurar que todo funciona correctamente
5. **Haz commit** de tus cambios (`git commit -m 'Añade nueva funcionalidad'`)
6. **Haz push** a la rama (`git push origin feature/nueva-funcionalidad`)
7. **Abre un Pull Request** en GitHub

### Guías de Contribución

-   Mantén el código limpio y bien documentado
-   Sigue las convenciones de nomenclatura existentes
-   Añade pruebas para nuevas funcionalidades
-   Actualiza la documentación cuando sea necesario

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

Gracias por considerar contribuir a este proyecto. Tu ayuda es fundamental para su mejora continua.
