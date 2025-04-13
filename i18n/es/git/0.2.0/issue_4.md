# JOURNAL.md

## Gestión de Configuración para Ajustes del Agente de Chat [#4]

### Objetivo

**Investigar cómo usar los parámetros del archivo de configuración actual (ver abajo) para construir un módulo de gestión de configuración.**  
Este módulo debe contener funciones que construyan el objeto de configuración para compartirlo entre diferentes componentes vía el módulo de servicio.

### Ejemplo de Archivo de Configuración (`Abiofile`)

```yaml
# Archivo de configuración general para el agente IA - Abiofile

agent:
  name: "<AGENT_NAME>"                          # (str) Nombre del agente IA.
  version: "<VERSION>"                          # (str) Número de versión del agente (ej: 1.0.0).
  description: "<AGENT_DESCRIPTION>"            # (str) Descripción breve de la funcionalidad del agente.
  environment: "<development|production|test>"  # (str) Entorno de ejecución del agente.

chat:
  message_limit: <CONTEXT_MESSAGE_LIMIT>        # (int) Número máximo de mensajes a retener en el contexto (ej: 50).
  default_model: "<AI_MODEL_NAME>"              # (str) Modelo IA predeterminado (ej: gemini-1.5-flash).
  temperature: <FLOAT_VALUE_BETWEEN_0_AND_1>    # (float) Temperatura de muestreo para controlar la aleatoriedad. Valores altos = más creatividad.
  top_p: <FLOAT_VALUE_BETWEEN_0_AND_1>          # (float) Parámetro de muestreo por núcleo. Valores bajos = resultados más enfocados.

  pretraining_prompts:
    - role: "system"                            # (str) Rol del hablante. Usar "system" para definir comportamiento inicial.
      content: "<INITIAL_SYSTEM_MESSAGE>"       # (str) Instrucciones iniciales o reglas del sistema para la IA.
    - role: "user"                              # (str) Rol del usuario que inicia la primera interacción.
      content: "<INITIAL_USER_QUESTION>"        # (str) Pregunta inicial para guiar el comportamiento del agente.

meta:
  created_by: "<YOUR_NAME>"                     # (str) Autor del archivo de configuración.
  created_at: "<CREATION_DATE>"                 # (str) Fecha de creación (ej: 2025-04-13).
  last_updated: "<LAST_UPDATE_DATE>"            # (str) Fecha de última modificación.
```

---

### ¿Qué es un `ABIO_CONFIG_OBJECT` y cómo se construye?

El `ABIO_CONFIG_OBJECT` es un formato estandarizado usado para construir el agente IA, su **comportamiento preentrenado** y **memoria**, junto con otros ajustes esenciales como:

- Límites de conversación  
- Selección de modelo  
- Ajustes de temperatura y muestreo  
- Metadatos adicionales

El módulo de configuración debe poder construir este objeto desde el archivo de configuración `abio` **o independientemente** (sin requerir el archivo).

---

### Desarrollo de la Clase `CONFIG_MANAGER`

La clase `CONFIG_MANAGER` presenta varias preguntas abiertas:

- ¿Cómo manejar el objeto de configuración?
- ¿Es apropiado ubicarlo en la carpeta `models`?
- ¿Cómo estructurar el objeto de configuración?
- ¿Qué estructura debería tener la clase `CONFIG_MANAGER`?

A continuación un prototipo básico para explorar estas cuestiones:

---

### Versión Primitiva de la Clase `AbioConfig`

```python
class AbioConfig:
    def __init__(self, agent, chat, meta):
        self.agent = agent
        self.chat = chat
        self.meta = meta

    def to_dict(self):
        """
        Convierte el objeto de configuración en un diccionario.
        """
        return {
            'agent': self.agent,
            'chat': self.chat,
            'meta': self.meta
        }
```

---

### Prototipo de la Clase `ConfigManager`

