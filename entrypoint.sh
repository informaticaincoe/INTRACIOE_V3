#!/bin/bash
set -e

APP_PORT="${APP_PORT:-8000}"

# Archivos estáticos (admin, CSS, JS)
echo ">>> Recopilando archivos estáticos..."
python3 manage.py collectstatic --noinput 2>/dev/null || true

# SIEMPRE aplicar migraciones (SQLite bootstrap o PostgreSQL)
echo ">>> Aplicando migraciones..."
python3 manage.py makemigrations --noinput 2>/dev/null || true
python3 manage.py migrate --noinput 2>/dev/null || true
echo ">>> Migraciones aplicadas."

# Si hay config de BD, cargar catálogos
if [ -f /app/config/db_config.json ] || [ -f /app/db_config.json ]; then
    echo ">>> Cargando catálogos de Hacienda..."
    python3 manage.py cargar_catalogos 2>/dev/null || true
fi

echo ">>> Iniciando INTRACOE en puerto $APP_PORT"
exec daphne -b 0.0.0.0 -p "$APP_PORT" intracoe.asgi:application
