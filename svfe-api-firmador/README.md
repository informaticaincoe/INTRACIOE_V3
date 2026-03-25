# Firmador DTE - El Salvador

Coloque aquí el archivo JAR del firmador de documentos tributarios electrónicos.

## Archivo requerido

```
svfe-api-firmador/
  └── firmador.jar    ← Copiar aquí el .jar del firmador
```

Si el archivo tiene otro nombre (ej: `svfe-api-firmador-1.0.0.jar`), renómbrelo a `firmador.jar` o ajuste el `command` en `docker-compose.yml`.

## Puerto

El firmador escucha en el puerto **8113** por defecto dentro del contenedor.
Desde la app Django se accede como `http://firmador:8113` (nombre del servicio en Docker).

## Configuración en INTRACOE

En el wizard de configuración (Paso 5 - Servidor), configure:
- **Clave:** `firmador`
- **URL Endpoint:** `http://firmador:8113/firmardocumento/`
