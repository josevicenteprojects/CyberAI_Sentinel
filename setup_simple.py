#!/usr/bin/env python3
"""
CyberAI Sentinel - Script de Configuracion Simple
Desarrollado por: Vicente Alonso
Especialista en Ciberseguridad y Administracion de Sistemas
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """
    Crear archivo .env con configuracion por defecto
    """
    env_content = """# CyberAI Sentinel - Variables de Entorno
# Desarrollado por: Vicente Alonso

# Base de datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cyberai_sentinel
DB_USER=cyberai_user
DB_PASSWORD=cyberai_password

# Aplicacion
DEBUG=True
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000

# Seguridad
SECRET_KEY=cyberai-sentinel-secret-key-2025
JWT_SECRET=cyberai-sentinel-jwt-secret-2025
ENCRYPTION_KEY=cyberai-sentinel-encryption-key-2025

# ML
ML_MODEL_PATH=./models
ML_TRAINING_DATA_PATH=./data/training
ML_PREDICTION_THRESHOLD=0.2
"""
    
    env_file = Path(".env")
    
    if env_file.exists():
        print("Archivo .env ya existe")
        return True
    
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("Archivo .env creado correctamente")
        return True
    except Exception as e:
        print(f"Error creando archivo .env: {e}")
        return False

def load_env_variables():
    """
    Cargar variables de entorno
    """
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("Variables de entorno cargadas correctamente")
        return True
    except ImportError:
        print("Instalando python-dotenv...")
        os.system("pip install python-dotenv")
        try:
            from dotenv import load_dotenv
            load_dotenv()
            print("Variables de entorno cargadas correctamente")
            return True
        except Exception as e:
            print(f"Error cargando variables de entorno: {e}")
            return False
    except Exception as e:
        print(f"Error cargando variables de entorno: {e}")
        return False

def main():
    """
    Funcion principal del script
    """
    print("=" * 60)
    print("CYBERAI SENTINEL - CONFIGURACION SIMPLE")
    print("=" * 60)
    print("Desarrollado por: Vicente Alonso")
    print("Email: jvab065@gmail.com")
    print("=" * 60)
    
    # Crear archivo .env
    print("\nPaso 1: Creando archivo .env...")
    if not create_env_file():
        print("Error creando archivo .env")
        return False
    
    # Cargar variables de entorno
    print("\nPaso 2: Cargando variables de entorno...")
    if not load_env_variables():
        print("Error cargando variables de entorno")
        return False
    
    print("\n" + "=" * 60)
    print("CONFIGURACION COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print("Variables configuradas:")
    print(f"  DB_HOST: {os.getenv('DB_HOST')}")
    print(f"  DB_PORT: {os.getenv('DB_PORT')}")
    print(f"  DB_NAME: {os.getenv('DB_NAME')}")
    print(f"  DB_USER: {os.getenv('DB_USER')}")
    print(f"  DEBUG: {os.getenv('DEBUG')}")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)






