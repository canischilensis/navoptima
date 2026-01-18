import os
from google.cloud.alloydb.connector import Connector, IPTypes
import sqlalchemy
import pg8000

def get_alloydb_engine():
    """
    Inicializa un pool de conexiones SQLAlchemy hacia Google Cloud AlloyDB
    usando el conector oficial de Python.
    """
    # 1. Recuperar variables de entorno de Google Cloud
    project_id = os.getenv("GCP_PROJECT_ID")
    region = os.getenv("GCP_REGION")
    cluster_id = os.getenv("ALLOYDB_CLUSTER_ID")
    instance_id = os.getenv("ALLOYDB_INSTANCE_ID")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    # Validación básica
    if not all([project_id, region, cluster_id, instance_id, db_user, db_pass, db_name]):
        raise ValueError("Faltan variables de entorno para conectar a AlloyDB.")

    # Construir el nombre completo de la instancia
    instance_connection_name = f"projects/{project_id}/locations/{region}/clusters/{cluster_id}/instances/{instance_id}"

    # 2. Inicializar el conector
    # Nota: refresh_strategy='lazy' es eficiente para Cloud Run o Functions
    connector = Connector()

    def getconn():
        conn = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            # ip_type=IPTypes.PUBLIC  # Descomentar si te conectas desde fuera de la VPC (ej. tu PC local)
            # ip_type=IPTypes.PRIVATE # Usar esto si el código corre DENTRO de Google Cloud (Cloud Run/VM)
        )
        return conn

    # 3. Crear el motor de SQLAlchemy
    # El creador usa la función getconn definida arriba
    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800,
    )

    return engine