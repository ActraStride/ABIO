# ISSUE_7.md

## EMBEDDINGS Y FAISS PARA GESTIÓN CONTEXTUAL MEJORADA [#7]

### Objetivo  
Integrar un módulo de embeddings y gestión vectorial con FAISS para mejorar la capacidad del agente de chat para manejar y enriquecer el contexto. Esto permitirá al agente almacenar, recuperar y utilizar representaciones vectorizadas de datos, posibilitando respuestas más inteligentes y conscientes del contexto.

### Solución Propuesta

#### 1. Integración del Módulo de Embeddings  
- Desarrollar un módulo para generar embeddings de textos utilizando modelos preentrenados  
- Hacer el módulo configurable (selección de modelo, dimensionalidad, etc.)  
- Crear una interfaz similar a `gemini_client` que abstraiga la complejidad  

#### 2. Implementación de Gestión Vectorial con FAISS  
- Utilizar FAISS para el almacenamiento y gestión de embeddings  
- Implementar funcionalidades clave:
  - Añadir nuevos embeddings al almacén vectorial  
  - Buscar los embeddings más relevantes por similitud  
  - Eliminar embeddings obsoletos o irrelevantes  
- Contemplar estrategias de persistencia y uso de metadatos  

#### 3. Mejora del Manejo de Contexto  
- Modificar el agente de chat para consultar la base de datos vectorial  
- Enriquecer el contexto actual con información relevante recuperada  
- Actualizar el `ContextManager` para incorporar los datos recuperados  

#### 4. Optimización de Rendimiento  
- Garantizar que la búsqueda vectorial sea eficiente incluso con grandes conjuntos de datos  
- Implementar mecanismos de procesamiento por lotes o caché si es necesario  
- Considerar estrategias de índices FAISS según el volumen de datos  

### Estructura Propuesta

```
src/
  embeddings/
    embeddings_client.py   # Cliente para generar embeddings
    vector_store.py        # Gestión de índices FAISS
    utils.py               # Funciones auxiliares
  models/
    vector_data.py         # Modelos para metadatos y resultados
  context/
    context_enrichment.py  # Lógica para enriquecer el contexto
```

### Modificaciones al Esquema de Configuración

```yaml
# Nuevas secciones a añadir en AbioConfig
embeddings:
  provider: "openai"  # Alternativas: "gemini", "huggingface"
  model: "text-embedding-3-small"
  dimensions: 1536
  
vector_store:
  type: "faiss"
  index_type: "IndexFlatL2"  # Alternativas: "IndexIVFFlat", "IndexHNSW"
  path: "./data/vector_store"
  metadata_db: "./data/metadata.db"
  top_k: 5  # Número predeterminado de resultados a recuperar
```

### Flujo de Trabajo

1. El usuario envía una consulta  
2. Se genera un embedding para la consulta  
3. Se buscan vectores similares en el almacén FAISS  
4. Se recuperan los metadatos asociados (texto original)  
5. Se enriquece el contexto actual con la información recuperada  
6. Se genera una respuesta utilizando el contexto enriquecido  

### Beneficios Esperados

- Mejora significativa en la calidad y relevancia de las respuestas  
- Capacidad para incorporar conocimiento específico en las conversaciones  
- Sistema modular y reutilizable para vectorización y recuperación  
- Mayor escalabilidad para manejar grandes volúmenes de información  

### Próximos Pasos

1. Implementar el cliente de embeddings con soporte multiproveedor  
2. Desarrollar el módulo de gestión vectorial con FAISS  
3. Integrar la recuperación vectorial en el flujo de conversación  
4. Escribir pruebas unitarias y de integración  
5. Evaluar el rendimiento y la calidad de las respuestas  

### Referencias

