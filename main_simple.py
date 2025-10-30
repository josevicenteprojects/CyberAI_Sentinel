#!/usr/bin/env python3
"""
CyberAI Sentinel - Versión Simplificada
Desarrollado por: Vicente Alonso
Especialista en Ciberseguridad y Administración de Sistemas

Versión simplificada que funciona sin base de datos para demostración
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional
import json
import time
from datetime import datetime
import random

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("cyberai_sentinel.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="CyberAI Sentinel",
    description="Sistema de inteligencia artificial para ciberseguridad",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos del dashboard si existen
static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/app", StaticFiles(directory=str(static_path), html=True), name="app")

# Almacenamiento en memoria para demostración
security_events = []
anomaly_results = []
ml_models = {
    "isolation_forest": {"trained": False, "accuracy": 0.0},
    "dbscan": {"trained": False, "accuracy": 0.0},
    "pca": {"trained": False, "accuracy": 0.0}
}

# =============================================================================
# RUTAS PRINCIPALES
# =============================================================================

@app.get("/")
async def root(request: Request):
    """Raíz: devuelve JSON simple; si el cliente quiere HTML, redirige al dashboard."""
    accept = request.headers.get("accept", "")
    if "text/html" in accept and static_path.exists():
        return RedirectResponse(url="/app/")
    return {
        "name": "CyberAI Sentinel",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
    }

@app.options("/")
async def options_root():
    """Responder preflight CORS explícitamente en la raíz."""
    return JSONResponse(status_code=200, content={})

@app.get("/health")
async def health_check():
    """
    Health check del sistema
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "api": "running",
            "ml_engine": "running",
            "database": "simulated",
            "elasticsearch": "simulated"
        },
        "uptime": "active"
    }

