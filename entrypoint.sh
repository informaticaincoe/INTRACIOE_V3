#!/bin/bash
set -e

APP_PORT="${APP_PORT:-8000}"

# Si existe db_config.json, aplicar migraciones y cargar catálogos
if [ -f /app/db_config.json ]; then
    echo ">>> Base de datos configurada — aplicando migraciones..."
    python3 manage.py makemigrations --noinput 2>/dev/null || true
    python3 manage.py migrate --noinput 2>/dev/null || true
    echo ">>> Migraciones aplicadas."

    echo ">>> Cargando catálogos de Hacienda..."
    python3 manage.py cargar_catalogos 2>/dev/null || true
fi

echo ">>> Iniciando INTRACOE en puerto $APP_PORT"
exec daphne -b 0.0.0.0 -p "$APP_PORT" intracoe.asgi:application
