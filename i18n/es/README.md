<h1 align="center">🤖 ABIO — Plataforma de Orquestación de Herramientas de IA</h1>

<p align="center">
  Una plataforma avanzada de orquestación que unifica y coordina servicios de inteligencia artificial, integrando las APIs de <strong>Gemini</strong> y <strong>Claude</strong> con capacidades de búsqueda semántica, coordinación de herramientas y gestión robusta de contexto.
</p>

---

## 📁 Estructura del Proyecto

```bash
.
├── data/                  # Datos de entrada/salida
├── docs/                  # Documentación del proyecto
├── logs/                  # Archivos de registro generados
├── src/                   # Código fuente principal
│   ├── chat/              # Gestión de sesiones de chat
│   ├── clients/           # Clientes API para Gemini y Claude
│   ├── config/            # Configuración del proyecto
│   ├── context/           # Manejo del contexto conversacional
│   ├── embeddings/        # Generación de vectores de embeddings
│   ├── errors/            # Tipos de errores personalizados
│   ├── faiss/             # Implementación de búsqueda vectorial
│   ├── models/            # Modelos de datos (Pydantic)
│   ├── services/          # Servicios auxiliares
│   ├── tools/             # Interfaces con herramientas externas
│   └── utils/             # Funciones utilitarias
├── tests/                 # Pruebas unitarias
├── main.py                # Punto de entrada principal
├── Abiofile               # Especificación de configuración
├── requirements.txt       # Dependencias de Python
├── Dockerfile             # Configuración del contenedor Docker
├── docker-compose.yml     # Orquestación con Docker
└── .env                   # Llaves API y variables de entorno
```

---

## ⚙️ Requisitos Previos

- Python **3.10 o superior**
- Opcional: **Docker** (para despliegue en contenedor)
- Llaves API para:
  - 🔑 **Gemini**
  - 🔐 **Claude (Anthropic)**
  - 🔍 **Modelos de embeddings** (si usas embeddings personalizados)

> Guarda tus llaves de forma segura en un archivo `.env` o configúralas en el archivo Abiofile.

---

## 🌟 Funcionalidades Principales

- 🔀 **Orquestación de Herramientas**  
  El propósito principal de ABIO es coordinar y estandarizar el acceso a herramientas y servicios externos de IA.

- 🧰 **Interfaz Unificada de Herramientas**  
  Interfaces estandarizadas para todas las herramientas integradas mediante el módulo `tools` como orquestador central.

- 🔄 **Gestión de Sesiones de Chat**  
  Administra conversaciones con `ChatSession` en [`chat_session.py`](src/chat/chat_session.py).

- 🌐 **Integración con Múltiples LLMs**  
  Cambia sin problemas entre diferentes modelos como Gemini y Claude según las necesidades específicas.

- 🧠 **Gestión de Contexto**  
  Mantiene el estado de la conversación entre diferentes invocaciones de herramientas con `ContextManager`.

- 📊 **Sistema de Embeddings Vectoriales**  
  Convierte texto a representaciones vectoriales mediante [`EmbeddingsGenerator`](src/embeddings/embeddings_generator.py).

- 🔍 **Búsqueda Semántica con FAISS**  
  Capacidades de búsqueda eficiente basada en vectores con [`FAISSManager`](src/faiss/faiss_manager.py).

- ⚙️ **Configuración Flexible**  
  Configura el sistema usando el archivo `Abiofile`, gestionado por `ConfigManager`.

---

## 🚀 Instalación

### 1. Clona el Repositorio

```bash
git clone https://github.com/your_user/abio.git
cd abio
```

### 2. Configura tu Entorno

```bash
python -m venv venv
source venv/bin/activate     # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Agrega tus Llaves API

Crea un archivo `.env` en el directorio raíz:

```env
GEMINI_API_KEY=tu_clave_gemini
ANTHROPIC_API_KEY=tu_clave_claude
```

---

## 💬 Uso

Inicia la plataforma ABIO con:

```bash
python main.py
```

Configura las herramientas y servicios en tu archivo `Abiofile` para personalizar el comportamiento de orquestación.

---

## 🧪 Ejecución de Pruebas

Ejecuta todas las pruebas unitarias con:

```bash
python -m unittest discover -s tests
```

---

## 🐳 Despliegue con Docker

### Construye la Imagen

```bash
docker-compose build
```

### Ejecuta los Servicios

```bash
docker-compose up
```

---

## 🔌 Extender ABIO

ABIO está diseñado para ser extensible con nuevas herramientas y capacidades:

1. Implementa la interfaz estándar de herramientas en el módulo `tools`
2. Registra tu herramienta en el orquestador
3. Configura sus parámetros en el archivo `Abiofile`

Consulta la documentación para ver las guías de extensión detalladas.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas!  
No dudes en hacer un fork del repositorio y enviar pull requests.

> Por favor, abre primero un issue para discutir cambios importantes o nuevas funcionalidades.

---

## 📄 Licencia

Este proyecto está licenciado bajo la **Licencia MIT**.  
Consulta el archivo [LICENSE](LICENSE) para más detalles.

