abio/
├── api/             (Mantiene la lógica de acceso a la API Gemini)
├── chat/            (Mantiene la lógica central del chat)
├── services/       (NUEVO - Capa de Servicios)
│   ├── __init__.py
│   ├── chat_service.py  (Implementa la lógica de la API del chat)
├── config/
├── ui/              (La UI se convierte en un cliente del servicio)
│   ├── __init__.py
│   └── console_ui.py (Ahora consume la capa de servicios)
├── utils/
├── main.py
└── requirements.txt