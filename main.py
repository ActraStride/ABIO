from src.clients.gemini_client import GeminiClient  # Asegúrate de tener instalada la biblioteca adecuada
from src.utils.setup_logging import setup_logging  # Importa la función setup_logging
from src.chat.chat_session import ChatSession  # Importa la clase ChatSession
from pathlib import Path
import logging

def main():
    # Configuración avanzada de logging
    project_root = Path("/home/actra_dev/Desktop/ABIO")  # Define la raíz del proyecto
    setup_logging(log_level="INFO", project_root=project_root)  # Llama a setup_logging
    
    logger = logging.getLogger("GeminiChat")  # Obtén el logger con el nombre deseado
    
    try:
        # Inicializar el cliente de Gemini
        logger.info("Inicializando cliente de Gemini...")
        client = GeminiClient(logger=logger)
        
        # Crear una nueva sesión de chat
        session_id = "12345"  # Puedes generar un ID único si lo prefieres
        model_name = "models/gemini-1.5-flash"
        chat_session = ChatSession(session_id=session_id, model_name=model_name)
        logger.info("Sesión de chat iniciada con ID: %s", session_id)
        
        # Iniciar el bucle de chat
        print("Bienvenido al chat con el modelo Gemini. Escribe 'salir' para terminar la sesión.")
        while True:
            user_input = input("\nTú: ")
            if user_input.lower() == "salir":
                print("Terminando la sesión de chat. ¡Hasta luego!")
                break
            
            # Agregar el mensaje del usuario a la sesión
            chat_session.add_message(role="user", content=user_input)
            
            # Generar respuesta del modelo
            logger.info("Generando respuesta del modelo...")
            response = client.generate_text(prompt=user_input, model_name=model_name)
            # Acceder al texto generado correctamente
            if hasattr(response, "generated_text"):
                generated_text = response.generated_text
            else:
                generated_text = "Error: No se pudo generar una respuesta."
            
            
            # Agregar la respuesta del modelo a la sesión
            chat_session.add_message(role="assistant", content=generated_text)
            
            # Mostrar la respuesta al usuario
            print(f"\nGemini: {generated_text}")
        
        # Mostrar el historial de la sesión al final
        print("\nHistorial de la sesión:")
        for message in chat_session.get_history():
            print(f"{message.role.capitalize()}: {message.content}")
    
    except Exception as e:
        logger.error("Error durante la sesión de chat: %s", e)

if __name__ == "__main__":
    client = None
    try:
        client = GeminiClient(logger=logging.getLogger("GeminiChat"))
        main()
    except Exception as e:
        logging.getLogger("GeminiChat").error("Unexpected error: %s", e)
    finally:
        if client:
            client.close()