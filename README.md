# ABIO - Chatbot with Generative Models

ABIO is a project designed to manage chat sessions with advanced generative models like Gemini and Claude. This system includes functionalities to handle conversation context, log recording, and integrations with generative model APIs.

## Project Structure

```
.
├── data/                  # Input/output data
├── docs/                  # Project documentation
├── logs/                  # Generated log files
├── src/                   # Main source code
│   ├── chat/              # Chat session management
│   ├── clients/           # Clients to interact with external APIs
│   ├── config/            # Project configuration
│   ├── context/           # Conversational context management
│   ├── errors/            # Custom error handling
│   ├── models/            # Data models (Pydantic)
│   ├── services/          # Additional services
│   └── utils/             # General utilities
├── tests/                 # Unit tests
├── main.py                # Main entry point
├── requirements.txt       # Project dependencies
├── Dockerfile             # Docker container configuration
├── docker-compose.yml     # Docker services orchestration
└── .env                   # Environment variables
```

## Prerequisites

- **Python 3.10 or higher**
- **Docker** (optional, for running in containers)
- **API Keys** for Gemini and Claude services, configured in the `.env` file.

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your_user/abio.git
   cd abio
   ```

2. Create a virtual environment and install the dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure the environment variables in a `.env` file:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   ANTHROPIC_API_KEY=your_claude_api_key
   ```

### Usage

Run the main file to start a chat session:
```bash
python main.py
```

### Testing

Run the unit tests with:
```bash
python -m unittest discover -s tests
```

### Using Docker

1. Build the Docker image:
   ```bash
   docker-compose build
   ```

2. Run the services:
   ```bash
   docker-compose up
   ```

## Main Features

- **Chat Session Management**: Handling messages and conversational context with [`ChatSession`](src/chat/chat_session.py).
- **API Integration**: Clients to interact with Gemini ([`GeminiClient`](src/clients/gemini_client.py)) and Claude ([`ClaudeClient`](src/clients/claude_client.py)).
- **Context Management**: Control of message history with [`ContextManager`](src/context/context_manager.py).
- **Log Recording**: Advanced log configuration with [`setup_logging`](src/utils/setup_logging.py).

## Contributions

Contributions are welcome. Please open an issue or submit a pull request to discuss any changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.