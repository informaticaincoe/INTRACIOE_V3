#!/bin/bash
set -e

APP_PORT="${APP_PORT:-8000}"

# Archivos estáticos (admin, CSS, JS)
echo ">>> Recopilando archivos estáticos..."
python3 manage.py collectstatic --noinput 2>/dev/null || true

# Buscar db_config.json en volumen persistente o en raíz
DB_CONFIG=""
if [ -f /app/config/db_config.json ]; then
    DB_CONFIG="/app/config/db_config.json"
elif [ -f /app/db_config.json ]; then
    DB_CONFIG="/app/db_config.json"
fi

if [ -n "$DB_CONFIG" ]; then
    echo ">>> Base de datos configurada ($DB_CONFIG) — aplicando migraciones..."
    python3 manage.py makemigrations --noinput 2>/dev/null || true
    python3 manage.py migrate --noinput 2>/dev/null || true
    echo ">>> Migraciones aplicadas."

    echo ">>> Cargando catálogos de Hacienda..."
    python3 manage.py cargar_catalogos 2>/dev/null || true
fi

echo ">>> Iniciando INTRACOE en puerto $APP_PORT"
exec daphne -b 0.0.0.0 -p "$APP_PORT" intracoe.asgi:application
