# 🤖 ABIO — Chatbot con Modelos Generativos

<p align="center">
  Una plataforma de IA conversacional que integra APIs de <strong>Gemini</strong> y <strong>Claude</strong>, con seguimiento de contexto, registro de actividad (logging) y un diseño modular robusto.
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
│   ├── context/           # Manejo del contexto de conversación
│   ├── errors/            # Tipos de error personalizados
│   ├── models/            # Modelos de datos (Pydantic)
│   ├── services/          # Servicios auxiliares
│   └── utils/             # Funciones de utilidad (ej., registro de actividad)
├── tests/                 # Pruebas unitarias
├── main.py                # Punto de entrada principal
├── requirements.txt       # Dependencias de Python
├── Dockerfile             # Configuración del contenedor Docker
├── docker-compose.yml     # Orquestación de Docker
└── .env                   # Claves API y variables de entorno
```

---

## ⚙️ Requisitos Previos

- Python **3.10+**
- Opcional: **Docker** (para despliegue en contenedor)
- Claves API para:
  - 🔑 **Gemini**
  - 🔐 **Claude (Anthropic)**

> Guarda tus claves de forma segura en un archivo `.env`.

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

### 3. Añade tus Claves API

Crea un archivo `.env` en el directorio raíz:

```env
GEMINI_API_KEY=your_gemini_api_key
ANTHROPIC_API_KEY=your_claude_api_key
```

---

## 💬 Uso

Inicia una sesión de chat con:

```bash
python main.py
```

---

## 🧪 Ejecutando Pruebas

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

## 🌟 Características Clave

- 🔄 **Gestión de Sesiones de Chat**
  Gestiona conversaciones con `ChatSession` en [`chat_session.py`](src/chat/chat_session.py).

- 🌐 **Integración de APIs Generativas**
  Utiliza `GeminiClient` y `ClaudeClient` para una interacción avanzada con modelos de IA.

- 🧠 **Memoria de Contexto**
  Mantiene el historial de mensajes con `ContextManager`.

- 📝 **Sistema de Registro de Actividad (Logging)**
  Registra logs detallados a través de `setup_logging.py`.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas!
Siéntete libre de bifurcar (fork) el repositorio y enviar pull requests.

> Por favor, abre un issue primero para discutir cambios importantes o nuevas funcionalidades.

---

## 📄 Licencia

Este proyecto está licenciado bajo la **Licencia MIT**.
Consulta el archivo [LICENSE](LICENSE) para más detalles.
```