```python
import yaml

class ConfigManager:
    _config_instance = None  # Patrón Singleton: mantiene la única instancia de la configuración

    @staticmethod
    def load_configuration(file_path=None):
        """
        Carga la configuración desde un archivo YAML o crea una predeterminada.
        """
        if file_path:
            return ConfigManager._load_from_file(file_path)
        else:
            return ConfigManager._create_default_config()

    @staticmethod
    def _load_from_file(file_path):
        """
        Carga la configuración desde un archivo YAML y construye un objeto AbioConfig.
        """
        with open(file_path, 'r') as file:
            config_data = yaml.safe_load(file)

        return AbioConfig(
            agent=config_data['agent'],
            chat=config_data['chat'],
            meta=config_data['meta']
        )

    @staticmethod
    def _create_default_config():
        """
        Construye una configuración predeterminada si no se provee archivo.
        """
        return AbioConfig(
            agent={
                "name": "Abio",
                "version": "1.0.0",
                "description": "AI Agent",
                "environment": "development"
            },
            chat={
                "message_limit": 50,
                "default_model": "gemini-1.5-flash",
                "temperature": 0.7,
                "top_p": 0.9,
                "pretraining_prompts": []
            },
            meta={
                "created_by": "User",
                "created_at": "2025-04-13",
                "last_updated": "2025-04-13"
            }
        )

    @staticmethod
    def update_configuration(new_config, file_path='abiofile.yaml'):
        """
        Actualiza la configuración en memoria y opcionalmente la guarda en archivo.
        """
        ConfigManager._config_instance = new_config
        with open(file_path, 'w') as file:
            yaml.dump(new_config.to_dict(), file)

    @staticmethod
    def get_config():
        """
        Devuelve la instancia singleton de la configuración.
        """
        if ConfigManager._config_instance is None:
            ConfigManager._config_instance = ConfigManager.load_configuration('abiofile.yaml')
        return ConfigManager._config_instance
```
---

### Construcción y Uso del `ABIO_CONFIG_OBJECT`

La clase `AbioConfig` previa debe reestructurarse para representar completamente **todos los valores configurables** definidos en un `abiofile`.

#### Limitación Actual

Actualmente el modelo solo incluye:
- `agent`
- `chat`
- `meta`

Sin embargo, el `abiofile` contiene datos adicionales no representados completamente:
- **Pretraining prompts**: Con roles como `"system"` y `"user"`.
- **Parámetros del modelo**: Como `default_model`, `temperature`, `top_p`, y `message_limit`.
- **Estructuras basadas en roles**: Los prompts usan atributos `role` que podrían requerir representación más robusta.

#### Mejoras Requeridas

- Definir modelos anidados para validación estructural
- Modelar pretraining prompts con clases como `PretrainingPrompt`
- Especificar valores predeterminados claramente
- Opcionalmente usar biblioteca de validación como **Pydantic**

### Clase `AbioConfig` Mejorada

