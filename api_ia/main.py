"""
API REST del Modelo de IA VESTIGO
==================================
Expone el modelo de recomendación de tallas y siluetas
a través de endpoints HTTP usando FastAPI.

Ejecutar con: uvicorn api_ia.main:app --reload
Documentación: http://127.0.0.1:8001/docs

Autor: Ronal + equipo VESTIGO
Fecha: Septiembre 2026
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import numpy as np
import os

# ============================================================
# 1. CONFIGURACIÓN DE LA API
# ============================================================
app = FastAPI(
    title="VESTIGO IA API",
    description="API del modelo de recomendación de tallas y siluetas para VESTIGO",
    version="1.0.0"
)

# Permitir que el frontend (Django) pueda consumir la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 2. CARGAR LOS MODELOS ENTRENADOS
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_MODELO_TALLA = os.path.join(BASE_DIR, 'modelo_ia', 'artefactos', 'modelo_talla.pkl')
RUTA_MODELO_SILUETA = os.path.join(BASE_DIR, 'modelo_ia', 'artefactos', 'modelo_silueta.pkl')

try:
    modelo_talla = joblib.load(RUTA_MODELO_TALLA)
    modelo_silueta = joblib.load(RUTA_MODELO_SILUETA)
    print("✓ Modelos cargados correctamente")
except FileNotFoundError as e:
    print(f"⚠ ERROR: No se encontró el modelo en {e}")
    modelo_talla = None
    modelo_silueta = None


# ============================================================
# 3. MODELOS DE DATOS (Pydantic)
# ============================================================
class MedidasCliente(BaseModel):
    """Medidas corporales del cliente (en centímetros)."""
    pecho: float = Field(..., ge=50, le=200, description="Circunferencia del pecho en cm")
    cintura: float = Field(..., ge=40, le=200, description="Circunferencia de la cintura en cm")
    cadera: float = Field(..., ge=50, le=200, description="Circunferencia de la cadera en cm")
    altura: float = Field(..., ge=120, le=220, description="Altura total en cm")

    class Config:
        json_schema_extra = {
            "example": {
                "pecho": 92,
                "cintura": 74,
                "cadera": 98,
                "altura": 168
            }
        }


class PrediccionTalla(BaseModel):
    """Respuesta del modelo de IA."""
    talla: str
    silueta: str
    confianza_talla: float
    confianza_silueta: float
    medidas_ingresadas: dict
    mensaje: str


# ============================================================
# 4. ENDPOINTS DE LA API
# ============================================================
@app.get("/")
def raiz():
    """Endpoint raíz: verifica que la API esté funcionando."""
    return {
        "api": "VESTIGO IA",
        "version": "1.0.0",
        "estado": "funcionando",
        "endpoints": {
            "predecir_talla": "POST /predecir-talla",
            "documentacion": "GET /docs",
            "healthcheck": "GET /health"
        }
    }


@app.get("/health")
def health_check():
    """Verifica que el modelo esté cargado correctamente."""
    return {
        "estado": "ok",
        "modelo_talla_cargado": modelo_talla is not None,
        "modelo_silueta_cargado": modelo_silueta is not None
    }


@app.post("/predecir-talla", response_model=PrediccionTalla)
def predecir_talla(medidas: MedidasCliente):
    """
    Predice la talla y silueta recomendada a partir de las medidas corporales.
    
    **Entrada:** medidas en cm (pecho, cintura, cadera, altura)
    
    **Salida:** talla recomendada + silueta + nivel de confianza
    """
    if modelo_talla is None or modelo_silueta is None:
        raise HTTPException(status_code=500, detail="Los modelos no están cargados")

    try:
        # Preparar los datos de entrada
        entrada = np.array([[
            medidas.pecho,
            medidas.cintura,
            medidas.cadera,
            medidas.altura
        ]])

        # Predecir talla
        talla_pred = modelo_talla.predict(entrada)[0]
        proba_talla = modelo_talla.predict_proba(entrada)[0]
        confianza_talla = float(max(proba_talla))

        # Predecir silueta
        silueta_pred = modelo_silueta.predict(entrada)[0]
        proba_silueta = modelo_silueta.predict_proba(entrada)[0]
        confianza_silueta = float(max(proba_silueta))

        # Generar mensaje personalizado
        if confianza_talla >= 0.9:
            nivel = "alta"
        elif confianza_talla >= 0.7:
            nivel = "media"
        else:
            nivel = "baja"

        mensaje = (
            f"Con tus medidas, te recomendamos la talla {talla_pred} "
            f"con silueta {silueta_pred}. "
            f"(Confianza: {nivel})"
        )

        return PrediccionTalla(
            talla=talla_pred,
            silueta=silueta_pred,
            confianza_talla=round(confianza_talla, 4),
            confianza_silueta=round(confianza_silueta, 4),
            medidas_ingresadas={
                "pecho": medidas.pecho,
                "cintura": medidas.cintura,
                "cadera": medidas.cadera,
                "altura": medidas.altura
            },
            mensaje=mensaje
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al predecir: {str(e)}")


# ============================================================
# 5. EJECUCIÓN DIRECTA
# ============================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)