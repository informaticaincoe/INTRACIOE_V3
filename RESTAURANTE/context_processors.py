# RESTAURANTE/context_processors.py
from django.urls import reverse, NoReverseMatch

def safe_reverse(name, args=None, kwargs=None, fallback="#"):
    try:
        return reverse(name, args=args or [], kwargs=kwargs or {})
    except NoReverseMatch:
        return fallback

MENU = [
    # --- Restaurante ---
    {
        "section": "Restaurante",
        "items": [
            {
                "label": "Mis mesas",
                "icon": "bi bi-grid-3x3-gap",
                "url_name": "mesas-lista",
                "perm": "RESTAURANTE.rest_view_mesas",
            },
            {
                "label": "Meseros",
                "icon": "bi bi-people",
                "url_name": "meseros-lista",
                "perm": "RESTAURANTE.rest_manage_asignaciones",  # admin
            },
            {
                "label": "Config. Restaurante",
                "icon": "bi bi-gear",
                "url_name": "config_restaurante",
                "perm": "RESTAURANTE.rest_manage_asignaciones",
            },
        ],
    },
]

def nav_menu(request):
    user = request.user
    built_sections = []

    for sec in MENU:
        visible_items = []
        for it in sec["items"]:
            perm = it.get("perm")
            if not perm:
                allowed = user.is_authenticated
            else:
                allowed = user.is_authenticated and user.has_perm(perm)

            if allowed:
                visible_items.append({
                    "label": it["label"],
                    "icon": it.get("icon", ""),
                    "href": safe_reverse(it["url_name"]),
                })

        if visible_items:
            built_sections.append({"section": sec["section"], "items": visible_items})

    return {"nav_menu": built_sections}
