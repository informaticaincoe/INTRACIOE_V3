# Cambiar a Python 3.10-slim-bullseye (o Python 3.11)
FROM python:3.11
# O usa FROM python:3.11-slim-bullseye para Python 3.11

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los requisitos del archivo requirements.txt
COPY requirements.txt .

# Instalar las dependencias necesarias para mysqlclient, pkg-config y SQL Server
RUN apt-get update && \
    apt-get install -y curl apt-transport-https \
    gnupg \
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
    gcc \
    pkg-config \
    libmariadb-dev \
    python3-dev \
    libpq-dev \
    --no-install-recommends && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Instalar los requisitos de Python
RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente de la aplicación en el contenedor
COPY . .

# Ejecutar el comando collectstatic durante la construcción
#RUN python3 manage.py collectstatic --noinput

# Exponer el puerto en el que la aplicación estará corriendo
EXPOSE 8000

# Comando para correr la aplicación
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
