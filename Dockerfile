FROM python:3.10-slim

WORKDIR /app

# Copia el archivo de dependencias e instálalas
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto al contenedor
COPY . .

# Comando por defecto para ejecutar los tests
CMD ["python", "-m", "unittest", "discover", "-s", "tests"]
