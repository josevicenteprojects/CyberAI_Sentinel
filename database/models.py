#!/usr/bin/env python3
"""
CyberAI Sentinel - Modelos de Base de Datos
Desarrollado por: Vicente Alonso
Especialista en Ciberseguridad y Administración de Sistemas

Modelos SQLAlchemy para la base de datos PostgreSQL
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

Base = declarative_base()

class SecurityEvent(Base):
    """
    Modelo para eventos de seguridad
    """
    __tablename__ = 'security_events'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_id = Column(String(100), nullable=False, index=True)
    ip_address = Column(String(45), nullable=False, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    success = Column(Boolean, nullable=False, default=True)
    response_time = Column(Float, nullable=True)
    bytes_transferred = Column(Integer, nullable=True)
    hour_of_day = Column(Integer, nullable=False)
    day_of_week = Column(Integer, nullable=False)
    raw_data = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    anomaly_results = relationship("AnomalyResult", back_populates="event")
    
    # Índices
    __table_args__ = (
        Index('idx_timestamp', 'timestamp'),
        Index('idx_user_ip', 'user_id', 'ip_address'),
        Index('idx_event_type', 'event_type'),
    )
    
    def __repr__(self):
        return f"<SecurityEvent(id={self.id}, type={self.event_type}, timestamp={self.timestamp})>"

class AnomalyResult(Base):
    """
    Modelo para resultados de detección de anomalías
    """
    __tablename__ = 'anomaly_results'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey('security_events.id'), nullable=False)
    is_anomaly = Column(Boolean, nullable=False, default=False)
    anomaly_score = Column(Float, nullable=True)
    isolation_forest_prediction = Column(Boolean, nullable=True)
    dbscan_prediction = Column(Boolean, nullable=True)
    consensus_prediction = Column(Boolean, nullable=False)
    confidence_score = Column(Float, nullable=True)
    model_version = Column(String(50), nullable=True)
    analysis_timestamp = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    event = relationship("SecurityEvent", back_populates="anomaly_results")
    
    # Índices
    __table_args__ = (
        Index('idx_anomaly', 'is_anomaly'),
        Index('idx_consensus', 'consensus_prediction'),
        Index('idx_analysis_timestamp', 'analysis_timestamp'),
    )
    
    def __repr__(self):
        return f"<AnomalyResult(id={self.id}, anomaly={self.is_anomaly}, score={self.anomaly_score})>"

class ThreatIntelligence(Base):
    """
    Modelo para inteligencia de amenazas
    """
    __tablename__ = 'threat_intelligence'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    indicator_type = Column(String(50), nullable=False)  # IP, Domain, Hash, etc.
    indicator_value = Column(String(500), nullable=False)
    threat_type = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    confidence = Column(Float, nullable=False)
    source = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    tags = Column(JSONB, nullable=True)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        Index('idx_indicator', 'indicator_type', 'indicator_value'),
        Index('idx_threat_type', 'threat_type'),
        Index('idx_severity', 'severity'),
        Index('idx_active', 'is_active'),
    )
    
    def __repr__(self):
        return f"<ThreatIntelligence(id={self.id}, type={self.indicator_type}, value={self.indicator_value})>"

class MLModel(Base):
    """
    Modelo para información de modelos ML
    """
    __tablename__ = 'ml_models'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_name = Column(String(100), nullable=False, unique=True)
    model_type = Column(String(50), nullable=False)  # isolation_forest, dbscan, pca
    version = Column(String(20), nullable=False)
    accuracy = Column(Float, nullable=True)
    precision = Column(Float, nullable=True)
    recall = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    training_samples = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    model_path = Column(String(500), nullable=True)
    hyperparameters = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        Index('idx_model_name', 'model_name'),
        Index('idx_model_type', 'model_type'),
        Index('idx_active', 'is_active'),
    )
    
    def __repr__(self):
        return f"<MLModel(id={self.id}, name={self.model_name}, type={self.model_type})>"

class SystemMetrics(Base):
    """
    Modelo para métricas del sistema
    """
    __tablename__ = 'system_metrics'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(20), nullable=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    tags = Column(JSONB, nullable=True)
    
    # Índices
    __table_args__ = (
        Index('idx_metric_name', 'metric_name'),
        Index('idx_timestamp', 'timestamp'),
    )
    
    def __repr__(self):
        return f"<SystemMetrics(id={self.id}, name={self.metric_name}, value={self.metric_value})>"

class UserSession(Base):
    """
    Modelo para sesiones de usuario
    """
    __tablename__ = 'user_sessions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(100), nullable=False, index=True)
    session_id = Column(String(100), nullable=False, unique=True)
    ip_address = Column(String(45), nullable=False)
    user_agent = Column(Text, nullable=True)
    login_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_activity = Column(DateTime, nullable=False, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    logout_time = Column(DateTime, nullable=True)
    session_data = Column(JSONB, nullable=True)
    
    # Índices
    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_session_id', 'session_id'),
        Index('idx_active', 'is_active'),
        Index('idx_login_time', 'login_time'),
    )
    
    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id}, session_id={self.session_id})>"

class Alert(Base):
    """
    Modelo para alertas de seguridad
    """
    __tablename__ = 'alerts'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alert_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    source_event_id = Column(UUID(as_uuid=True), ForeignKey('security_events.id'), nullable=True)
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(String(100), nullable=True)
    alert_data = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        Index('idx_alert_type', 'alert_type'),
        Index('idx_severity', 'severity'),
        Index('idx_resolved', 'is_resolved'),
        Index('idx_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Alert(id={self.id}, type={self.alert_type}, severity={self.severity})>"








