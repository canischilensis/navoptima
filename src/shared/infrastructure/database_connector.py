import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Importamos el conector de nube (manejo de error por si no tienes las librerías instaladas aún)
try:
    from src.shared.infrastructure.alloydb_connector import get_alloydb_engine
except ImportError:
    get_alloydb_engine = None

class DatabaseConnector:
    _engine = None

    @classmethod
    def get_engine(cls):
        """
        Patrón Singleton para obtener el motor de base de datos.
        Detecta automáticamente si estamos en entorno LOCAL o CLOUD.
        """
        if cls._engine is not None:
            return cls._engine

        env_state = os.getenv("ENV_STATE", "local").lower()

        if env_state == "cloud":
            print("☁️ Iniciando conexión a Google Cloud AlloyDB...")
            if not get_alloydb_engine:
                raise ImportError("Se requiere 'google-cloud-alloydb-connector' para modo cloud.")
            cls._engine = get_alloydb_engine()
        
        else:
            # Configuración LOCAL (Docker / PostgreSQL estándar)
            print("🐳 Iniciando conexión a PostgreSQL Local (Docker)...")
            db_user = os.getenv("DB_USER", "postgres")
            db_pass = os.getenv("DB_PASSWORD", "postgres")
            db_host = os.getenv("DB_HOST", "localhost")
            db_port = os.getenv("DB_PORT", "5432")
            db_name = os.getenv("DB_NAME", "navoptima")

            database_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
            
            cls._engine = create_engine(database_url, echo=False)

        return cls._engine

    @classmethod
    def get_session(cls):
        """Devuelve una nueva sesión lista para usar"""
        engine = cls.get_engine()
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return SessionLocal()

# Instancia para uso rápido
db = DatabaseConnector()