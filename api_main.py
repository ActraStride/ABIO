# En ABIOService, crea api_main.py

from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Dict, Any
import json
import logging

# Importa tu clase de servicio. La ruta podría variar.
from src.services.abio_service import ABIOService 

# --- Configuración inicial ---
app = FastAPI(
    title="ABIO Service",
    description="Servicio de IA conversacional y de extracción de entidades."
)

# Inicializa tu servicio UNA SOLA VEZ cuando la aplicación arranca.
# Esto es muy importante para la eficiencia.
try:
    abio_service = ABIOService(config_path="Abiofile").initialize()
    logging.info("🚀 ABIOService inicializado y listo para recibir peticiones.")
except Exception as e:
    logging.critical(f"🔥🔥🔥 FALLO CRÍTICO AL INICIAR ABIOService: {e}")
    # En un caso real, esto debería detener el arranque de la aplicación.
    abio_service = None

# --- Modelos de datos para la API (Pydantic) ---
class ChatRequest(BaseModel):
    message: str

# --- Endpoints de la API ---

@app.post("/session", status_code=201)
def create_session() -> Dict[str, str]:
    """Crea una nueva sesión de chat y devuelve su ID."""
    if not abio_service:
        raise HTTPException(status_code=503, detail="El servicio de IA no está disponible.")
    session_id = abio_service.create_session()
    return {"session_id": session_id}

@app.post("/chat/{session_id}")
def chat_with_session(session_id: str, request: ChatRequest) -> Dict[str, Any]:
    """Envía un mensaje a una sesión existente y obtiene una respuesta estructurada."""
    if not abio_service:
        raise HTTPException(status_code=503, detail="El servicio de IA no está disponible.")
    try:
        response_message = abio_service.send_message(session_id, request.message)
        
        # --- Lógica para interpretar la respuesta de la IA ---
        # Intentamos parsear la respuesta como si fuera el JSON estructurado que esperamos.
        try:
            # Buscamos el bloque ```json ... ``` que le pedimos a la IA
            json_block = response_message.content.split("```json")[1].split("```")[0]
            structured_response = json.loads(json_block)
            return structured_response
        except (IndexError, json.JSONDecodeError):
            # Si no es un JSON estructurado, es un mensaje de chat normal.
            return {
                "response_type": "CHAT_MESSAGE",
                "payload": {"message_for_user": response_message.content}
            }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/session/{session_id}", status_code=204)
def close_session(session_id: str):
    """Cierra y elimina una sesión de chat."""
    if not abio_service:
        return # Si el servicio no está, no hay nada que hacer.
    abio_service.close_session(session_id)
    return None