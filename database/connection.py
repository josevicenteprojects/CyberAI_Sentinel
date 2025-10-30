#!/usr/bin/env python3
"""
CyberAI Sentinel - Configuración de Base de Datos
Desarrollado por: Vicente Alonso
Especialista en Ciberseguridad y Administración de Sistemas

Configuración de conexión a PostgreSQL con SQLAlchemy
"""

import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from .models import Base

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Gestor de base de datos para CyberAI Sentinel
    """
    
    def __init__(self):
        """
        Inicializar gestor de base de datos
        """
        self.engine = None
        self.SessionLocal = None
        self._setup_database()
    
    def _get_database_url(self) -> str:
        """
        Obtener URL de conexión a la base de datos
        
        Returns:
            URL de conexión a PostgreSQL
        """
        # Configuración desde variables de entorno
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'cyberai_sentinel')
        db_user = os.getenv('DB_USER', 'cyberai_user')
        db_password = os.getenv('DB_PASSWORD', 'cyberai_password')
        
        # URL de conexión
        database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        logger.info(f"Configurando conexión a: {db_host}:{db_port}/{db_name}")
        return database_url
    
    def _setup_database(self):
        """
        Configurar conexión a la base de datos
        """
        try:
            # URL de conexión
            database_url = self._get_database_url()
            
            # Crear engine con configuración optimizada
            self.engine = create_engine(
                database_url,
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False,  # Cambiar a True para debug
                connect_args={
                    "options": "-c timezone=UTC"
                }
            )
            
            # Crear session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            logger.info("Conexión a base de datos configurada correctamente")
            
        except Exception as e:
            logger.error(f"Error configurando base de datos: {e}")
            raise
    
    def create_tables(self):
        """
        Crear todas las tablas en la base de datos
        """
        try:
            logger.info("Creando tablas en la base de datos...")
            Base.metadata.create_all(bind=self.engine)
            logger.info("Tablas creadas correctamente")
        except Exception as e:
            logger.error(f"Error creando tablas: {e}")
            raise
    
    def drop_tables(self):
        """
        Eliminar todas las tablas de la base de datos
        """
        try:
            logger.info("Eliminando tablas de la base de datos...")
            Base.metadata.drop_all(bind=self.engine)
            logger.info("Tablas eliminadas correctamente")
        except Exception as e:
            logger.error(f"Error eliminando tablas: {e}")
            raise
    
    def check_connection(self) -> bool:
        """
        Verificar conexión a la base de datos
        
        Returns:
            True si la conexión es exitosa, False en caso contrario
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                result.fetchone()
            logger.info("Conexión a base de datos verificada")
            return True
        except Exception as e:
            logger.error(f"Error verificando conexión: {e}")
            return False
    
    def get_session(self) -> Session:
        """
        Obtener sesión de base de datos
        
        Returns:
            Sesión de SQLAlchemy
        """
        return self.SessionLocal()
    
    @contextmanager
    def get_db_session(self) -> Generator[Session, None, None]:
        """
        Context manager para sesiones de base de datos
        
        Yields:
            Sesión de SQLAlchemy
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error en sesión de base de datos: {e}")
            raise
        finally:
            session.close()
    
    def execute_raw_query(self, query: str, params: dict = None):
        """
        Ejecutar consulta SQL raw
        
        Args:
            query: Consulta SQL
            params: Parámetros de la consulta
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params or {})
                return result.fetchall()
        except Exception as e:
            logger.error(f"Error ejecutando consulta: {e}")
            raise
    
    def get_database_info(self) -> dict:
        """
        Obtener información de la base de datos
        
        Returns:
            Diccionario con información de la base de datos
        """
        try:
            # Información de conexión
            connection_info = {
                'host': os.getenv('DB_HOST', 'localhost'),
                'port': os.getenv('DB_PORT', '5432'),
                'database': os.getenv('DB_NAME', 'cyberai_sentinel'),
                'user': os.getenv('DB_USER', 'cyberai_user'),
                'status': 'connected' if self.check_connection() else 'disconnected'
            }
            
            # Información de tablas
            with self.engine.connect() as connection:
                tables_query = """
                SELECT table_name, table_type 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                """
                tables = connection.execute(text(tables_query)).fetchall()
                connection_info['tables'] = [{'name': t[0], 'type': t[1]} for t in tables]
            
            return connection_info
            
        except Exception as e:
            logger.error(f"Error obteniendo información de base de datos: {e}")
            return {'error': str(e)}

# Instancia global del gestor de base de datos
db_manager = DatabaseManager()

# Función de utilidad para obtener sesión
def get_db() -> Generator[Session, None, None]:
    """
    Dependency para FastAPI - obtener sesión de base de datos
    
    Yields:
        Sesión de SQLAlchemy
    """
    with db_manager.get_db_session() as session:
        yield session

# Función para inicializar base de datos
def init_database():
    """
    Inicializar base de datos (crear tablas)
    """
    try:
        db_manager.create_tables()
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error inicializando base de datos: {e}")
        raise

# Función para verificar conexión
def check_database_health() -> dict:
    """
    Verificar salud de la base de datos
    
    Returns:
        Diccionario con estado de la base de datos
    """
    try:
        is_connected = db_manager.check_connection()
        db_info = db_manager.get_database_info()
        
        return {
            'status': 'healthy' if is_connected else 'unhealthy',
            'connected': is_connected,
            'info': db_info,
            'timestamp': '2025-01-01T00:00:00Z'
        }
    except Exception as e:
        logger.error(f"Error verificando salud de base de datos: {e}")
        return {
            'status': 'error',
            'connected': False,
            'error': str(e),
            'timestamp': '2025-01-01T00:00:00Z'
        }

# Ejemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Crear gestor de base de datos
    db = DatabaseManager()
    
    # Verificar conexión
    if db.check_connection():
        print("✅ Conexión a base de datos exitosa")
        
        # Crear tablas
        db.create_tables()
        print("✅ Tablas creadas correctamente")
        
        # Obtener información
        info = db.get_database_info()
        print(f"📊 Información de base de datos: {info}")
    else:
        print("❌ Error conectando a base de datos")








