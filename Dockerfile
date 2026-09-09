# 1. Imagen base oficial de Python
FROM python:3.10-slim

# 2. Instalar dependencias esenciales del sistema para OpenGL/Pandas
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 3. Directorio de trabajo
WORKDIR /app

# 4. Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar todo el código y dataset al contenedor
COPY . .

# 6. Ejecutar directamente con Python (sin xvfb-run)
CMD ["python", "GraphicsTestCI.py"]