#Maneja la conexión a base de datos de todo el proyecto

import psycopg2
import json

# #***********************************************************************************************************************Update database
def database_connection():
    config_path = "config.json"
        # Leer los datos de conexión desde el archivo JSON
    with open(config_path) as file:
        data = json.load(file)

    # Obtener los valores de conexión
    database = data['database']
    user = data['user']
    password = data['password']
    host = data['host']
    port = data['port']

    # Establecer la conexión a la base de datos
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return conn