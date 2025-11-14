FROM python:3.13-slim

WORKDIR /app

# Copia el archivo de dependencias e instálalas
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto al contenedor
COPY . .


EXPOSE 8001

CMD ["uvicorn", "api_main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]