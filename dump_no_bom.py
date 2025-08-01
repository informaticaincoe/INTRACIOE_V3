import os
import django

# Configura el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intracoe.settings')
django.setup()

from django.core.management import call_command

# Ruta donde guardarás el JSON completo
output_path = os.path.join('FE', 'fixtures', 'full_dump.json')

# Abrir el archivo sin BOM
with open(output_path, 'w', encoding='utf-8') as f:
    # dumpdata de toda la base
    call_command('dumpdata', indent=2, stdout=f)

print(f"Archivo generado correctamente en {output_path}")
