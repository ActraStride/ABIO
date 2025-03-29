from src.clients.gemini_client import GeminiClient  # Asegúrate de tener instalada la biblioteca adecuada
from src.utils.setup_logging import setup_logging  # Importa la función setup_logging
from pathlib import Path
import logging

def main():
    # Configuración avanzada de logging
    project_root = Path("/home/actra_dev/Desktop/ABIO")  # Define la raíz del proyecto
    setup_logging(log_level="INFO", project_root=project_root)  # Llama a setup_logging
    
    logger = logging.getLogger("GeminiTest")  # Obtén el logger con el nombre deseado
    
    try:
        # Inicializar el cliente de Gemini
        logger.info("Inicializando cliente de Gemini...")
        client = GeminiClient(logger=logger)
        
        # Listar modelos disponibles
        models = client.list_models()
        logger.info("Modelos disponibles: %s", models)
        print("Modelos disponibles:")
        for model in models:
            print(f"- {model}")
        
        # Generar texto con un modelo específico
        if models:
            prompt = "Escribe un poema sobre la tecnología."
            logger.info("Generando texto con el modelo: %s", models[17])
            print("\nGenerando texto con el modelo:", models[17])
            response = client.generate_text(prompt=prompt, model_name=models[17])
            logger.info("Texto generado: %s", response)
            print("\nTexto generado:")
            print(response)
        else:
            logger.warning("No hay modelos disponibles para generar contenido.")
            print("No hay modelos disponibles para generar contenido.")
    except Exception as e:
        logger.error("Error durante la prueba del cliente de Gemini: %s", e)

if __name__ == "__main__":
    main()
