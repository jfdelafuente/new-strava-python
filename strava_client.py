"""
Cliente para interactuar con la API de Strava
"""
import requests
import json
from typing import Optional, Dict, List
from datetime import datetime


class StravaClient:
    """Cliente para consultar datos de actividades de Strava"""

    BASE_URL = "https://www.strava.com/api/v3"
    AUTH_URL = "https://www.strava.com/oauth/token"

    def __init__(self, client_id: str, client_secret: str, refresh_token: str):
        """
        Inicializa el cliente de Strava

        Args:
            client_id: ID de la aplicación de Strava
            client_secret: Secret de la aplicación de Strava
            refresh_token: Token de actualización para obtener access tokens
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.access_token: Optional[str] = None

    def _get_access_token(self) -> str:
        """Obtiene un nuevo access token usando el refresh token"""
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'
        }

        response = requests.post(self.AUTH_URL, data=payload)
        response.raise_for_status()

        data = response.json()
        self.access_token = data['access_token']
        return self.access_token

    def _get_headers(self) -> Dict[str, str]:
        """Obtiene los headers con autenticación para las peticiones"""
        if not self.access_token:
            self._get_access_token()

        return {
            'Authorization': f'Bearer {self.access_token}'
        }

    def get_athlete(self) -> Dict:
        """
        Obtiene información del atleta autenticado

        Returns:
            Diccionario con los datos del atleta
        """
        url = f"{self.BASE_URL}/athlete"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def get_activities(self, per_page: int = 30, page: int = 1) -> List[Dict]:
        """
        Obtiene las actividades del atleta

        Args:
            per_page: Número de actividades por página (máximo 200)
            page: Número de página

        Returns:
            Lista de actividades
        """
        url = f"{self.BASE_URL}/athlete/activities"
        params = {
            'per_page': per_page,
            'page': page
        }

        response = requests.get(url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return response.json()

    def get_activity_by_id(self, activity_id: int) -> Dict:
        """
        Obtiene los detalles de una actividad específica

        Args:
            activity_id: ID de la actividad

        Returns:
            Diccionario con los detalles de la actividad
        """
        url = f"{self.BASE_URL}/activities/{activity_id}"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def get_activity_streams(self, activity_id: int,
                            stream_types: List[str] = None) -> Dict:
        """
        Obtiene los streams (datos detallados) de una actividad

        Args:
            activity_id: ID de la actividad
            stream_types: Tipos de streams a obtener
                         (latlng, distance, altitude, time, etc.)

        Returns:
            Diccionario con los streams de la actividad
        """
        if stream_types is None:
            stream_types = ['latlng', 'distance', 'altitude', 'time',
                           'velocity_smooth', 'heartrate', 'cadence', 'watts']

        streams_str = ','.join(stream_types)
        url = f"{self.BASE_URL}/activities/{activity_id}/streams/{streams_str}"

        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def get_athlete_stats(self, athlete_id: int) -> Dict:
        """
        Obtiene las estadísticas del atleta

        Args:
            athlete_id: ID del atleta

        Returns:
            Diccionario con las estadísticas del atleta
        """
        url = f"{self.BASE_URL}/athletes/{athlete_id}/stats"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()


def format_activity_summary(activity: Dict) -> str:
    """
    Formatea un resumen de una actividad para mostrar

    Args:
        activity: Diccionario con los datos de la actividad

    Returns:
        String con el resumen formateado
    """
    name = activity.get('name', 'Sin nombre')
    activity_type = activity.get('type', 'N/A')
    distance_km = activity.get('distance', 0) / 1000
    moving_time_min = activity.get('moving_time', 0) / 60
    elevation_gain = activity.get('total_elevation_gain', 0)
    start_date = activity.get('start_date_local', 'N/A')

    summary = f"""
{'='*50}
Actividad: {name}
Tipo: {activity_type}
Fecha: {start_date}
Distancia: {distance_km:.2f} km
Tiempo en movimiento: {moving_time_min:.2f} min
Desnivel acumulado: {elevation_gain:.0f} m
{'='*50}
    """
    return summary
