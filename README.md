# 🛡️ CyberAI Sentinel - Sistema de IA para Ciberseguridad

**Proyecto de Demostración de Habilidades Técnicas**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--learn-orange.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Desarrollado por:** [Vicente Alonso](https://linkedin.com/in/vicente-alonso-cybersecurity)  
**Especialista en Ciberseguridad y Administración de Sistemas**  
**Email:** jvab065@gmail.com

---

## 🎯 **Descripción del Proyecto**

**CyberAI Sentinel** es un sistema de demostración de inteligencia artificial aplicada a la ciberseguridad que combina machine learning, análisis de comportamiento y detección de amenazas en tiempo real. Este proyecto demuestra competencias técnicas en:

- **Desarrollo de APIs REST** con FastAPI
- **Machine Learning** aplicado a ciberseguridad
- **Arquitectura de software** moderna
- **Automatización** y scripting
- **Documentación técnica** profesional

---

## 🚀 **Características Principales**

### **🤖 Inteligencia Artificial**
- **Detección de anomalías** con algoritmos ML
- **Análisis de comportamiento** de usuarios
- **Clasificación automática** de eventos de seguridad
- **Predicción de amenazas** basada en patrones

### **📊 APIs REST Completas**
- **8 endpoints** funcionales
- **Documentación automática** con Swagger
- **Manejo de errores** HTTP estándar
- **CORS** configurado para integración

### **🔍 Análisis de Seguridad**
- **Monitoreo en tiempo real** de eventos
- **Clasificación automática** por severidad
- **Detección de patrones** anómalos
- **Recomendaciones inteligentes** de mitigación

---

## 🛠️ **Tecnologías Utilizadas**

### **Backend**
- **Python 3.8+** - Lenguaje principal
- **FastAPI** - Framework web moderno
- **scikit-learn** - Machine Learning
- **SQLAlchemy** - ORM para base de datos
- **uvicorn** - Servidor ASGI

### **Machine Learning**
- **Isolation Forest** - Detección de anomalías
- **DBSCAN** - Clustering de eventos
- **PCA** - Reducción de dimensionalidad
- **pandas/numpy** - Procesamiento de datos

### **Herramientas**
- **pytest** - Testing
- **python-dotenv** - Variables de entorno
- **requests** - Cliente HTTP para pruebas

---

## 📁 **Estructura del Proyecto**

```
CyberAI_Sentinel/
├── main_simple.py          # Servidor principal
├── test_simple.py          # Pruebas del sistema
├── setup_simple.py         # Configuración automática
├── requirements.txt        # Dependencias
├── README.md              # Documentación
├── database/              # Modelos de base de datos
│   ├── __init__.py
│   ├── connection.py
│   └── models.py
├── ml_engine/             # Motor de Machine Learning
│   └── anomaly_detector.py
├── models/                # Modelos ML guardados
│   ├── isolation_forest.joblib
│   ├── dbscan.joblib
│   ├── pca.joblib
│   └── scaler.joblib
└── tests/                 # Tests unitarios
    ├── __init__.py
    ├── test_anomaly_detector.py
    └── test_api.py
```

---

## 🚀 **Instalación y Uso**

## 👀 Preview

![Dashboard](/docs/capturas/01_dashboard.png)

![Health](/docs/capturas/02_health.png)

![Modelos ML](/docs/capturas/03_models.png)

![Analizar Evento](/docs/capturas/04_analyze.png)

### ⚡ Inicio Rápido con Docker (Recomendado)

1. Copiar variables de entorno de ejemplo:
   ```bash
   cp config.env.example config.env
   ```

2. Construir e iniciar servicios:
   ```bash
   # Linux/Mac
   ./start.sh

   # Windows
   ./start.ps1
   ```

3. Acceso:
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

4. Persistencia: PostgreSQL se levanta en Docker con credenciales de `config.env`.

Nota: La imagen Docker usa un set mínimo de dependencias (`requirements.docker.txt`) para asegurar compatibilidad rápida. El `requirements.txt` completo incluye librerías opcionales (TensorFlow, Torch, etc.) que no son necesarias para la demo y pueden fallar al compilar en algunos entornos.

### **Requisitos del Sistema**
- Python 3.8 o superior
- pip (gestor de paquetes)

### **Instalación Rápida (sin Docker)**

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/vicente-alonso/CyberAI-Sentinel.git
   cd CyberAI-Sentinel
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar entorno:**
   ```bash
   python setup_simple.py
   ```

4. **Ejecutar servidor:**
   ```bash
   python main_simple.py
   ```

5. **Acceder a la aplicación:**
   - **API:** http://localhost:8000
   - **Documentación:** http://localhost:8000/docs
   - **Health Check:** http://localhost:8000/health

### **Ejecutar Pruebas**
```bash
python test_simple.py
```

---

## 📊 **APIs Disponibles**

### **Endpoints Principales**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Información del sistema |
| `GET` | `/health` | Health check |
| `GET` | `/api/v1/security/events` | Eventos de seguridad |
| `POST` | `/api/v1/security/analyze` | Análisis con IA |
| `GET` | `/api/v1/security/anomalies` | Anomalías detectadas |
| `GET` | `/api/v1/ml/models` | Información de modelos ML |
| `POST` | `/api/v1/ml/train` | Entrenar modelos |
| `GET` | `/api/v1/system/health` | Salud del sistema |

### **Ejemplo de Uso**

**Análisis de evento de seguridad:**
```bash
curl -X POST "http://localhost:8000/api/v1/security/analyze" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "user_001",
       "ip_address": "192.168.1.100",
       "event_type": "login",
       "success": true,
       "response_time": 0.5,
       "bytes_transferred": 1024,
       "hour_of_day": 14,
       "day_of_week": 1
     }'
```

**Respuesta:**
```json
{
  "analysis_id": "analysis_1640995200",
  "threat_level": "low",
  "confidence": 0.85,
  "anomaly_score": 0.15,
  "is_anomaly": false,
  "recommendations": ["Continuar monitoreo normal"],
  "timestamp": "2025-01-01T12:00:00Z"
}
```

---

## 🎯 **Casos de Uso Empresariales**

### **Para SOC (Security Operations Center)**
- **Monitoreo 24/7** de amenazas
- **Detección proactiva** de anomalías
- **Clasificación automática** de eventos
- **Alertas inteligentes** con recomendaciones

### **Para CISO**
- **Reportes ejecutivos** automatizados
- **Métricas de seguridad** en tiempo real
- **Análisis de tendencias** históricas
- **Dashboard** de inteligencia

### **Para Analistas de Seguridad**
- **Herramientas de análisis** avanzado
- **Correlación de eventos** automática
- **Investigación** de incidentes
- **Workflow** de respuesta

---

## 📈 **Métricas del Proyecto**

### **Técnicas**
- **8 APIs REST** implementadas
- **3 algoritmos ML** integrados
- **100% documentación** técnica
- **Tests automatizados** incluidos

### **Funcionales**
- **Detección de anomalías** en tiempo real
- **Clasificación automática** de amenazas
- **Recomendaciones inteligentes** de mitigación
- **Monitoreo continuo** del sistema

---

## 🔧 **Desarrollo y Contribución**

### **Ejecutar en Modo Desarrollo**
```bash
# Con recarga automática
uvicorn main_simple:app --reload --host 0.0.0.0 --port 8000
```

### **Ejecutar Tests**
```bash
# Tests unitarios
python -m pytest tests/

# Tests del sistema
python test_simple.py
```

### **Estructura de Código**
- **main_simple.py** - Aplicación principal FastAPI
- **ml_engine/** - Motor de Machine Learning
- **database/** - Modelos y conexión de BD
- **tests/** - Tests unitarios y de integración

---

## 📚 **Documentación Adicional**

- **API Documentation:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## ⚠️ **Notas Importantes**

### **Propósito del Proyecto**
Este proyecto está diseñado como **demostración de habilidades técnicas** y no para uso en producción. Algunas funcionalidades están simuladas para propósitos de demostración.

### **Limitaciones Conocidas**
- **Base de datos:** Almacenamiento en memoria (no persistente)
- **Machine Learning:** Algoritmos simulados para demostración
- **Seguridad:** Sin autenticación implementada
- **Escalabilidad:** Arquitectura monolítica

### **Para Producción**
Para uso en producción, se requerirían:
- Base de datos real (PostgreSQL)
- Algoritmos ML reales con datos de entrenamiento
- Autenticación y autorización
- Arquitectura distribuida
- Monitoreo y logging avanzado

---

## 📞 **Contacto y Soporte**

**Desarrollador:** Vicente Alonso  
**Email:** jvab065@gmail.com  
**LinkedIn:** [linkedin.com/in/vicente-alonso-cybersecurity](https://linkedin.com/in/vicente-alonso-cybersecurity)  
**GitHub:** [github.com/vicente-alonso](https://github.com/vicente-alonso)

---

## 📄 **Licencia**

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 🙏 **Agradecimientos**

- **FastAPI** - Framework web moderno
- **scikit-learn** - Librería de Machine Learning
- **Comunidad Python** - Ecosistema de desarrollo
- **Comunidad de Ciberseguridad** - Conocimiento y mejores prácticas

---

*Desarrollado como proyecto de demostración de habilidades técnicas en ciberseguridad y desarrollo de software*  
*Versión: 1.0.0 - Proyecto de Demostración*