import psycopg2
import requests
import pandas as pd
from datetime import datetime

# Paso 1: Crear la base de datos y la tabla desde Python
def create_database_and_table():
    try:
        # Conexión al servidor PostgreSQL (sin especificar una base de datos)
        conn = psycopg2.connect(
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True  
        cursor = conn.cursor()

        # Crear la base de datos "cybersecurity_datos" si no existe
        cursor.execute("SELECT datname FROM pg_database WHERE datname='cybersecurity_datos';")
        if not cursor.fetchone():
            cursor.execute("CREATE DATABASE cybersecurity_datos;")
            print("Base de datos 'cybersecurity_datos' creada correctamente.")
        else:
            print("La base de datos 'cybersecurity_datos' ya existe.")

        # Cerrar la conexión inicial
        cursor.close()
        conn.close()

        # Conectar a la nueva base de datos
        conn = psycopg2.connect(
            database="cybersecurity_datos",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Crear la tabla "datosapinist" si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS datosapinist (
            cve_id VARCHAR(20) PRIMARY KEY,
            description TEXT,
            published TIMESTAMP,
            last_modified TIMESTAMP,
            severity VARCHAR(10)
        );
        """)
        print("Tabla 'datosapinist' creada correctamente.")

        # Confirmar cambios y cerrar la conexión
        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error al crear la base de datos o la tabla: {e}")

# Paso 2: Obtener datos de la API y crear el DataFrame
def get_cve_data():
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    headers = {"Accept": "application/json"}
    api_key = "dd4e52a0-f2f8-4cdd-8d6d-03febbef0963"
    params = {
        "resultsPerPage": 10,
        "apiKey": api_key
    }

    # Realiza la solicitud
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 404:
        print("Parámetros fallaron, intentando sin ellos...")
        response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        cves = data["vulnerabilities"][:10]  # Limita a 10 filas

        # Crear el DataFrame con 5 columnas
        df = pd.DataFrame([
            {
                "cve_id": cve["cve"]["id"],
                "description": cve["cve"]["descriptions"][0]["value"],
                "published": cve["cve"]["published"],
                "last_modified": cve["cve"]["lastModified"],
                "severity": cve["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseSeverity"] if "cvssMetricV31" in cve["cve"]["metrics"] else "N/A"
            }
            for cve in cves
        ])
        print("Datos obtenidos de la API:")
        print(df)
        return df
    else:
        print("Error al obtener datos:", response.status_code, response.text)
        return None

# Paso 3: Insertar datos en la tabla
def insert_cve_data(df):
    if df is None:
        print("No hay datos para insertar.")
        return

    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            database="cybersecurity_datos",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Preparar los datos del DataFrame para la inserción
        records = [
            (
                row["cve_id"],
                row["description"],
                datetime.strptime(row["published"], "%Y-%m-%dT%H:%M:%S.%f"),  # Convertir a TIMESTAMP
                datetime.strptime(row["last_modified"], "%Y-%m-%dT%H:%M:%S.%f"),  # Convertir a TIMESTAMP
                row["severity"]
            )
            for index, row in df.iterrows()
        ]

        # Insertar registros en la tabla
        cursor.executemany("""
        INSERT INTO datosapinist (cve_id, description, published, last_modified, severity)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (cve_id) DO NOTHING;  -- Evita duplicados por cve_id
        """, records)

        # Confirmar cambios y cerrar la conexión
        conn.commit()
        print("Datos insertados correctamente en 'datosapinist'.")
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error al insertar datos: {e}")

# Ejecutar todas las funciones
if __name__ == "__main__":
    create_database_and_table()  # Crear base de datos y tabla
    df = get_cve_data()          # Obtener datos de la API
    insert_cve_data(df)          # Insertar datos en la tabla