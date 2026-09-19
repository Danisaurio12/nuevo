import os
from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env (no versionado)
load_dotenv()


class Config:
    """Configuración de la aplicación, leída desde variables de entorno."""

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "inventario_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    SECRET_KEY = os.getenv("SECRET_KEY", "clave-de-desarrollo-no-usar-en-produccion")
