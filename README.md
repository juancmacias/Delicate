# 🚀 Delicaté - Plataforma de Productos Gourmet

<div align="center">
  <h3>Una solución completa para la gestión de productos gourmet</h3>
</div>

Delicaté es una plataforma moderna que permite a empresas comercializar productos gourmet, gestionar inventario, procesar ventas y administrar clientes. El sistema cuenta con una robusta API REST construida con Django REST Framework y un panel de administración personalizado.

## 📑 Índice
- Administración
  - [Descripción del Proyecto](#-descripción-del-proyecto)
  - [Tecnologías Utilizadas](#️-tecnologías-utilizadas)
  - [Estructura de la Base de Datos](#-estructura-de-la-base-de-datos)
  - [Estructura del Proyecto](#-estructura-del-proyecto)
  - [Configuración del Entorno de Desarrollo](#️-configuración-del-entorno-de-desarrollo)
  - [Ejecución del Proyecto](#-ejecución-del-proyecto)
  - [Ejecución de Pruebas](#-ejecución-de-pruebas)
  - [API REST](#-api-rest)
  - [Roles de Usuario](#-roles-de-usuario)
  - [Despliegue](#-despliegue)
  - [Gestión del Proyecto](#-gestión-del-proyecto)
  - [Niveles de Entrega](#-niveles-de-entrega)
  - [Próximos Pasos](#-próximos-pasos)
  - [Equipo de Desarrollo](#-equipo-de-desarrollo)
  - [Cómo Contribuir](#-cómo-contribuir)
  - [Licencia](#-licencia)
- [Public](#-public)
  - [Despliege en local](#-despliege-en-local)

## 📋 Descripción del Proyecto

El proyecto se enfoca en desarrollar una plataforma integral para la empresa Delicaté que desea comercializar sus productos gourmet. El desarrollo se ha planificado en fases:

1. **Fase 1**: Dar a conocer sus mejores productos (Nacional/Internacional)
2. **Fase 2**: Distribuir los productos en un bar-restaurante para catas
3. **Fase 3**: Expandirse a otras provincias para degustación de productos

## 🛠️ Tecnologías Utilizadas

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/DRF-FF1709?style=for-the-badge&logo=django&logoColor=white" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white" alt="JWT">
  <img src="https://img.shields.io/badge/Cloudinary-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white" alt="Cloudinary">
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git">
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</div>

- **Backend**: Django 5.1.6, Django REST Framework 3.15.2
- **Autenticación**: JWT (JSON Web Tokens)
- **Base de Datos**: PostgreSQL / SQLite (configurable)
- **Almacenamiento de imágenes**: Cloudinary
- **Control de versiones**: Git y GitHub Projects

## 📊 Estructura de la Base de Datos

El proyecto utiliza una estructura de base de datos relacional optimizada para la gestión de productos gourmet, usuarios y ventas:

### Tablas Principales

| Tabla | Descripción |
| ----- | ----------- |
| **company** | Almacena información de las empresas registradas con su nombre, CIF y datos de contacto |
| **type** | Categoriza los tipos de comercio o categorías de negocio |
| **users** | Gestiona usuarios del sistema con diferentes roles (admin, manager, employee, customer) |
| **products** | Catálogo de productos con precios, impuestos, stock y relaciones con empresa y tipo |
| **basket** | Carrito de compras temporal con productos seleccionados por los usuarios |
| **invoices** | Registro de ventas con información de pago, fecha y montos |
| **invoice_items** | Detalle de productos incluidos en cada factura |
| **stock_movements** | Historial de cambios en el inventario (entradas, salidas, ajustes) |

La estructura permite un seguimiento completo desde la adición de productos al inventario hasta la venta y facturación, manteniendo un registro de todos los movimientos.

Diagrama completo disponible en: [DBDiagram.io](https://dbdiagram.io/d/Copy-of-Untitled-Diagram-67cc7c6b263d6cf9a0b0ec13)

## 📦 Estructura del Proyecto

El proyecto está organizado de manera modular siguiendo los principios de Django, dividido en varias aplicaciones que gestionan diferentes aspectos del negocio:

```
delicate/
├── delicate_manager/         # Configuración principal del proyecto
│   ├── settings.py           # Configuración de Django
│   ├── urls.py               # Rutas principales
│   └── ...
│
├── delicate_apps/            # Aplicaciones modulares
│   ├── users/                # Gestión de usuarios y autenticación
│   ├── company/              # Administración de empresas
│   ├── store/                # Gestión de productos e inventario
│   ├── invoices/             # Facturación y exportación a CSV
│   ├── basket/               # Carrito de compras y proceso de checkout
│   └── type/                 # Clasificación de tipos de comercio
│
├── manage.py                 # Utilidad de gestión de Django
├── requirements.txt          # Dependencias del proyecto
└── .env_example              # Plantilla para variables de entorno
```

Cada aplicación contiene:
- **models.py**: Modelos de datos y lógica de negocio
- **views.py**: Controladores para procesar solicitudes
- **serializers.py**: Conversión entre formatos de datos
- **urls.py**: Definición de rutas de la API
- **admin.py**: Configuración del panel de administración
- **tests.py**: Pruebas unitarias y de integración

## ⚙️ Configuración del Entorno de Desarrollo

### Requisitos Previos

- Python 3.12 o superior
- PostgreSQL (opcional, también puede usar SQLite)
- pip o uv (gestor de paquetes)

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
   # Configuración general
   DEBUG=True
   SECURITY_KEY=tu_clave_segura_generada

   # Configuración de base de datos
   USE_LOCAL_DB=True
   LOCAL_DB_NAME=delicate_local
   LOCAL_DB_USER=postgres
   LOCAL_DB_PASSWORD=tu_contraseña_local
   LOCAL_DB_HOST=localhost
   LOCAL_DB_PORT=5432

   # Cloudinary
   CLOUDINARY_CLOUD_NAME=tu_cloud_name
   CLOUDINARY_API_KEY=tu_api_key
   CLOUDINARY_API_SECRET=tu_api_secret
   CLOUDINARY_URL_PREFIX=https://res.cloudinary.com/tu_cloud_name/
   ```

6. **Aplicar migraciones**:
   ```bash
   python manage.py migrate
   ```

### Configuración Inicial de la Base de Datos

Para utilizar el sistema, primero debes crear una compañía y un usuario administrador:

1. **Crear una compañía**:
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

2. **Crear un usuario administrador vinculado a la compañía**:
   ```bash
   python manage.py customcreateuser
   ```
   
   Sigue las instrucciones en la terminal:
   ```
   Email: admin@delicate.com
   Name: Admin User
   Roll (admin/manager/employee/customer): admin
   Company ID: 1  # El ID de la compañía creada anteriormente
   Password: ****
   Confirm Password: ****
   ```

## 🚀 Ejecución del Proyecto

1. **Iniciar el servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```

2. **Acceder al panel de administración**:
   Visita [http://localhost:8000/admin/](http://localhost:8000/admin/) e ingresa con las credenciales del usuario administrador creado anteriormente.

3. **Explorar el panel de administración y las funcionalidades implementadas**

## 🧪 Ejecución de Pruebas

El proyecto incluye un conjunto completo de pruebas unitarias y de integración para validar su funcionamiento. Las pruebas se han desarrollado siguiendo las mejores prácticas con un enfoque en la cobertura de código y la detección temprana de errores.

### Ejecutar todas las pruebas

```bash
python manage.py test
```

### Ejecutar pruebas específicas por aplicación

```bash
python manage.py test delicate_apps.users   # Pruebas de la aplicación de usuarios
python manage.py test delicate_apps.store   # Pruebas de la aplicación de productos
python manage.py test delicate_apps.basket  # Pruebas del carrito de compras
```

### Verificar cobertura de pruebas

Para verificar la cobertura de código de las pruebas (requiere instalar `coverage`):

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📝 API REST

### Endpoints Principales

- **Autenticación**:
  - `POST /v1/api/token/`: Obtener token JWT
  - `POST /v1/api/token/refresh/`: Refrescar token JWT

- **Usuarios**:
  - `GET /v1/api/users/users/`: Listar usuarios
  - `POST /v1/api/users/users/`: Crear usuario
  - `GET /v1/api/users/users/{id}/`: Obtener usuario por ID

- **Productos**:
  - `GET /v1/api/store/`: Listar productos
  - `POST /v1/api/store/create/`: Crear producto
  - `GET /v1/api/store/{id}/`: Obtener producto por ID

- **Carrito de Compras**:
  - `GET /v1/api/basket/basket/`: Listar items del carrito
  - `POST /v1/api/basket/basket/add/`: Añadir producto al carrito
  - `POST /v1/api/basket/basket/checkout/`: Procesar compra

- **Facturas**:
  - `GET /v1/api/invoices/`: Listar facturas
  - `GET /v1/api/invoices/{id}/`: Obtener factura por ID
  - `GET /v1/api/invoices/{id}/export-csv/`: Exportar factura a CSV

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



## 📊 Gestión del Proyecto

El desarrollo de Delicaté se ha gestionado utilizando GitHub Projects, implementando metodologías ágiles (SCRUM) para organizar el trabajo, realizar seguimiento de tareas y planificar sprints. Cada funcionalidad ha sido implementada siguiendo el flujo de trabajo de Git-flow, con ramas específicas para características, correcciones y versiones.

## 📁 Public

La parte publica para este proyecto se implementará utilizando Fast API. Esta sección se completará en una fase posterior del desarrollo.

## Despliege en local
Para utilizar una base de datos PostgreSQL remota y securias los login es necesario, configura en el archivo `.env`.

```bash
python -m venv .ven
pip .venv/Scripts/activate
pip install -r requirements.txt
python main.py
--
uvicorno app.main:app --reload
```
## End point principales de Public

### Endpoints Principales

- **Autenticación**:
  - `POST /v1/token/`: Logarse token JWT
  - `GET /v1/protected/`: Obtener el token

  **Monolitico**
  - Registrarse
  - Logarse
  - Ver productos
  - Ver detalles de productos
  - Añadir a la cesta
  - Finalir compra
  - Listar productos comprados
  - Descargar en pdf de factura

```bash
pytest tests/
```

## 🚧 Niveles de Entrega

El proyecto se ha desarrollado siguiendo un enfoque incremental con los siguientes niveles de funcionalidad:


## 🔮 Próximos Pasos

Esta sección describirá las mejoras y características planificadas para futuras versiones del proyecto.

> *Esta sección se completará a medida que el proyecto evolucione, detallando las próximas funcionalidades y mejoras que se implementarán.*

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

## 📄 Licencia

Este proyecto está bajo la Licencia MIT 

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

- Mantén el código limpio y bien documentado
- Sigue las convenciones de nomenclatura existentes
- Añade pruebas para nuevas funcionalidades
- Actualiza la documentación cuando sea necesario

Gracias por considerar contribuir a este proyecto. Tu ayuda es fundamental para su mejora continua.