@app.get("/api/v1/security/events")
async def get_security_events(
    limit: int = 100,
    offset: int = 0,
    event_type: Optional[str] = None,
    user_id: Optional[str] = None
):
    """
    Obtener eventos de seguridad con filtros
    """
    try:
        # Generar eventos de ejemplo si no hay datos
        if not security_events:
            generate_sample_events(50)
        
        # Filtrar eventos
        filtered_events = security_events.copy()
        
        if event_type:
            filtered_events = [e for e in filtered_events if e.get('event_type') == event_type]
        if user_id:
            filtered_events = [e for e in filtered_events if e.get('user_id') == user_id]
        
        # Aplicar paginación
        total = len(filtered_events)
        events = filtered_events[offset:offset + limit]
        
        return {
            "events": events,
            "total": total,
            "limit": limit,
            "offset": offset,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo eventos: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.post("/api/v1/security/analyze")
async def analyze_security_event(event_data: dict):
    """
    Analizar evento de seguridad con IA
    """
    try:
        # Simular análisis de IA
        analysis_id = f"analysis_{int(time.time())}"
        
        # Generar métricas simuladas
        anomaly_score = random.uniform(0.0, 1.0)
        confidence = random.uniform(0.7, 0.95)
        
        # Determinar nivel de amenaza
        if anomaly_score > 0.8:
            threat_level = "critical"
        elif anomaly_score > 0.5:
            threat_level = "high"
        elif anomaly_score > 0.2:
            threat_level = "medium"
        else:
            threat_level = "low"
        
        # Generar recomendaciones
        recommendations = generate_recommendations(threat_level)
        
        # Crear resultado
        result = {
            "analysis_id": analysis_id,
            "threat_level": threat_level,
            "confidence": confidence,
            "anomaly_score": anomaly_score,
            "is_anomaly": anomaly_score > 0.2,
            "recommendations": recommendations,
            "model_info": {
                "models_used": ["isolation_forest", "dbscan", "pca"],
                "version": "1.0.0",
                "trained": True
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Guardar evento y resultado
        security_events.append({
            "id": analysis_id,
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": event_data.get('user_id', 'unknown'),
            "ip_address": event_data.get('ip_address', '0.0.0.0'),
            "event_type": event_data.get('event_type', 'unknown'),
            "success": event_data.get('success', True),
            "response_time": event_data.get('response_time', 0.0),
            "bytes_transferred": event_data.get('bytes_transferred', 0),
            "hour_of_day": event_data.get('hour_of_day', 12),
            "day_of_week": event_data.get('day_of_week', 1)
        })
        
        anomaly_results.append({
            "id": analysis_id,
            "event_id": analysis_id,
            "is_anomaly": result["is_anomaly"],
            "anomaly_score": anomaly_score,
            "confidence_score": confidence,
            "threat_level": threat_level,
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "model_version": "1.0.0"
        })
        
        return result
        
    except Exception as e:
        logger.error(f"Error en análisis de seguridad: {e}")
        raise HTTPException(status_code=500, detail=f"Error en análisis: {str(e)}")

@app.get("/api/v1/ml/models")
async def get_ml_models():
    """
    Obtener información de modelos ML
    """
    try:
        return {
            "models": [
                {
                    "name": "isolation_forest",
                    "type": "anomaly_detection",
                    "version": "1.0.0",
                    "status": "active",
                    "trained": ml_models["isolation_forest"]["trained"],
                    "accuracy": ml_models["isolation_forest"]["accuracy"]
                },
                {
                    "name": "dbscan",
                    "type": "clustering",
                    "version": "1.0.0",
                    "status": "active",
                    "trained": ml_models["dbscan"]["trained"],
                    "accuracy": ml_models["dbscan"]["accuracy"]
                },
                {
                    "name": "pca",
                    "type": "dimensionality_reduction",
                    "version": "1.0.0",
                    "status": "active",
                    "trained": ml_models["pca"]["trained"],
                    "accuracy": ml_models["pca"]["accuracy"]
                }
            ],
            "system_status": {
                "is_trained": all(model["trained"] for model in ml_models.values()),
                "models_available": {name: True for name in ml_models.keys()},
                "total_models": len(ml_models)
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error obteniendo modelos ML: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.post("/api/v1/ml/train")
async def train_ml_models():
    """
    Entrenar modelos ML con datos sintéticos
    """
    try:
        # Simular entrenamiento
        training_samples = 2000
        
        # Actualizar estado de modelos
        for model_name in ml_models:
            ml_models[model_name]["trained"] = True
            ml_models[model_name]["accuracy"] = random.uniform(0.85, 0.98)
        
        return {
            "status": "success",
            "message": "Modelos entrenados correctamente",
            "training_samples": training_samples,
            "metrics": {
                "isolation_forest_accuracy": ml_models["isolation_forest"]["accuracy"],
                "dbscan_accuracy": ml_models["dbscan"]["accuracy"],
                "pca_accuracy": ml_models["pca"]["accuracy"],
                "overall_accuracy": sum(model["accuracy"] for model in ml_models.values()) / len(ml_models)
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error entrenando modelos: {e}")
        raise HTTPException(status_code=500, detail=f"Error entrenando: {str(e)}")

@app.get("/api/v1/security/anomalies")
async def get_anomalies(
    limit: int = 100,
    offset: int = 0,
    severity: Optional[str] = None
):
    """
    Obtener anomalías detectadas
    """
    try:
        # Filtrar anomalías por severidad
        filtered_anomalies = anomaly_results.copy()
        
        if severity:
            if severity == "high":
                filtered_anomalies = [a for a in filtered_anomalies if a.get('anomaly_score', 0) > 0.7]
            elif severity == "medium":
                filtered_anomalies = [a for a in filtered_anomalies if 0.3 < a.get('anomaly_score', 0) <= 0.7]
            elif severity == "low":
                filtered_anomalies = [a for a in filtered_anomalies if a.get('anomaly_score', 0) <= 0.3]
        
        # Aplicar paginación
        total = len(filtered_anomalies)
        anomalies = filtered_anomalies[offset:offset + limit]
        
        return {
            "anomalies": anomalies,
            "total": total,
            "limit": limit,
            "offset": offset,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo anomalías: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/api/v1/system/health")
async def get_system_health():
    """
    Obtener estado de salud del sistema
    """
    try:
        return {
            "status": "healthy",
            "services": {
                "database": "simulated",
                "ml_models": "active" if all(model["trained"] for model in ml_models.values()) else "inactive",
                "api": "running"
            },
            "database": {
                "status": "simulated",
                "connected": True,
                "events_count": len(security_events),
                "anomalies_count": len(anomaly_results)
            },
            "ml_models": {
                "is_trained": all(model["trained"] for model in ml_models.values()),
                "models_available": {name: True for name in ml_models.keys()},
                "total_models": len(ml_models)
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error verificando salud del sistema: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def generate_sample_events(count: int):
    """
    Generar eventos de ejemplo
    """
    event_types = ['login', 'logout', 'file_access', 'network_scan', 'data_transfer']
    users = [f'user_{i}' for i in range(1, 11)]
    ips = [f'192.168.1.{i}' for i in range(1, 255)]
    
    for i in range(count):
        event = {
            "id": f"event_{i+1}",
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": random.choice(users),
            "ip_address": random.choice(ips),
            "event_type": random.choice(event_types),
            "success": random.choice([True, True, True, False]),  # 75% éxito
            "response_time": random.uniform(0.1, 2.0),
            "bytes_transferred": random.randint(1024, 1048576),
            "hour_of_day": random.randint(0, 23),
            "day_of_week": random.randint(0, 6)
        }
        security_events.append(event)

def generate_recommendations(threat_level: str) -> list:
    """
    Generar recomendaciones basadas en el nivel de amenaza
    """
    if threat_level == "critical":
        return [
            "Bloquear IP inmediatamente",
            "Investigar actividad del usuario",
            "Revisar logs del sistema",
            "Notificar al equipo de seguridad"
        ]
    elif threat_level == "high":
        return [
            "Monitorear actividad del usuario",
            "Verificar integridad del sistema",
            "Revisar políticas de acceso"
        ]
    elif threat_level == "medium":
        return [
            "Monitorear actividad del usuario",
            "Verificar integridad del sistema"
        ]
    else:
        return [
            "Continuar monitoreo normal"
        ]

# =============================================================================
# MANEJO DE ERRORES
# =============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Manejo personalizado de errores HTTP
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Manejo general de errores
    """
    logger.error(f"Error no manejado: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url)
        }
    )

# =============================================================================
# EVENTOS DE APLICACIÓN
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Eventos de inicio de la aplicación
    """
    logger.info("Iniciando CyberAI Sentinel (Versión Simplificada)...")
    logger.info("Sistema de IA para Ciberseguridad")
    logger.info("Desarrollado por: Vicente Alonso")
    logger.info("Aplicación iniciada correctamente")

    # Mensaje de disponibilidad del dashboard
    if static_path.exists():
        logger.info("Dashboard estático disponible en /app/")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Eventos de cierre de la aplicación
    """
    logger.info("Cerrando CyberAI Sentinel...")
    logger.info("Aplicación cerrada correctamente")

# =============================================================================
# PUNTO DE ENTRADA PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    """
    Punto de entrada principal de la aplicación
    """
    print("CyberAI Sentinel - Sistema de IA para Ciberseguridad")
    print("Desarrollado por: Vicente Alonso")
    print("Email: jvab065@gmail.com")
    print("LinkedIn: linkedin.com/in/vicente-alonso-cybersecurity")
    print("=" * 60)
    print("VERSIÓN SIMPLIFICADA - FUNCIONANDO SIN BASE DE DATOS")
    print("=" * 60)
    
    # Ejecutar servidor
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )






