from src.clients.gemini_client import GeminiClient
from src.utils.setup_logging import setup_logging
from src.chat.chat_session import ChatSession
from src.config.agent_config import ConfigManager
from src.context import ContextManager
from pathlib import Path
import logging

from colorama import Fore, Style, init
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# Inicializa colorama
init(autoreset=True)
console = Console()

def main():
    # Configuración avanzada de logging
    project_root = Path("/home/actra_dev/Desktop/ABIO")
    setup_logging(log_level="INFO", project_root=project_root)

    logger = logging.getLogger("GeminiChat")

    try:
        # Mostrar cabecera visual
        console.print(Panel.fit("[bold cyan]🤖 Bienvenido al sistema de chat Gemini[/bold cyan]\nEscribe 'salir' para terminar la sesión.", title="Gemini CLI", subtitle="Actra Dev"))

        # Cargar configuración del agente
        config_manager = ConfigManager(config_path="Abiofile")  
        config = config_manager.get_config()
        logger.info("📄 Configuración cargada desde Abiofile:")
        logger.info(config)

        # Inicializar el cliente de Gemini
        logger.info("Inicializando cliente de Gemini...")
        client = GeminiClient()

        # Crear una nueva sesión de chat
        session_id = "12345"
        context_manager = ContextManager(config.context.message_limit, config.context.context_messages)
        chat_session = ChatSession(
            session_id=session_id,
            model_name=config.chat.default_model,
            client=client,
            context_manager=context_manager
        )

        logger.info(f"✅ Sesión de chat iniciada con ID: {session_id}")
        logger.info(f"🧠 Modelo activo: {config.chat.default_model}")

        # Bucle principal de chat
        while True:
            user_input = input(Fore.CYAN + "\nTú: ")
            if user_input.strip().lower() == "salir":
                print(Fore.YELLOW + "👋 Terminando la sesión de chat. ¡Hasta luego!")
                break

            chat_session.add_message(role="user", content=user_input)
            logger.info("💬 Generando respuesta del modelo...")

            try:
                response_message = chat_session.generate_response(prompt=user_input)
                print(Fore.GREEN + Style.BRIGHT + f"\n{config.agent.name}: {response_message.content}")
            except Exception as gen_error:
                logger.error("Error generando respuesta del modelo: %s", gen_error)
                print(Fore.RED + "⚠️ Ocurrió un error al generar la respuesta. Intenta de nuevo.")

        # Mostrar historial de la sesión
        console.print("\n📜 [bold]Historial de la sesión:[/bold]")
        for message in chat_session.get_history():
            role = message.role.capitalize()
            if message.role == "user":
                print(Fore.CYAN + f"{role}: {message.content}")
            else:
                print(Fore.GREEN + Style.BRIGHT + f"{role}: {message.content}")

    except Exception as e:
        logger.exception("❌ Error durante la sesión de chat")
        print(Fore.RED + f"Ocurrió un error inesperado: {e}")

    finally:
        if 'client' in locals() and client:
            client.close()
            logger.info("🔒 Cliente Gemini cerrado correctamente.")

if __name__ == "__main__":
    main()
