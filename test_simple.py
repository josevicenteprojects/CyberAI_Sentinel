#!/usr/bin/env python3
"""
CyberAI Sentinel - Script de Prueba Simple
Desarrollado por: Vicente Alonso
Especialista en Ciberseguridad y Administracion de Sistemas
"""

import requests
import json
import time
import sys

# Configurar URL base
BASE_URL = "http://localhost:8000"

def print_header():
    """
    Imprimir cabecera del script
    """
    print("=" * 80)
    print("CYBERAI SENTINEL - PRUEBA SIMPLE DEL SISTEMA")
    print("=" * 80)
    print("Desarrollado por: Vicente Alonso")
    print("Email: jvab065@gmail.com")
    print("LinkedIn: linkedin.com/in/vicente-alonso-cybersecurity")
    print("=" * 80)

def test_server_connection():
    """
    Probar conexion con el servidor
    """
    print("\nProbando conexion con el servidor...")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"Servidor conectado: {data['message']}")
            print(f"Version: {data['version']}")
            print(f"Estado: {data['status']}")
            return True
        else:
            print(f"Error de conexion: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("No se puede conectar al servidor")
        print("Asegurate de que el servidor este ejecutandose:")
        print("python main.py")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False

def test_health_check():
    """
    Probar health check
    """
    print("\nProbando health check...")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"Health check exitoso: {data['status']}")
            print(f"Servicios: {data['services']}")
            return True
        else:
            print(f"Error en health check: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error en health check: {e}")
        return False

def test_ml_models():
    """
    Probar modelos ML
    """
    print("\nProbando modelos ML...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/ml/models", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"Modelos ML disponibles: {len(data['models'])}")
            for model in data['models']:
                print(f"  - {model['name']}: {model['status']}")
            return True
        else:
            print(f"Error obteniendo modelos: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error probando modelos ML: {e}")
        return False

def test_ml_training():
    """
    Probar entrenamiento de modelos ML
    """
    print("\nProbando entrenamiento de modelos ML...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/ml/train", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"Entrenamiento exitoso: {data['status']}")
            print(f"Muestras de entrenamiento: {data['training_samples']}")
            return True
        else:
            print(f"Error en entrenamiento: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"Error en entrenamiento: {e}")
        return False

def test_security_analysis():
    """
    Probar analisis de seguridad
    """
    print("\nProbando analisis de seguridad...")
    
    # Datos de prueba
    test_event = {
        "user_id": "test_user_001",
        "ip_address": "192.168.1.100",
        "event_type": "login",
        "success": True,
        "response_time": 0.5,
        "bytes_transferred": 1024,
        "hour_of_day": 14,
        "day_of_week": 1
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/security/analyze",
            json=test_event,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"Analisis exitoso: {data['threat_level']}")
            print(f"Confianza: {data['confidence']:.2f}")
            print(f"Es anomalia: {data['is_anomaly']}")
            print(f"Recomendaciones: {len(data['recommendations'])}")
            return True
        else:
            print(f"Error en analisis: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"Error en analisis: {e}")
        return False

def main():
    """
    Funcion principal del script de prueba
    """
    print_header()
    
    # Lista de pruebas
    tests = [
        ("Conexion del servidor", test_server_connection),
        ("Health check", test_health_check),
        ("Modelos ML", test_ml_models),
        ("Entrenamiento ML", test_ml_training),
        ("Analisis de seguridad", test_security_analysis)
    ]
    
    # Ejecutar pruebas
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Ejecutando: {test_name}")
        print(f"{'='*60}")
        
        try:
            if test_func():
                passed += 1
                print(f"EXITOSO: {test_name}")
            else:
                print(f"FALLIDO: {test_name}")
        except Exception as e:
            print(f"ERROR: {test_name} - {e}")
    
    # Resumen final
    print(f"\n{'='*80}")
    print(f"RESUMEN DE PRUEBAS")
    print(f"{'='*80}")
    print(f"Pruebas exitosas: {passed}/{total}")
    print(f"Porcentaje de exito: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("TODAS LAS PRUEBAS EXITOSAS!")
        print("CyberAI Sentinel esta funcionando correctamente")
    elif passed >= total * 0.8:
        print("La mayoria de las pruebas fueron exitosas")
        print("CyberAI Sentinel esta funcionando con algunos problemas menores")
    else:
        print("Varias pruebas fallaron")
        print("Revisa la configuracion y los logs")
    
    print(f"{'='*80}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)






