"""
Ejemplo de uso del cliente de Strava
"""
import json
from strava_client import StravaClient, format_activity_summary


def main():
    # Cargar configuración
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Crear cliente
    client = StravaClient(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        refresh_token=config['refresh_token']
    )

    # Ejemplo 1: Obtener información del atleta
    print("Obteniendo información del atleta...")
    athlete = client.get_athlete()
    print(f"Atleta: {athlete['firstname']} {athlete['lastname']}")
    print(f"ID: {athlete['id']}")
    print()

    # Ejemplo 2: Obtener las últimas 10 actividades
    print("Obteniendo las últimas 10 actividades...")
    activities = client.get_activities(per_page=10)

    for i, activity in enumerate(activities, 1):
        print(f"\n--- Actividad {i} ---")
        print(format_activity_summary(activity))

    # Ejemplo 3: Obtener detalles de una actividad específica
    if activities:
        first_activity_id = activities[0]['id']
        print(f"\nObteniendo detalles de la actividad {first_activity_id}...")
        activity_details = client.get_activity_by_id(first_activity_id)

        print(f"Descripción: {activity_details.get('description', 'Sin descripción')}")
        print(f"Calorías: {activity_details.get('calories', 'N/A')}")
        print(f"Velocidad promedio: {activity_details.get('average_speed', 0) * 3.6:.2f} km/h")

        # Ejemplo 4: Obtener streams (datos detallados) de la actividad
        print(f"\nObteniendo streams de la actividad {first_activity_id}...")
        try:
            streams = client.get_activity_streams(
                first_activity_id,
                stream_types=['latlng', 'distance', 'altitude', 'time']
            )

            for stream in streams:
                stream_type = stream['type']
                data_length = len(stream['data'])
                print(f"Stream '{stream_type}': {data_length} puntos de datos")
        except Exception as e:
            print(f"No se pudieron obtener los streams: {e}")

    # Ejemplo 5: Obtener estadísticas del atleta
    print(f"\nObteniendo estadísticas del atleta...")
    stats = client.get_athlete_stats(athlete['id'])

    # Estadísticas totales
    all_time = stats.get('all_run_totals', {})
    if all_time:
        print("\nEstadísticas de carrera (todo el tiempo):")
        print(f"Distancia total: {all_time.get('distance', 0) / 1000:.2f} km")
        print(f"Número de actividades: {all_time.get('count', 0)}")
        print(f"Tiempo total: {all_time.get('moving_time', 0) / 3600:.2f} horas")


if __name__ == "__main__":
    main()
