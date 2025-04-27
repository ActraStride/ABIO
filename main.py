from src.services.abio_service import ABIOService
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
    logger = logging.getLogger("ABIO_CLI")
    
    try:
        # Mostrar cabecera visual
        console.print(Panel.fit("[bold cyan]🤖 Bienvenido al sistema de chat Actra[/bold cyan]\nEscribe 'salir' para terminar la sesión.", title="Actra CLI", subtitle="Actra Dev"))

        # Inicializar el servicio ABIO
        service = ABIOService().initialize()
        logger.info("🚀 Servicio ABIO inicializado correctamente")
        
        # Crear una nueva sesión de chat
        session_id = service.create_session()
        config = service.config
        
        logger.info(f"✅ Sesión de chat iniciada con ID: {session_id}")
        logger.info(f"🧠 Modelo activo: {config.chat.default_model}")

        # Bucle principal de chat
        while True:
            user_input = input(Fore.CYAN + "\nTú: ")
            if user_input.strip().lower() == "salir":
                print(Fore.YELLOW + "👋 Terminando la sesión de chat. ¡Hasta luego!")
                break

            try:
                # Usar el servicio para enviar mensajes
                response_message = service.send_message(session_id, user_input)
                print(Fore.GREEN + Style.BRIGHT + f"\n{config.agent.name}: {response_message.content}")
            except Exception as gen_error:
                logger.error("Error generando respuesta del modelo: %s", gen_error)
                print(Fore.RED + "⚠️ Ocurrió un error al generar la respuesta. Intenta de nuevo.")

        # Mostrar historial de la sesión
        history = service.get_history(session_id)
        console.print("\n📜 [bold]Historial de la sesión:[/bold]")
        for message in history:
            role = message.role.capitalize()
            if message.role == "user":
                print(Fore.CYAN + f"{role}: {message.content}")
            else:
                print(Fore.GREEN + Style.BRIGHT + f"{role}: {message.content}")

    except Exception as e:
        logger.exception("❌ Error durante la sesión de chat")
        print(Fore.RED + f"Ocurrió un error inesperado: {e}")

    finally:
        if 'service' in locals():
            service.shutdown()
            logger.info("🔒 Servicio ABIO cerrado correctamente")

if __name__ == "__main__":
    main()
