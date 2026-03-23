# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**INTRACIOE V3** — Enterprise administration and electronic invoicing system (Sistema de Administración Empresarial y Facturación Electrónica) for El Salvador. Full Django application — views rendered via Django templates, with DRF for REST API endpoints.

## Commands

### Backend (Django)
```bash
python manage.py runserver          # Start dev server (port 8000)
python manage.py migrate            # Apply migrations
python manage.py makemigrations     # Create new migrations
python manage.py test               # Run all tests
python manage.py test FE            # Run tests for a specific app
python manage.py test AUTENTICACION # Run tests for a specific app
python manage.py createsuperuser    # Create admin user
flake8 .                            # Lint (config in .flake8)
```

### Docker
```bash
docker-compose up    # Start backend on port 8787
```

## Architecture

### Backend — Django Modular Monolith

Each domain is a separate Django app. Apps are registered in `intracoe/settings.py` and routed in `intracoe/urls.py`.

| App | URL prefix | Purpose |
|-----|-----------|---------|
| `FE/` | `/fe/` | Electronic invoicing (Facturación Electrónica) — largest module |
| `RRHH/` | `/rrhh/` | Human resources & payroll |
| `CONTABILIDAD/` | `/contabilidad/` | Accounting & tax annexes |
| `INVENTARIO/` | `/inventario/` | Products, warehouses, stock movements |
| `RESTAURANTE/` | `/restaurante/` | Restaurant/POS with WebSocket consumers |
| `AUTENTICACION/` | `/autentications/` | Custom user model, token auth, password reset |
| `INFORMATICA/` | `/informatica/` | System setup wizard |

**Each app follows this internal pattern:**
```
models.py        # Data models
views.py         # HTML template views (class & function-based)
api_views.py     # DRF REST endpoints
serializers.py   # DRF serializers
urls.py          # URL routing
forms.py         # Django forms
migrations/      # Database migrations
templates/       # App-specific HTML templates
```

**Authentication:** Token-based (`Authorization: Token <token>`). Custom `MultiRoleBackend` in `AUTENTICACION/`. Roles: `admin`, `vendedor`, `supervisor`, `cliente`, `mesero`, `cocinero`, `cajero`.

**Real-time:** Django Channels (ASGI) used in `RESTAURANTE/` for WebSocket connections.

**External integrations:**
- PostgreSQL at `192.168.2.49:5432` (primary DB — `intracoe_prod`)
- SQL Server at `200.31.164.67:2034` (read-only legacy system — `olComun`)
- El Salvador government tax authority (Hacienda) API for DTE validation and submission

### Frontend — Django Templates

The UI is rendered server-side via Django templates. Each app has a `templates/` subdirectory with its own HTML files. A central `templates/` directory at the project root holds shared base templates and layouts.

Templates use Django's template inheritance — extend a base template and fill named blocks. Static assets (CSS, JS, images) are served from `static/`.

## Key Domain Concepts

- **DTE** (Documento Tributario Electrónico): Electronic tax documents submitted to El Salvador's Hacienda
- **Emisor**: The company issuing invoices — configured once in `FE/Emisor_fe`
- **Receptor**: Invoice recipient/customer — `FE/Receptor_fe`
- **NumeroControl**: Sequential invoice number control system
- **Contingencia**: Offline invoice mode when Hacienda is unavailable — tracked in `FE/EventoContingencia`
- **CCF** vs **Factura**: Two main invoice types (CCF for VAT-registered businesses, Factura for end consumers)
