#!/usr/bin/env python3
"""
CyberAI Sentinel - Tests para API
Desarrollado por: Vicente Alonso
Especialista en Ciberseguridad y Administración de Sistemas

Tests unitarios para la API FastAPI
"""

import unittest
import requests
import json
import time
import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestCyberAISentinelAPI(unittest.TestCase):
    """
    Tests para la API de CyberAI Sentinel
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Configurar tests de API
        """
        cls.base_url = "http://localhost:8000"
        cls.api_url = f"{cls.base_url}/api/v1"
        
        # Esperar a que la API esté disponible
        cls.wait_for_api()
    
    @classmethod
    def wait_for_api(cls, timeout=30):
        """
        Esperar a que la API esté disponible
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{cls.base_url}/health", timeout=5)
                if response.status_code == 200:
                    return
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)
        
        raise Exception("API no disponible después de 30 segundos")
    
    def test_root_endpoint(self):
        """
        Test: Endpoint raíz
        """
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('message', data)
        self.assertIn('version', data)
        self.assertIn('developer', data)
    
    def test_health_endpoint(self):
        """
        Test: Health check
        """
        response = requests.get(f"{self.base_url}/health")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('status', data)
        self.assertIn('services', data)
    
    def test_security_events_endpoint(self):
        """
        Test: Endpoint de eventos de seguridad
        """
        response = requests.get(f"{self.api_url}/security/events")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('events', data)
        self.assertIn('total', data)
        self.assertIn('timestamp', data)
    
    def test_security_events_with_filters(self):
        """
        Test: Eventos de seguridad con filtros
        """
        params = {
            'limit': 10,
            'offset': 0,
            'event_type': 'login'
        }
        
        response = requests.get(f"{self.api_url}/security/events", params=params)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('events', data)
        self.assertIn('total', data)
        self.assertEqual(data['limit'], 10)
        self.assertEqual(data['offset'], 0)
    
    def test_analyze_security_event(self):
        """
        Test: Análisis de evento de seguridad
        """
        event_data = {
            'user_id': 'test_user',
            'ip_address': '192.168.1.100',
            'event_type': 'login',
            'success': True,
            'response_time': 150.0,
            'bytes_transferred': 1024,
            'hour_of_day': 14,
            'day_of_week': 1
        }
        
        response = requests.post(
            f"{self.api_url}/security/analyze",
            json=event_data
        )
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('analysis_id', data)
        self.assertIn('threat_level', data)
        self.assertIn('confidence', data)
        self.assertIn('recommendations', data)
        self.assertIn('is_anomaly', data)
    
    def test_ml_models_endpoint(self):
        """
        Test: Endpoint de modelos ML
        """
        response = requests.get(f"{self.api_url}/ml/models")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('models', data)
        self.assertIn('system_status', data)
        self.assertIn('timestamp', data)
        
        # Verificar estructura de modelos
        models = data['models']
        self.assertIsInstance(models, list)
        self.assertGreater(len(models), 0)
        
        for model in models:
            self.assertIn('name', model)
            self.assertIn('type', model)
            self.assertIn('version', model)
            self.assertIn('status', model)
    
    def test_train_ml_models(self):
        """
        Test: Entrenamiento de modelos ML
        """
        response = requests.post(f"{self.api_url}/ml/train")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('status', data)
        self.assertIn('message', data)
        self.assertIn('training_samples', data)
        self.assertIn('metrics', data)
        
        self.assertEqual(data['status'], 'success')
        self.assertGreater(data['training_samples'], 0)
    
    def test_anomalies_endpoint(self):
        """
        Test: Endpoint de anomalías
        """
        response = requests.get(f"{self.api_url}/security/anomalies")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('anomalies', data)
        self.assertIn('total', data)
        self.assertIn('limit', data)
        self.assertIn('offset', data)
    
    def test_anomalies_with_severity_filter(self):
        """
        Test: Anomalías con filtro de severidad
        """
        params = {
            'limit': 10,
            'offset': 0,
            'severity': 'high'
        }
        
        response = requests.get(f"{self.api_url}/security/anomalies", params=params)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('anomalies', data)
        self.assertIn('total', data)
    
    def test_system_health_endpoint(self):
        """
        Test: Endpoint de salud del sistema
        """
        response = requests.get(f"{self.api_url}/system/health")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('status', data)
        self.assertIn('services', data)
        self.assertIn('database', data)
        self.assertIn('ml_models', data)
        self.assertIn('timestamp', data)
    
    def test_api_documentation(self):
        """
        Test: Documentación de la API
        """
        # Swagger UI
        response = requests.get(f"{self.base_url}/docs")
        self.assertEqual(response.status_code, 200)
        
        # ReDoc
        response = requests.get(f"{self.base_url}/redoc")
        self.assertEqual(response.status_code, 200)
    
    def test_error_handling(self):
        """
        Test: Manejo de errores
        """
        # Endpoint inexistente
        response = requests.get(f"{self.api_url}/nonexistent")
        self.assertEqual(response.status_code, 404)
        
        # Datos inválidos
        response = requests.post(
            f"{self.api_url}/security/analyze",
            json={"invalid": "data"}
        )
        # Debería funcionar con datos mínimos
        self.assertIn(response.status_code, [200, 422])
    
    def test_cors_headers(self):
        """
        Test: Headers CORS
        """
        response = requests.options(self.base_url)
        self.assertIn('Access-Control-Allow-Origin', response.headers)
        self.assertIn('Access-Control-Allow-Methods', response.headers)

class TestAPIIntegration(unittest.TestCase):
    """
    Tests de integración para la API
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Configurar tests de integración
        """
        cls.base_url = "http://localhost:8000"
        cls.api_url = f"{cls.base_url}/api/v1"
        cls.wait_for_api()
    
    @classmethod
    def wait_for_api(cls, timeout=30):
        """
        Esperar a que la API esté disponible
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{cls.base_url}/health", timeout=5)
                if response.status_code == 200:
                    return
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)
        
        raise Exception("API no disponible después de 30 segundos")
    
    def test_full_workflow(self):
        """
        Test: Flujo completo de trabajo
        """
        # 1. Verificar salud del sistema
        health_response = requests.get(f"{self.api_url}/system/health")
        self.assertEqual(health_response.status_code, 200)
        
        # 2. Entrenar modelos ML
        train_response = requests.post(f"{self.api_url}/ml/train")
        self.assertEqual(train_response.status_code, 200)
        
        # 3. Analizar evento de seguridad
        event_data = {
            'user_id': 'integration_test_user',
            'ip_address': '10.0.0.100',
            'event_type': 'suspicious_login',
            'success': False,
            'response_time': 5000.0,
            'bytes_transferred': 50000,
            'hour_of_day': 2,
            'day_of_week': 6
        }
        
        analyze_response = requests.post(
            f"{self.api_url}/security/analyze",
            json=event_data
        )
        self.assertEqual(analyze_response.status_code, 200)
        
        # 4. Verificar que se detectó anomalía
        analysis_data = analyze_response.json()
        self.assertIn('is_anomaly', analysis_data)
        self.assertIn('threat_level', analysis_data)
        
        # 5. Obtener anomalías detectadas
        anomalies_response = requests.get(f"{self.api_url}/security/anomalies")
        self.assertEqual(anomalies_response.status_code, 200)
        
        # 6. Obtener eventos de seguridad
        events_response = requests.get(f"{self.api_url}/security/events")
        self.assertEqual(events_response.status_code, 200)
    
    def test_performance(self):
        """
        Test: Rendimiento de la API
        """
        import time
        
        # Test de tiempo de respuesta
        start_time = time.time()
        response = requests.get(f"{self.api_url}/security/events")
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(end_time - start_time, 5.0)  # Menos de 5 segundos
        
        # Test de múltiples requests
        start_time = time.time()
        for _ in range(10):
            response = requests.get(f"{self.api_url}/security/events")
        end_time = time.time()
        
        self.assertLess(end_time - start_time, 10.0)  # Menos de 10 segundos para 10 requests

if __name__ == '__main__':
    # Ejecutar tests
    unittest.main(verbosity=2)








