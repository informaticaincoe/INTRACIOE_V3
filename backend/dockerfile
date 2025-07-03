# Python base
FROM python:3.11-slim-bullseye

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y \
        curl \
        gnupg \
        gcc \
        pkg-config \
        libmariadb-dev \
        python3-dev \
        libpq-dev \
        build-essential \
        # dependencias de npm
        ca-certificates \
        # otras dependencias
        libpango-1.0-0 \
        libpangoft2-1.0-0 \
        libpangocairo-1.0-0 \
        libodbc1 \
        libcairo2 \
        libcairo2-dev \
        libgdk-pixbuf2.0-0 \
        libgdk-pixbuf2.0-dev \
        unixodbc \
        unixodbc-dev \
        # instalar Node.js LTS
        && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
        && apt-get install -y nodejs \
        && apt-get clean && \
        rm -rf /var/lib/apt/lists/*

# Set working dir
WORKDIR /app

# Instalar dependencias python
COPY requirements.txt .
RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

# Instalar dependencias del frontend
WORKDIR /app/intracoe-frontend
RUN npm install
RUN npm install vite --save-dev


# Exponer puertos
EXPOSE 8000 5173

# Comando para ejecutar ambos procesos en paralelo
WORKDIR /app
CMD bash -c "python3 manage.py runserver 0.0.0.0:8000 & cd intracoe-frontend && npm run dev"