- [FAISS Documentation](https://github.com/facebookresearch/faiss/wiki)  
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/index)  
- [OpenAI Embeddings API](https://platform.openai.com/docs/guides/embeddings)  

### Prioridad  
Alta 


## Módulo de Embeddings: Una explicación a fondo

### Estructura recomendada

En lugar de llamarlo "cliente", podemos nombrarlo más apropiadamente:

```
src/
  embeddings/
    embeddings_generator.py   # Generador de embeddings usando SentenceTransformers
    vector_store.py           # Gestión del índice FAISS y metadatos
    utils.py                  # Funciones auxiliares para procesamiento de textos
```

### El módulo `embeddings_generator.py`

Este módulo tendría como responsabilidad principal transformar texto en representaciones vectoriales (embeddings).

```python
# embeddings_generator.py
from sentence_transformers import SentenceTransformer
from typing import List, Union, Optional
import numpy as np

class EmbeddingsGenerator:
    """
    Generador de embeddings utilizando modelos de SentenceTransformers.
    Transforma texto en representaciones vectoriales que capturan significado semántico.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Inicializa el generador de embeddings con un modelo específico.
        
        Args:
            model_name: Nombre del modelo de SentenceTransformers a utilizar.
                        Por defecto usa all-MiniLM-L6-v2 (384 dimensiones).
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        # Dimensión del espacio vectorial (específica del modelo)
        self.dimension = self.model.get_sentence_embedding_dimension()
        
    def generate(self, text: Union[str, List[str]], 
                 batch_size: int = 32) -> np.ndarray:
        """
        Genera embeddings para un texto o lista de textos.
        
        Args:
            text: Un string o lista de strings para vectorizar
            batch_size: Tamaño del lote para procesamiento eficiente
            
        Returns:
            Array numpy con los embeddings generados. Si la entrada es un solo
            texto, retorna un vector 1D. Si es una lista, retorna una matriz 2D.
        """
        return self.model.encode(text, batch_size=batch_size)
        
    def get_dimension(self) -> int:
        """
        Retorna la dimensión del espacio vectorial del modelo.
        
        Returns:
            Número entero con la dimensión de los vectores generados.
        """
        return self.dimension
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocesa el texto antes de generar embeddings.
        
        Args:
            text: Texto a preprocesar
            
        Returns:
            Texto preprocesado
        """
        # Preprocesamiento básico - puedes expandir según necesidades
        text = text.strip()
        # Opcional: normalización, eliminación de caracteres especiales, etc.
        return text
    
    def segment_text(self, text: str, max_length: int = 512) -> List[str]:
        """
        Segmenta textos largos en fragmentos más manejables.
        
        Args:
            text: Texto largo a segmentar
            max_length: Longitud aproximada máxima por segmento
            
        Returns:
            Lista de segmentos de texto
        """
        # Implementación básica - puedes mejorarla con técnicas más sofisticadas
        # que mantengan contexto o divisiones semánticas
        words = text.split()
        segments = []
        current_segment = []
        
        for word in words:
            current_segment.append(word)
            if len(' '.join(current_segment)) >= max_length:
                segments.append(' '.join(current_segment))
                current_segment = []
                
        if current_segment:
            segments.append(' '.join(current_segment))
            
        return segments
```

### Explicación detallada

#### Propósito del módulo

El módulo `EmbeddingsGenerator` tiene la responsabilidad de:

1. **Transformar texto a vectores**: Convertir lenguaje natural en representaciones matemáticas que capturan el significado semántico.

2. **Gestionar el modelo subyacente**: Encapsular la complejidad del modelo de embeddings, proporcionando una interfaz simple.

3. **Preprocesar y segmentar textos**: Ofrecer funcionalidades para preparar los textos antes de la vectorización.

#### Componentes clave

##### Método `generate()`

Este es el método principal que convierte texto en embeddings:

- **Funcionalidad**: Transforma texto o listas de textos en vectores numéricos.
- **Flexibilidad**: Acepta tanto cadenas únicas como listas de textos.
- **Eficiencia**: Utiliza procesamiento por lotes (batching) para optimizar rendimiento.
- **Salida**: Devuelve arrays numpy que son compatibles directamente con FAISS.

##### Método `segment_text()`

Este método resuelve un problema común: los textos largos necesitan ser divididos en fragmentos más pequeños para obtener embeddings efectivos:

- **Propósito**: Dividir documentos largos en fragmentos más cortos.
- **Importancia**: Los modelos de embeddings tienen límites en la longitud de texto que pueden procesar efectivamente.
- **Enfoque simple**: La implementación básica divide por cantidad de palabras.
- **Mejoras posibles**: Se podría mejorar para dividir en párrafos o unidades semánticas.

##### Método `preprocess_text()`

Prepara el texto para obtener mejores embeddings:

- **Normalización**: Eliminación de espacios innecesarios, caracteres especiales.
- **Expansibilidad**: Puedes añadir pasos adicionales como normalización de casing, eliminación de stopwords, etc.

#### Consideraciones técnicas

1. **Rendimiento**: El módulo está diseñado pensando en el rendimiento, utilizando batching para procesamiento eficiente.

2. **Memoria**: Los modelos de embeddings pueden ocupar bastante RAM (100MB-1GB dependiendo del modelo).

3. **Dimensionalidad**: 
   - all-MiniLM-L6-v2: 384 dimensiones (buen equilibrio entre calidad y eficiencia)
   - all-mpnet-base-v2: 768 dimensiones (mayor calidad pero más pesado)

4. **Tipado**: Se utiliza typing para documentar claramente los tipos de entrada/salida.

### Uso práctico

Este módulo se utilizaría generalmente en dos escenarios:

1. **Indexación**: Cuando procesas documentos para almacenarlos en tu base vectorial:

```python
# Ejemplo de indexación de documentos
embeddings_gen = EmbeddingsGenerator()
vector_store = VectorStore(dimension=embeddings_gen.get_dimension())

document = "Texto largo sobre algún tema específico..."
segments = embeddings_gen.segment_text(document)

for segment in segments:
    processed_segment = embeddings_gen.preprocess_text(segment)
    embedding = embeddings_gen.generate(processed_segment)
    vector_store.add(processed_segment, embedding, metadata={"source": "documento1.txt"})
```

2. **Consulta**: Cuando necesitas vectorizar una consulta para buscar similitudes:

```python
# Ejemplo de búsqueda
query = "¿Qué es la inteligencia artificial?"
query_processed = embeddings_gen.preprocess_text(query)
query_embedding = embeddings_gen.generate(query_processed)

results = vector_store.search(query_embedding, top_k=3)
```