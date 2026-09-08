# 1. Imagen base oficial de Python
FROM python:3.10-slim

# 2. Instalar dependencias del sistema requeridas para aplicaciones gráficas (Tkinter/X11/Virtual Display)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk \
    xvfb \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiar e instalar librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

# 5. Copiar el código del proyecto al contenedor
COPY . .

# 6. Ejecutar la app con Xvfb (Servidor de pantalla virtual para entornos headless/CI)
CMD ["xvfb-run", "python", "main.py"]