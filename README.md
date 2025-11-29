# Aplicación de consulta de datos de Strava

Aplicación en Python para consultar datos de actividades de un atleta a través de la API de Strava.

## Características

- Autenticación OAuth2 con Strava
- Consulta de información del atleta
- Obtención de actividades (rutas)
- Detalles completos de actividades individuales
- Obtención de streams (datos detallados como GPS, altitud, frecuencia cardíaca, etc.)
- Estadísticas del atleta

## Requisitos

- Python 3.7 o superior
- Cuenta de Strava
- Aplicación registrada en Strava API

## Instalación

1. Clona este repositorio o descarga los archivos

2. Crea un entorno virtual para aislar las dependencias del proyecto:

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

1. Instala las dependencias:
```bash
pip install -r requirements.txt
```

**Nota:** Cuando termines de trabajar con el proyecto, puedes desactivar el entorno virtual con:
```bash
deactivate
```

## Configuración

### 1. Registra tu aplicación en Strava

1. Ve a [https://www.strava.com/settings/api](https://www.strava.com/settings/api)
2. Crea una nueva aplicación
3. Anota tu `Client ID` y `Client Secret`

### 2. Obtén tu Refresh Token

Para obtener el refresh token, necesitas completar el flujo OAuth:

1. Ve a la siguiente URL en tu navegador (reemplaza `YOUR_CLIENT_ID`):
```
https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost&approval_prompt=force&scope=activity:read_all
```

2. Autoriza la aplicación. Serás redirigido a una URL como:
```
http://localhost/?state=&code=AUTHORIZATION_CODE&scope=read,activity:read_all
```

3. Copia el `code` de la URL

4. Usa este código para obtener el refresh token (reemplaza los valores):
```bash
curl -X POST https://www.strava.com/oauth/token \
  -d client_id=YOUR_CLIENT_ID \
  -d client_secret=YOUR_CLIENT_SECRET \
  -d code=AUTHORIZATION_CODE \
  -d grant_type=authorization_code
```

5. En la respuesta JSON, encontrarás tu `refresh_token`

### 3. Configura las credenciales

1. Copia el archivo de ejemplo:
```bash
cp config.example.json config.json
```

2. Edita `config.json` con tus credenciales:
```json
{
  "client_id": "TU_CLIENT_ID",
  "client_secret": "TU_CLIENT_SECRET",
  "refresh_token": "TU_REFRESH_TOKEN"
}
```

## Uso

### Ejecutar el ejemplo

```bash
python example.py
```

Este script mostrará:
- Información del atleta
- Las últimas 10 actividades
- Detalles de la actividad más reciente
- Streams de datos de la actividad
- Estadísticas generales del atleta

### Uso programático

```python
from strava_client import StravaClient
import json

# Cargar configuración
with open('config.json', 'r') as f:
    config = json.load(f)

# Crear cliente
client = StravaClient(
    client_id=config['client_id'],
    client_secret=config['client_secret'],
    refresh_token=config['refresh_token']
)

# Obtener actividades
activities = client.get_activities(per_page=20)

# Obtener detalles de una actividad
activity_details = client.get_activity_by_id(activity_id)

# Obtener streams (datos GPS, altitud, etc.)
streams = client.get_activity_streams(
    activity_id,
    stream_types=['latlng', 'distance', 'altitude']
)
```

## Métodos disponibles

### `StravaClient`

- `get_athlete()`: Obtiene información del atleta autenticado
- `get_activities(per_page, page)`: Obtiene lista de actividades
- `get_activity_by_id(activity_id)`: Obtiene detalles de una actividad específica
- `get_activity_streams(activity_id, stream_types)`: Obtiene datos detallados de una actividad
- `get_athlete_stats(athlete_id)`: Obtiene estadísticas del atleta

### Tipos de streams disponibles

- `latlng`: Coordenadas GPS
- `distance`: Distancia
- `altitude`: Altitud
- `time`: Tiempo
- `velocity_smooth`: Velocidad suavizada
- `heartrate`: Frecuencia cardíaca
- `cadence`: Cadencia
- `watts`: Potencia
- `temp`: Temperatura

## Estructura del proyecto

```
.
├── strava_client.py       # Cliente principal de Strava
├── example.py             # Ejemplo de uso
├── config.example.json    # Plantilla de configuración
├── config.json           # Tu configuración (no incluir en git)
├── requirements.txt      # Dependencias
├── .gitignore           # Archivos a ignorar en git
└── README.md            # Esta documentación
```

## Seguridad

- **NUNCA** compartas tu `config.json` o tus credenciales
- El archivo `config.json` está incluido en `.gitignore` para evitar subirlo accidentalmente
- Revoca el acceso de la aplicación desde tu cuenta de Strava si ya no la usas

## Límites de la API

Strava tiene límites de uso de la API:
- 100 peticiones cada 15 minutos
- 1000 peticiones por día

## Referencias

- [Documentación de la API de Strava](https://developers.strava.com/docs/reference/)
- [Guía de autenticación OAuth](https://developers.strava.com/docs/authentication/)
