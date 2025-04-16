# FastAPI Sample App

Una aplicación de ejemplo creada con FastAPI, containerizada con Docker y diseñada para correr tanto en ambiente local como desplegarse en IBM Code Engine.

## Tabla de Contenido

- [Descripción](#descripción)
- [Requisitos](#requisitos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación y Ejecución en Local](#instalación-y-ejecución-en-local)
  - [Ejecutar sin Docker](#ejecutar-sin-docker)
  - [Ejecutar con Docker](#ejecutar-con-docker)
- [Despliegue en IBM Code Engine](#despliegue-en-ibm-code-engine)
  - [Pasos Previos](#pasos-previos)
  - [Construir y Publicar la Imagen](#construir-y-publicar-la-imagen)
  - [Crear y Desplegar la Aplicación](#crear-y-desplegar-la-aplicación)
- [Consideraciones Finales](#consideraciones-finales)

## Descripción

Esta aplicación es una API desarrollada con FastAPI que ilustra buenas prácticas de desarrollo, incluyendo organización modular, manejo de configuración y pruebas. Además, se encuentra preparada para ser containerizada con Docker y desplegada en IBM Code Engine, lo cual garantiza consistencia entre ambientes de desarrollo, prueba y producción.

## Requisitos

- **Python 3.9+**: para ejecutar la aplicación de forma local.
- **Docker**: para construir y ejecutar la imagen de la aplicación.
- **Git**: para gestionar el control de versiones.
- **Cuenta en IBM Cloud**: para utilizar IBM Code Engine.
- **CLI de IBM Cloud y plugin Code Engine**: para desplegar la aplicación.

## Estructura del Proyecto

La estructura de carpetas recomendada es la siguiente:

```
fastapi-app/                # Raíz del proyecto
├── app/                    # Código fuente de la aplicación
│   ├── routers/
│   ├── crm.py
│   ├── docs.py
│   └── search.py
├── services/
│   ├── cloudant.py
│   ├── elastic.py
│   └── hubspot.py
├── workers/
│   ├── indexer.py
│   └── __init__.py
├── config.py
├── main.py
└── models.py
├── Dockerfile              # Instrucciones para construir la imagen Docker
├── requirements.txt        # Dependencias del proyecto
├── .env                    # Archivo de variables de entorno (no subir a Git)
├── .gitignore              # Archivos y carpetas a ignorar por Git
└── README.md               # Este archivo
```


## Instalación y Ejecución en Local
### Ejecutar sin Docker
Clonar el repositorio:
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio

#### Crear un entorno virtual e instalar dependencias:
python -m venv venv
source venv/bin/activate    # En Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

##### Configurar variables de entorno:
Crea o modifica el archivo .env en la raíz del proyecto con los valores necesarios (por ejemplo, configuraciones de base de datos y otros parámetros).

Ejecutar la aplicación:

uvicorn app.main:app --reload
La API estará disponible por defecto en http://localhost:8000.

###### Ejecutar con Docker
Construir la imagen Docker:
docker build -t fastapi-app .

Ejecutar el contenedor:
docker run -d --name fastapi-app -p 8000:8000 fastapi-app
Accede a la API en http://localhost:8000.

##### Despliegue en IBM Code Engine
IBM Code Engine permite desplegar aplicaciones containerizadas sin necesidad de gestionar infraestructura compleja. Sigue estos pasos:

#### Pasos Previos
Instalar IBM Cloud CLI:
Descarga e instala la CLI de IBM Cloud.
Instalar el plugin de Code Engine:r
ibmcloud plugin install code-engine
Iniciar sesión en IBM Cloud:
ibmcloud login --sso
Sigue las instrucciones para autenticarte.

### Seleccionar el proyecto de Code Engine:
Crea o selecciona un proyecto en Code Engine y usa:

ibmcloud ce project select --name <nombre-de-tu-proyecto>
Construir y Publicar la Imagen

### Construir la imagen con Docker (si no lo has hecho ya):

docker build -t <tu-registro>/<tu-namespace>/fastapi-app:latest .
Publicar la imagen en un Container Registry:
IBM Code Engine puede trabajar con IBM Cloud Container Registry o cualquier otra. Para IBM Cloud Container Registry, autentícate y sube la imagen:
ibmcloud cr login
docker push <tu-registro>/<tu-namespace>/fastapi-app:latest

Asegúrate de que la imagen sea accesible (pública o con las credenciales adecuadas).

Crear y Desplegar la Aplicación
### Crear la aplicación en Code Engine:
ibmcloud ce application create --name fastapi-app --image <tu-registro>/<tu-namespace>/fastapi-app:latest --port 8000
Esto creará y desplegará la aplicación en Code Engine. El parámetro --port debe coincidir con el puerto expuesto en tu Dockerfile (en este ejemplo, 8000).

### Verificar el despliegue: Obtén la URL pública asignada a tu aplicación:

ibmcloud ce application get --name fastapi-app
Con la URL obtenida, podrás acceder a tu API desde cualquier navegador.

## Consideraciones Finales
Variables de Entorno y Configuración:
Asegúrate de manejar con cuidado el archivo .env en local y de configurar las variables necesarias en IBM Code Engine (puedes usar secret management o variables de entorno configuradas desde la CLI).

## Actualizaciones y Escalabilidad:
Cada vez que realices cambios en el código, repite el proceso de construir y publicar la nueva imagen, y actualiza el despliegue en Code Engine.

## Pruebas y CI/CD:
Integra pruebas automatizadas para validar cambios locales y considera configurar un pipeline de CI/CD (por ejemplo, usando GitHub Actions) que automatice la construcción y despliegue de la imagen.

