import psycopg2
import psycopg2.extras

from config import Config


def get_connection():
    """Abre y devuelve una nueva conexión a PostgreSQL.

    Se usa RealDictCursor para que cada fila se pueda leer como un
    diccionario (producto["nombre"]) tanto en las rutas como en las
    plantillas Jinja.
    """
    return psycopg2.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        cursor_factory=psycopg2.extras.RealDictCursor,
    )