```python
"""
Módulo: config

Define modelos de configuración para el agente IA Abio.

Este módulo provee modelos Pydantic para estructurar, validar y gestionar
configuraciones cargadas desde un Abiofile (YAML/JSON). Incluye metadatos del agente,
ajustes de chat y prompts de preentrenamiento.

Ejemplo:
    >>> from src.models.config import AbioConfig
    >>> config = AbioConfig.parse_file("abiofile.yaml")
    >>> print(config.agent.name)

Dependencias:
    - pydantic
    - typing
    - datetime
"""

from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from datetime import datetime


class AgentConfig(BaseModel):
    """
    Configuración del agente IA.

    Atributos:
        name (str): Nombre del agente.
        version (str): Versión (ej: 1.0.0).
        description (str): Descripción breve.
        environment (Literal): Entorno de ejecución.
    """
    name: str
    version: str
    description: str
    environment: Literal["development", "production", "test"]

    class Config:
        from_attributes = True


class PretrainingPrompt(BaseModel):
    """
    Prompt de preentrenamiento con rol asignado.

    Atributos:
        role (Literal): Rol del mensaje (ej: system, user).
        content (str): Contenido del mensaje.
    """
    role: Literal["system", "user"]
    content: str

    class Config:
        from_attributes = True


class ChatConfig(BaseModel):
    """
    Configuración de chat y parámetros del modelo.

    Atributos:
        message_limit (int): Límite de mensajes en contexto.
        default_model (str): Modelo IA predeterminado.
        temperature (float): Temperatura de muestreo.
        top_p (float): Valor de muestreo por núcleo.
        pretraining_prompts (List[PretrainingPrompt]): Prompts iniciales.
    """
    message_limit: int = Field(..., ge=1)
    default_model: str
    temperature: float = Field(..., ge=0.0, le=1.0)
    top_p: float = Field(..., ge=0.0, le=1.0)
    pretraining_prompts: List[PretrainingPrompt] = []

    class Config:
        from_attributes = True


class MetaConfig(BaseModel):
    """
    Metadatos de creación y versión.

    Atributos:
        created_by (str): Autor de la configuración.
        created_at (str): Fecha ISO de creación.
        last_updated (str): Fecha ISO de última modificación.
    """
    created_by: str
    created_at: str
    last_updated: str

    class Config:
        from_attributes = True


class AbioConfig(BaseModel):
    """
    Modelo raíz de configuración para Abio.

    Atributos:
        agent (AgentConfig): Información general del agente.
        chat (ChatConfig): Parámetros de chat.
        meta (MetaConfig): Metadatos del archivo.
    """
    agent: AgentConfig
    chat: ChatConfig
    meta: MetaConfig

    class Config:
        from_attributes = True
```

Aquí tienes la continuación de la traducción al español:

---

## Modelos de Configuración y Arquitectura del Cargador

El sistema de configuración está diseñado para garantizar validación robusta, modularidad y escalabilidad. Utiliza **modelos Pydantic** para representar y validar cada sección del archivo `abiofile`.

### 🧩 Estructura de Modelos

Todas las clases relacionadas con configuración se definen en `src/config/config.py`. Incluyen modelos anidados para cada sección principal:

- **`AgentConfig`**: Describe identidad y contexto operativo del agente (ej: `name`, `version`, `environment`).
- **`ChatConfig`**: Parámetros del modelo como `temperature`, `top_p`, `message_limit`.
- **`PretrainingPrompt`**: Prompts iniciales con roles (`system`, `user`).
- **`MetaConfig`**: Metadatos de creación y actualización.
- **`AbioConfig`**: Modelo principal que agrupa todas las secciones.

Ejemplo de estructura:
```python
class PretrainingPrompt(BaseModel):
    role: Literal["system", "user"]
    content: str

class ChatConfig(BaseModel):
    message_limit: int
    default_model: str
    temperature: float
    top_p: float
    pretraining_prompts: List[PretrainingPrompt]

class AbioConfig(BaseModel):
    agent: AgentConfig
    chat: ChatConfig
    meta: MetaConfig
```

### ⚙️ Módulo Cargador de Configuración

La lógica de carga se implementa en `src/config/config.py` o un módulo dedicado:

```python
def load_abio_config(path: str) -> AbioConfig:
    """Carga y valida la configuración desde un archivo YAML"""
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return AbioConfig(**data)
```

> ✅ **Mejor Práctica**: Mantén los modelos en el paquete `config` y la lógica de carga en funciones utilitarias.

---

## Desarrollo del Gestor de Configuración [#4]

### Objetivo

**Diseñar e implementar un módulo ConfigManager completo** para manejar carga, acceso y mantenimiento de ajustes en todo el agente Abio.

### Arquitectura Propuesta

#### Decisiones Clave

1. **Separación Modelos/Lógica**:
   - Modelos Pydantic en `config.py`
   - Clase `ConfigManager` en `config_manager.py`

2. **Inyección de Dependencias**:
   - Eliminar estado global usando inyección
   - Mejorar testabilidad y flexibilidad

---

### Diseño de la Clase `ConfigManager`

