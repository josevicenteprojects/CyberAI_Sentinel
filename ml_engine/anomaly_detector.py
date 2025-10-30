#!/usr/bin/env python3
"""
CyberAI Sentinel - Motor de Machine Learning
Desarrollado por: Vicente Alonso
Especialista en Ciberseguridad y Administración de Sistemas

Motor de detección de anomalías que combina:
- Isolation Forest para detección de outliers
- DBSCAN para clustering de eventos
- PCA para reducción de dimensionalidad
- Análisis de comportamiento de usuarios
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import joblib
import os

from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

class AnomalyDetector:
    """
    Motor de detección de anomalías para ciberseguridad
    """
    
    def __init__(self, model_path: str = "models/"):
        """
        Inicializar el detector de anomalías
        
        Args:
            model_path: Ruta donde guardar/cargar modelos
        """
        self.model_path = model_path
        self.isolation_forest = None
        self.dbscan = None
        self.pca = None
        self.scaler = None
        self.is_trained = False
        
        # Crear directorio de modelos si no existe
        os.makedirs(model_path, exist_ok=True)
        
        # Cargar modelos existentes si están disponibles
        self._load_models()
    
    def _load_models(self):
        """Cargar modelos pre-entrenados si existen"""
        try:
            if os.path.exists(f"{self.model_path}/isolation_forest.joblib"):
                self.isolation_forest = joblib.load(f"{self.model_path}/isolation_forest.joblib")
                logger.info("Modelo Isolation Forest cargado")
            
            if os.path.exists(f"{self.model_path}/dbscan.joblib"):
                self.dbscan = joblib.load(f"{self.model_path}/dbscan.joblib")
                logger.info("Modelo DBSCAN cargado")
            
            if os.path.exists(f"{self.model_path}/pca.joblib"):
                self.pca = joblib.load(f"{self.model_path}/pca.joblib")
                logger.info("Modelo PCA cargado")
            
            if os.path.exists(f"{self.model_path}/scaler.joblib"):
                self.scaler = joblib.load(f"{self.model_path}/scaler.joblib")
                logger.info("Scaler cargado")
            
            self.is_trained = True
            logger.info("Modelos cargados correctamente")
            
        except Exception as e:
            logger.warning(f"Error cargando modelos: {e}")
            self.is_trained = False
    
    def _save_models(self):
        """Guardar modelos entrenados"""
        try:
            if self.isolation_forest:
                joblib.dump(self.isolation_forest, f"{self.model_path}/isolation_forest.joblib")
            
            if self.dbscan:
                joblib.dump(self.dbscan, f"{self.model_path}/dbscan.joblib")
            
            if self.pca:
                joblib.dump(self.pca, f"{self.model_path}/pca.joblib")
            
            if self.scaler:
                joblib.dump(self.scaler, f"{self.model_path}/scaler.joblib")
            
            logger.info("Modelos guardados correctamente")
            
        except Exception as e:
            logger.error(f"Error guardando modelos: {e}")
    
    def generate_synthetic_data(self, n_samples: int = 1000) -> pd.DataFrame:
        """
        Generar datos sintéticos para entrenamiento y testing
        
        Args:
            n_samples: Número de muestras a generar
            
        Returns:
            DataFrame con datos sintéticos
        """
        logger.info(f"Generando {n_samples} muestras sintéticas...")
        
        # Generar datos normales (80% del dataset)
        normal_samples = int(n_samples * 0.8)
        
        # Características de eventos normales
        normal_data = {
            'timestamp': pd.date_range(start='2025-01-01', periods=normal_samples, freq='1min'),
            'user_id': np.random.randint(1, 100, normal_samples),
            'ip_address': [f"192.168.1.{np.random.randint(1, 255)}" for _ in range(normal_samples)],
            'event_type': np.random.choice(['login', 'file_access', 'network_request'], normal_samples),
            'success': np.random.choice([0, 1], normal_samples, p=[0.1, 0.9]),  # 90% éxito
            'response_time': np.random.normal(200, 50, normal_samples),  # ms
            'bytes_transferred': np.random.normal(1024, 256, normal_samples),
            'hour_of_day': np.random.randint(8, 18, normal_samples),  # Horario laboral
            'day_of_week': np.random.randint(0, 5, normal_samples),  # Lunes a viernes
        }
        
        # Generar datos anómalos (20% del dataset)
        anomaly_samples = n_samples - normal_samples
        
        anomaly_data = {
            'timestamp': pd.date_range(start='2025-01-01', periods=anomaly_samples, freq='1min'),
            'user_id': np.random.randint(1, 100, anomaly_samples),
            'ip_address': [f"10.0.0.{np.random.randint(1, 255)}" for _ in range(anomaly_samples)],
            'event_type': np.random.choice(['suspicious_login', 'data_exfiltration', 'privilege_escalation'], anomaly_samples),
            'success': np.random.choice([0, 1], anomaly_samples, p=[0.7, 0.3]),  # 70% fallo
            'response_time': np.random.normal(2000, 1000, anomaly_samples),  # ms - más lento
            'bytes_transferred': np.random.normal(10000, 5000, anomaly_samples),  # Más datos
            'hour_of_day': np.random.randint(0, 24, anomaly_samples),  # Cualquier hora
            'day_of_week': np.random.randint(0, 7, anomaly_samples),  # Cualquier día
        }
        
        # Combinar datos
        all_data = {key: list(normal_data[key]) + list(anomaly_data[key]) for key in normal_data.keys()}
        
        # Crear DataFrame
        df = pd.DataFrame(all_data)
        
        # Mezclar datos
        df = df.sample(frac=1).reset_index(drop=True)
        
        # Añadir etiquetas (1 = anómalo, 0 = normal)
        df['is_anomaly'] = [0] * normal_samples + [1] * anomaly_samples
        df = df.sample(frac=1).reset_index(drop=True)
        
        logger.info(f"Datos sintéticos generados: {len(df)} muestras")
        return df
    
    def prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """
        Preparar características para el modelo ML
        
        Args:
            df: DataFrame con datos de eventos
            
        Returns:
            Array numpy con características preparadas
        """
        logger.info("Preparando características...")
        
        # Crear copia para no modificar el original
        df_processed = df.copy()
        
        # Codificar variables categóricas
        df_processed['event_type_encoded'] = pd.Categorical(df_processed['event_type']).codes
        df_processed['ip_class'] = df_processed['ip_address'].apply(
            lambda x: 1 if x.startswith('192.168.') else 0
        )
        
        # Extraer características temporales
        df_processed['hour_sin'] = np.sin(2 * np.pi * df_processed['hour_of_day'] / 24)
        df_processed['hour_cos'] = np.cos(2 * np.pi * df_processed['hour_of_day'] / 24)
        df_processed['day_sin'] = np.sin(2 * np.pi * df_processed['day_of_week'] / 7)
        df_processed['day_cos'] = np.cos(2 * np.pi * df_processed['day_of_week'] / 7)
        
        # Seleccionar características numéricas
        feature_columns = [
            'success', 'response_time', 'bytes_transferred', 'hour_of_day',
            'day_of_week', 'event_type_encoded', 'ip_class',
            'hour_sin', 'hour_cos', 'day_sin', 'day_cos'
        ]
        
        features = df_processed[feature_columns].values
        
        logger.info(f"Características preparadas: {features.shape}")
        return features
    
    def train_models(self, df: pd.DataFrame) -> Dict:
        """
        Entrenar modelos de ML
        
        Args:
            df: DataFrame con datos de entrenamiento
            
        Returns:
            Diccionario con métricas de entrenamiento
        """
        logger.info("Iniciando entrenamiento de modelos...")
        
        # Preparar características
        X = self.prepare_features(df)
        y = df['is_anomaly'].values
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Normalizar características
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Entrenar Isolation Forest
        logger.info("Entrenando Isolation Forest...")
        self.isolation_forest = IsolationForest(
            contamination=0.2,  # 20% de anomalías esperadas
            random_state=42,
            n_estimators=100
        )
        self.isolation_forest.fit(X_train_scaled)
        
        # Entrenar DBSCAN
        logger.info("Entrenando DBSCAN...")
        self.dbscan = DBSCAN(eps=0.5, min_samples=5)
        self.dbscan.fit(X_train_scaled)
        
        # Entrenar PCA
        logger.info("Entrenando PCA...")
        self.pca = PCA(n_components=0.95)  # Mantener 95% de varianza
        self.pca.fit(X_train_scaled)
        
        # Evaluar modelos
        metrics = self._evaluate_models(X_test_scaled, y_test)
        
        # Guardar modelos
        self._save_models()
        self.is_trained = True
        
        logger.info("Entrenamiento completado")
        return metrics
    
    def _evaluate_models(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """
        Evaluar rendimiento de los modelos
        
        Args:
            X_test: Características de prueba
            y_test: Etiquetas de prueba
            
        Returns:
            Diccionario con métricas de evaluación
        """
        logger.info("Evaluando modelos...")
        
        # Predicciones Isolation Forest
        if_anomalies = self.isolation_forest.predict(X_test)
        if_scores = self.isolation_forest.score_samples(X_test)
        
        # Convertir predicciones (-1 = anómalo, 1 = normal)
        if_predictions = np.where(if_anomalies == -1, 1, 0)
        
        # Predicciones DBSCAN
        dbscan_labels = self.dbscan.fit_predict(X_test)
        dbscan_predictions = np.where(dbscan_labels == -1, 1, 0)
        
        # Métricas Isolation Forest
        if_metrics = {
            'isolation_forest': {
                'accuracy': np.mean(if_predictions == y_test),
                'precision': np.sum((if_predictions == 1) & (y_test == 1)) / np.sum(if_predictions == 1) if np.sum(if_predictions == 1) > 0 else 0,
                'recall': np.sum((if_predictions == 1) & (y_test == 1)) / np.sum(y_test == 1) if np.sum(y_test == 1) > 0 else 0,
                'f1_score': 0
            }
        }
        
        # Calcular F1-score
        if if_metrics['isolation_forest']['precision'] + if_metrics['isolation_forest']['recall'] > 0:
            if_metrics['isolation_forest']['f1_score'] = (
                2 * if_metrics['isolation_forest']['precision'] * if_metrics['isolation_forest']['recall']
            ) / (if_metrics['isolation_forest']['precision'] + if_metrics['isolation_forest']['recall'])
        
        # Métricas DBSCAN
        dbscan_metrics = {
            'dbscan': {
                'accuracy': np.mean(dbscan_predictions == y_test),
                'precision': np.sum((dbscan_predictions == 1) & (y_test == 1)) / np.sum(dbscan_predictions == 1) if np.sum(dbscan_predictions == 1) > 0 else 0,
                'recall': np.sum((dbscan_predictions == 1) & (y_test == 1)) / np.sum(y_test == 1) if np.sum(y_test == 1) > 0 else 0,
                'f1_score': 0
            }
        }
        
        # Calcular F1-score DBSCAN
        if dbscan_metrics['dbscan']['precision'] + dbscan_metrics['dbscan']['recall'] > 0:
            dbscan_metrics['dbscan']['f1_score'] = (
                2 * dbscan_metrics['dbscan']['precision'] * dbscan_metrics['dbscan']['recall']
            ) / (dbscan_metrics['dbscan']['precision'] + dbscan_metrics['dbscan']['recall'])
        
        metrics = {**if_metrics, **dbscan_metrics}
        
        logger.info(f"Métricas Isolation Forest: {metrics['isolation_forest']}")
        logger.info(f"Métricas DBSCAN: {metrics['dbscan']}")
        
        return metrics
    
    def detect_anomalies(self, df: pd.DataFrame) -> Dict:
        """
        Detectar anomalías en nuevos datos
        
        Args:
            df: DataFrame con nuevos eventos
            
        Returns:
            Diccionario con resultados de detección
        """
        if not self.is_trained:
            logger.error("Modelos no entrenados. Ejecutar train_models() primero.")
            return {"error": "Modelos no entrenados"}
        
        logger.info("Detectando anomalías...")
        
        # Preparar características
        X = self.prepare_features(df)
        X_scaled = self.scaler.transform(X)
        
        # Predicciones Isolation Forest
        if_anomalies = self.isolation_forest.predict(X_scaled)
        if_scores = self.isolation_forest.score_samples(X_scaled)
        
        # Predicciones DBSCAN
        dbscan_labels = self.dbscan.fit_predict(X_scaled)
        
        # Combinar predicciones (consenso)
        if_predictions = np.where(if_anomalies == -1, 1, 0)
        dbscan_predictions = np.where(dbscan_labels == -1, 1, 0)
        
        # Consenso: si ambos modelos predicen anomalía
        consensus_predictions = np.where(
            (if_predictions == 1) & (dbscan_predictions == 1), 1, 0
        )
        
        # Crear resultados
        results = {
            'total_events': len(df),
            'anomalies_detected': np.sum(consensus_predictions),
            'anomaly_rate': np.mean(consensus_predictions),
            'isolation_forest_anomalies': np.sum(if_predictions),
            'dbscan_anomalies': np.sum(dbscan_predictions),
            'anomaly_scores': if_scores.tolist(),
            'predictions': consensus_predictions.tolist(),
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Anomalías detectadas: {results['anomalies_detected']}/{results['total_events']}")
        
        return results
    
    def get_model_info(self) -> Dict:
        """
        Obtener información de los modelos
        
        Returns:
            Diccionario con información de los modelos
        """
        return {
            'is_trained': self.is_trained,
            'models_available': {
                'isolation_forest': self.isolation_forest is not None,
                'dbscan': self.dbscan is not None,
                'pca': self.pca is not None,
                'scaler': self.scaler is not None
            },
            'model_path': self.model_path,
            'timestamp': datetime.now().isoformat()
        }

# Función de utilidad para crear detector
def create_anomaly_detector(model_path: str = "models/") -> AnomalyDetector:
    """
    Crear instancia del detector de anomalías
    
    Args:
        model_path: Ruta donde guardar/cargar modelos
        
    Returns:
        Instancia de AnomalyDetector
    """
    return AnomalyDetector(model_path)

# Ejemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Crear detector
    detector = create_anomaly_detector()
    
    # Generar datos sintéticos
    df = detector.generate_synthetic_data(1000)
    
    # Entrenar modelos
    metrics = detector.train_models(df)
    
    # Detectar anomalías
    results = detector.detect_anomalies(df)
    
    print("=== CYBERAI SENTINEL - MOTOR ML ===")
    print(f"Modelos entrenados: {detector.is_trained}")
    print(f"Métricas: {metrics}")
    print(f"Resultados: {results}")