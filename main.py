from src.clients.gemini_client import GeminiClient  # Asegúrate de tener instalada la biblioteca adecuada
import logging

def main():
    # Configuración básica
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("GeminiTest")
    
    try:
        # Inicializar el cliente de Gemini
        client = GeminiClient(logger=logger)
        
        # Listar modelos disponibles
        models = client.list_models()
        print("Modelos disponibles:")
        for model in models:
            print(f"- {model}")
        
        # Generar texto con un modelo específico
        if models:
            prompt = "Escribe un poema sobre la tecnología."
            print("\nGenerando texto con el modelo:", models[17])
            response = client.generate_text(prompt=prompt, model_name=models[17])
            print("\nTexto generado:")
            print(response)
        else:
            print("No hay modelos disponibles para generar contenido.")
    except Exception as e:
        logger.error("Error durante la prueba del cliente de Gemini: %s", e)

if __name__ == "__main__":
    main()
