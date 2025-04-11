<h1 align="center">🤖 ABIO — Chatbot with Generative Models</h1>

<p align="center">
  A conversational AI platform integrating <strong>Gemini</strong> and <strong>Claude</strong> APIs, with context tracking, logging, and robust modular design.
</p>

---

## 📁 Project Structure

```
.
├── data/                  # Input/output data
├── docs/                  # Project documentation
├── logs/                  # Generated log files
├── src/                   # Main source code
│   ├── chat/              # Chat session management
│   ├── clients/           # API clients for Gemini & Claude
│   ├── config/            # Project configuration
│   ├── context/           # Conversation context handling
│   ├── errors/            # Custom error types
│   ├── models/            # Data models (Pydantic)
│   ├── services/          # Auxiliary services
│   └── utils/             # Utility functions (e.g., logging)
├── tests/                 # Unit tests
├── main.py                # Main entry point
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

> Store your keys securely in a `.env` file.

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

Start a chat session with:

```bash
python main.py
```

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

## 🌟 Key Features

- 🔄 **Chat Session Management**  
  Manage conversations with `ChatSession` in [`chat_session.py`](src/chat/chat_session.py).

- 🌐 **Generative API Integration**  
  Use `GeminiClient` and `ClaudeClient` for advanced AI model interaction.

- 🧠 **Context Memory**  
  Maintain message history with `ContextManager`.

- 📝 **Logging System**  
  Record detailed logs via `setup_logging.py`.

---

## 🤝 Contributions

Contributions are welcome!  
Feel free to fork the repo and submit pull requests.

> Please open an issue first to discuss major changes or new features.

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.
