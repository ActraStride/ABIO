from src.clients.gemini_client import GeminiClient  # Cliente Gemini
from src.utils.setup_logging import setup_logging  # Logging
from src.chat.chat_session import ChatSession  # Sesiones de chat
from src.config.agent_config import ConfigManager  # <--- Aquí importamos el ConfigManager
from src.context import ContextManager  # Contexto de la conversación
from pathlib import Path
import logging

from colorama import Fore, Style, init
from pprint import pprint

# Inicializa colorama
init(autoreset=True)

def main():
    # Configuración avanzada de logging
    project_root = Path("/home/actra_dev/Desktop/ABIO")  # Define la raíz del proyecto
    setup_logging(log_level="INFO", project_root=project_root)
    
    logger = logging.getLogger("GeminiChat")
    
    try:
         # Inicialización y carga de configuración
        config_manager = ConfigManager(config_path="Abiofile")  
        config = config_manager.get_config()
        logger = logging.getLogger("GeminiChat")
        logger.info("📄 Configuración cargada desde Abiofile:")
        logger.info(config)
        
        # Inicializar el cliente de Gemini
        logger.info("Inicializando cliente de Gemini...")
        client = GeminiClient()
        
        # Crear una nueva sesión de chat
        session_id = "12345"
        context_manager = ContextManager(config.context.message_limit, config.context.context_messages)

        chat_session = ChatSession(session_id=session_id, model_name=config.chat.default_model, client=client, context_manager=context_manager)
        logger.info("Sesión de chat iniciada con ID: %s", session_id)

        # TODO: IMPLEMENTAR UNA FUNCION DE ARRANQUE PARA CARGAR EL CONTEXTO EN EL MODELO
        
        
        # Iniciar el bucle de chat
        print("Bienvenido al chat con el modelo Gemini. Escribe 'salir' para terminar la sesión.")
        while True:
            user_input = input(Fore.CYAN + "\nTú: ")  # Respuesta del usuario en cyan
            if user_input.lower() == "salir":
                print(Fore.YELLOW + "Terminando la sesión de chat. ¡Hasta luego!")
                break
            
            chat_session.add_message(role="user", content=user_input)
            logger.info("Generando respuesta del modelo...")
            response_message = chat_session.generate_response(prompt=user_input)
            print(Fore.GREEN + Style.BRIGHT + f"\nGemini: {response_message.content}")  # Respuesta del modelo en verde y brillante (simulando cursiva)
        
        # Mostrar el historial de la sesión
        print("\nHistorial de la sesión:")
        for message in chat_session.get_history():
            if message.role == "user":
                print(Fore.CYAN + f"{message.role.capitalize()}: {message.content}")  # Respuesta del usuario en cyan
            else:
                print(Fore.GREEN + Style.BRIGHT + f"{message.role.capitalize()}: {message.content}")  # Respuesta del modelo en verde brillante

    except Exception as e:
        logger.error("Error durante la sesión de chat: %s", e)

if __name__ == "__main__":
    client = None
    try:
        client = GeminiClient()
        main()
    except Exception as e:
        logging.getLogger("GeminiChat").error("Unexpected error: %s", e)
    finally:
        if client:
            client.close()
