
<h1 align="center">🤖 ABIO — AI Tool Orchestration Platform</h1>

<p align="center">
  An advanced orchestration platform that unifies and coordinates AI services, integrating <strong>Gemini</strong> and <strong>Claude</strong> APIs with semantic search capabilities, tool coordination, and robust context management.
</p>



## 📁 Project Structure

```bash
.
├── data/                  # Input/output data
├── docs/                  # Project documentation
├── logs/                  # Generated log files
├── src/                   # Main source code
│   ├── chat/              # Chat session management
│   ├── clients/           # API clients for Gemini & Claude
│   ├── config/            # Project configuration
│   ├── context/           # Conversation context handling
│   ├── embeddings/        # Vector embeddings generation
│   ├── errors/            # Custom error types
│   ├── faiss/             # Vector search implementation
│   ├── models/            # Data models (Pydantic)
│   ├── services/          # Auxiliary services
│   ├── tools/             # External tool interfaces
│   └── utils/             # Utility functions
├── tests/                 # Unit tests
├── main.py                # Main entry point
├── Abiofile               # Configuration specification
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker container config
├── docker-compose.yml     # Docker orchestration
└── .env                   # API keys and environment vars
```

---

## ⚙️ Prerequisites

- Python **3.10+**
- Optional: **Docker** (for containerized deployment)
- API Keys for:
  - 🔑 **Gemini**
  - 🔐 **Claude (Anthropic)**
  - 🔍 **Embedding models** (if using custom embeddings)

> Store your keys securely in a `.env` file or configure via Abiofile.

---

## 🌟 Key Features

- 🔀 **Tool Orchestration**  
  ABIO's core purpose is to coordinate and standardize access to external AI tools and services.

- 🧰 **Unified Tool Interface**  
  Standardized interfaces for all integrated tools with the `tools` module acting as a central orchestrator.

- 🔄 **Chat Session Management**  
  Manage conversations with `ChatSession` in [`chat_session.py`](src/chat/chat_session.py).

- 🌐 **Multiple LLM Integration**  
  Switch seamlessly between different AI models like Gemini and Claude based on specific needs.

- 🧠 **Context Management**  
  Maintain conversation state across different tool invocations with `ContextManager`.

- 📊 **Vector Embeddings System**  
  Convert text to vector representations using [`EmbeddingsGenerator`](src/embeddings/embeddings_generator.py).

- 🔍 **Semantic Search with FAISS**  
  Efficient vector-based search capabilities through [`FAISSManager`](src/faiss/faiss_manager.py).

- ⚙️ **Flexible Configuration**  
  Configure the system using the `Abiofile` specification managed by `ConfigManager`.

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your_user/abio.git
cd abio
```

### 2. Set Up Your Environment

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add Your API Keys

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key
ANTHROPIC_API_KEY=your_claude_api_key
```


---

## 💬 Usage

Start the ABIO platform with:

```bash
python main.py
```

Configure tools and services in your Abiofile to customize orchestration behavior.

---

## 🧪 Running Tests

Run all unit tests with:

```bash
python -m unittest discover -s tests
```

---

## 🐳 Docker Deployment

### Build the Image

```bash
docker-compose build
```

### Run the Services

```bash
docker-compose up
```

---

## 🔌 Extending ABIO

ABIO is designed to be extended with new tools and capabilities:

1. Implement the standard tool interface in the `tools` module
2. Register your tool with the orchestrator
3. Configure usage parameters in your Abiofile

See documentation for detailed extension guidelines.

---

## 🤝 Contributions

Contributions are welcome!  
Feel free to fork the repo and submit pull requests.

> Please open an issue first to discuss major changes or new features.

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.