Implementada en `src/config/config_manager.py`:

```python
class ConfigManager:
    """
    Gestiona el ciclo de vida de la configuración del agente Abio.
    
    Maneja carga desde archivos/valores predeterminados,
    acceso a valores, y persistencia de cambios.
    """
    
    def __init__(self, config_path: Optional[str] = None, config: Optional[AbioConfig] = None):
        self._config = None
        self._config_path = config_path
        
        if config:
            self._config = config
        elif config_path:
            self._config = self._load_from_file(config_path)
        else:
            self._config = self._create_default_config()
    
    def get_config(self) -> AbioConfig:
        """Devuelve el objeto de configuración actual."""
        return self._config
    
    def update_config(self, new_config: AbioConfig) -> None:
        """Actualiza la configuración actual."""
        self._config = new_config
        
    def save_config(self, path: Optional[str] = None) -> None:
        """Guarda la configuración en archivo."""
        save_path = path or self._config_path
        if not save_path:
            raise ValueError("Ruta no especificada para guardar")
        
        # Implementación de serialización
```

---

### Integración con la Capa de Servicio

El `ConfigManager` se inyecta en `AbioService` para proveer configuración:

```python
class AbioService:
    """Clase central del agente que coordina componentes."""
    
    def __init__(self, config_manager: ConfigManager):
        self._config_manager = config_manager
        self._chat_session = None
        self._model_client = None
        
        self._initialize_components()
        
    def _initialize_components(self):
        """Inicializa componentes con configuración."""
        config = self._config_manager.get_config()
        
        self._model_client = self._create_model_client(config.chat.default_model)
        self._chat_session = ChatSession(
            message_limit=config.chat.message_limit,
            pretraining_prompts=config.chat.pretraining_prompts
        )
```

---

### Manejo de Cambios en Configuración

1. **Notificación de Cambios**:
   - Sistema de eventos para cambios
   - Registro de listeners

2. **Reconfiguración Dinámica**:
   - Actualizaciones controladas en tiempo real
   - Validación previa a cambios

```python
class ConfigManager:
    # ... métodos existentes ...
    
    def register_change_listener(self, listener: Callable[[str, Any, Any], None]) -> None:
        """Registra un listener para cambios."""
        self._listeners.append(listener)
        
    def update_value(self, path: str, value: Any) -> None:
        """Actualiza un valor y notifica."""
        old_value = self._get_value_by_path(path)
        self._set_value_by_path(path, value)
        for listener in self._listeners:
            listener(path, old_value, value)
```

---

### Configuración por Entorno

Soporte para entornos específicos:

```python
def load_environment_config(base_path: str, environment: str) -> AbioConfig:
    """
    Carga configuración base + ajustes por entorno.
    
    Ejemplo:
        base_path: abiofile.yaml
        environment: development -> carga abiofile.development.yaml
    """
    base_config = load_config(base_path)
    env_path = f"{base_path.rsplit('.', 1)[0]}.{environment}.yaml"
    if os.path.exists(env_path):
        env_config = load_config(env_path)
        return merge_configs(base_config, env_config)
    return base_config
```

---

### Consideraciones Futuras

1. **Versionado de Esquemas**:
   - Migración entre versiones de configuración
   - Compatibilidad hacia atrás

2. **Gestión de Datos Sensibles**:
   - Almacenamiento seguro de claves API
   - Integración con variables de entorno

3. **Reglas de Validación Avanzadas**:
   - Validación entre campos
   - Restricciones complejas

4. **Interfaz de Edición**:
   - UI web para editar configuración
   - Formularios generados desde esquemas

---

### Próximos Pasos

1. Implementar núcleo de `ConfigManager`
2. Añadir soporte para entornos
3. Integrar con capa de servicio
4. Desarrollar pruebas automatizadas
5. Documentar el sistema

Esta arquitectura provee una base sólida para la gestión de configuración en el agente Abio, asegurando validación adecuada y separación de responsabilidades.