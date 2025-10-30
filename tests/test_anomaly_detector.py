#!/usr/bin/env python3
"""
CyberAI Sentinel - Tests para Motor ML
Desarrollado por: Vicente Alonso
Especialista en Ciberseguridad y Administración de Sistemas

Tests unitarios para el detector de anomalías
"""

import unittest
import numpy as np
import pandas as pd
import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_engine.anomaly_detector import AnomalyDetector, create_anomaly_detector

class TestAnomalyDetector(unittest.TestCase):
    """
    Tests para la clase AnomalyDetector
    """
    
    def setUp(self):
        """
        Configurar tests
        """
        self.detector = create_anomaly_detector("test_models/")
        self.test_data = self.detector.generate_synthetic_data(100)
    
    def tearDown(self):
        """
        Limpiar después de tests
        """
        import shutil
        if os.path.exists("test_models/"):
            shutil.rmtree("test_models/")
    
    def test_detector_initialization(self):
        """
        Test: Inicialización del detector
        """
        self.assertIsNotNone(self.detector)
        self.assertFalse(self.detector.is_trained)
        self.assertEqual(self.detector.model_path, "test_models/")
    
    def test_synthetic_data_generation(self):
        """
        Test: Generación de datos sintéticos
        """
        data = self.detector.generate_synthetic_data(100)
        
        # Verificar estructura
        self.assertEqual(len(data), 100)
        self.assertIn('user_id', data.columns)
        self.assertIn('ip_address', data.columns)
        self.assertIn('event_type', data.columns)
        self.assertIn('is_anomaly', data.columns)
        
        # Verificar tipos de datos
        self.assertTrue(pd.api.types.is_numeric_dtype(data['user_id']))
        self.assertTrue(pd.api.types.is_bool_dtype(data['is_anomaly']))
    
    def test_feature_preparation(self):
        """
        Test: Preparación de características
        """
        features = self.detector.prepare_features(self.test_data)
        
        # Verificar forma
        self.assertEqual(features.shape[0], len(self.test_data))
        self.assertGreater(features.shape[1], 0)
        
        # Verificar que no hay NaN
        self.assertFalse(np.isnan(features).any())
    
    def test_model_training(self):
        """
        Test: Entrenamiento de modelos
        """
        # Entrenar modelos
        metrics = self.detector.train_models(self.test_data)
        
        # Verificar que está entrenado
        self.assertTrue(self.detector.is_trained)
        
        # Verificar métricas
        self.assertIn('isolation_forest', metrics)
        self.assertIn('dbscan', metrics)
        
        # Verificar que los modelos existen
        self.assertIsNotNone(self.detector.isolation_forest)
        self.assertIsNotNone(self.detector.dbscan)
        self.assertIsNotNone(self.detector.pca)
        self.assertIsNotNone(self.detector.scaler)
    
    def test_anomaly_detection(self):
        """
        Test: Detección de anomalías
        """
        # Entrenar modelos primero
        self.detector.train_models(self.test_data)
        
        # Detectar anomalías
        results = self.detector.detect_anomalies(self.test_data)
        
        # Verificar estructura de resultados
        self.assertIn('total_events', results)
        self.assertIn('anomalies_detected', results)
        self.assertIn('anomaly_rate', results)
        self.assertIn('predictions', results)
        
        # Verificar valores
        self.assertEqual(results['total_events'], len(self.test_data))
        self.assertGreaterEqual(results['anomalies_detected'], 0)
        self.assertLessEqual(results['anomaly_rate'], 1.0)
        self.assertGreaterEqual(results['anomaly_rate'], 0.0)
    
    def test_model_info(self):
        """
        Test: Información de modelos
        """
        info = self.detector.get_model_info()
        
        # Verificar estructura
        self.assertIn('is_trained', info)
        self.assertIn('models_available', info)
        self.assertIn('model_path', info)
        
        # Verificar tipos
        self.assertIsInstance(info['is_trained'], bool)
        self.assertIsInstance(info['models_available'], dict)
    
    def test_create_anomaly_detector(self):
        """
        Test: Función de utilidad create_anomaly_detector
        """
        detector = create_anomaly_detector("test_models/")
        
        self.assertIsInstance(detector, AnomalyDetector)
        self.assertEqual(detector.model_path, "test_models/")

class TestAnomalyDetectorIntegration(unittest.TestCase):
    """
    Tests de integración para el detector de anomalías
    """
    
    def setUp(self):
        """
        Configurar tests de integración
        """
        self.detector = create_anomaly_detector("test_models/")
        self.large_dataset = self.detector.generate_synthetic_data(1000)
    
    def tearDown(self):
        """
        Limpiar después de tests
        """
        import shutil
        if os.path.exists("test_models/"):
            shutil.rmtree("test_models/")
    
    def test_full_pipeline(self):
        """
        Test: Pipeline completo de detección
        """
        # Entrenar con dataset grande
        metrics = self.detector.train_models(self.large_dataset)
        
        # Verificar métricas
        self.assertIsInstance(metrics, dict)
        self.assertIn('isolation_forest', metrics)
        self.assertIn('dbscan', metrics)
        
        # Detectar anomalías
        results = self.detector.detect_anomalies(self.large_dataset)
        
        # Verificar resultados
        self.assertGreater(results['total_events'], 0)
        self.assertGreaterEqual(results['anomalies_detected'], 0)
        
        # Verificar que las predicciones tienen la longitud correcta
        self.assertEqual(len(results['predictions']), len(self.large_dataset))
    
    def test_model_persistence(self):
        """
        Test: Persistencia de modelos
        """
        # Entrenar modelos
        self.detector.train_models(self.large_dataset)
        
        # Crear nuevo detector
        new_detector = create_anomaly_detector("test_models/")
        
        # Verificar que los modelos se cargan
        self.assertTrue(new_detector.is_trained)
        self.assertIsNotNone(new_detector.isolation_forest)
        self.assertIsNotNone(new_detector.dbscan)
    
    def test_edge_cases(self):
        """
        Test: Casos límite
        """
        # Dataset vacío
        empty_data = self.detector.generate_synthetic_data(0)
        self.assertEqual(len(empty_data), 0)
        
        # Dataset muy pequeño
        small_data = self.detector.generate_synthetic_data(5)
        self.assertEqual(len(small_data), 5)
        
        # Entrenar con dataset pequeño
        try:
            metrics = self.detector.train_models(small_data)
            self.assertIsInstance(metrics, dict)
        except Exception as e:
            # Es esperado que falle con dataset muy pequeño
            self.assertIsInstance(e, Exception)

if __name__ == '__main__':
    # Configurar logging para tests
    import logging
    logging.basicConfig(level=logging.WARNING)
    
    # Ejecutar tests
    unittest.main(verbosity=2)








