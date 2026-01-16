import datetime
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db.models import Exists, OuterRef, Q
from RESTAURANTE.models import Area, AsignacionMesa, Mesa, Mesero, Platillo
from django.utils.dateparse import parse_datetime
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from RESTAURANTE.views.views_pedidos import get_mesero_from_user

"""
MANEJO DE:
    - Mesa
    - AsignacionMesa
    - Estados de mesa
"""
###############################################################################################################
#                                                  Mesas                                                      #
###############################################################################################################
def cambiar_estado_mesa(request, pk, estado):
    mesa = get_object_or_404(Mesa, pk=pk)
    # Quitamos la validación estricta de POST para que funcione con el enlace
    mesa.estado = estado
    mesa.save()
    messages.success(request, f'Mesa {mesa.numero} ahora está OCUPADA.')
    return redirect("mesas-lista")

def _parse_dt(value: str | None):
    """
    Convierte strings tipo '2025-12-16T09:43' a datetime aware (con TZ).
    Si viene vacío => None.
    """
    if not value:
        return None

    dt = parse_datetime(value)  # intenta parsear ISO
    if dt is None:
        dt = datetime.fromisoformat(value) # fallback para datetime-local sin segundos

    # Si viene naive (sin tz) lo asumimos en zona horaria local del sistema
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_current_timezone())

    return dt

@login_required
def listar_mesas(request):
    search_query = request.GET.get('search_name') or ""
    ahora = timezone.localtime()

    # --- Si es MESERO: solo sus mesas asignadas ---
    if getattr(request.user, "role", None) == "mesero":
        mesero = get_mesero_from_user(request.user)
        if not mesero:
            messages.error(request, "No tienes un mesero asociado o estás inactivo.")
            return redirect("login_mesero")

        # Asignaciones activas del mesero
        asignacion_activa = (
            AsignacionMesa.objects
            .filter(mesero=mesero)
            .filter(
                Q(fecha_inicio__lte=ahora, fecha_fin__gte=ahora) |
                Q(fecha_inicio__lte=ahora, fecha_fin__isnull=True) |
                Q(es_fija=True)
            )
        )

        # Mesas asignadas
        mesas = Mesa.objects.filter(
            id__in=asignacion_activa.values("mesa_id")
        ).order_by("numero")
        platillos = Platillo.objects.all()

        print("PLATILLOS ", platillos)
        if search_query:
            mesas = mesas.filter(numero__icontains=search_query)

        

        # Opcional: marcar que tiene mesero (para tu UI)
        for m in mesas:
            m.tiene_mesero = True
            acciones_mesero = []

            if m.estado == 'LIBRE':
                acciones_mesero.append({
                    "type": "link",
                    "label": "Ocupar mesa",
                    "icon": "bi bi-journal-plus",
                    # al ocupar: pasa a PENDIENTE_ORDEN
                    "href": reverse("cambiar_estado_mesa", args=[m.id, "PENDIENTE_ORDEN"])
                })

            elif m.estado == 'PENDIENTE_ORDEN':
                acciones_mesero.append({
                    "type": "modal",
                    "label": "Tomar orden",
                    "icon": "bi bi-clipboard-check",
                    "target": "#tomarOrdenModal",
                    "href": reverse("pedido_crear_desde_mesa"),
                    "data": {
                        "mesa-id": m.id,
                        "mesa-numero": m.numero,
                    }
                })
                acciones_mesero.append({
                    "type": "link",
                    "label": "Cancelar",
                    "icon": "bi bi-x-circle text-danger",
                    "href": reverse("cambiar_estado_mesa", args=[m.id, "LIBRE"])
                })

            elif m.estado == 'OCUPADA':
                acciones_mesero.append({
                    "type": "modal",
                    "label": "Ver / agregar pedido",
                    "icon": "bi bi-receipt",
                    "target": "#verOrdenModal",
                    "data": {
                        "mesa-id": m.id,
                        "mesa-numero": m.numero,
                        "modo": "ver",  # opcional
                    }
                })
                acciones_mesero.append({
                    "type": "link",
                    "label": "Entregar",
                    "icon": "bi bi-x-circle text-danger",
                    "href": reverse("cambiar_estado_mesa", args=[m.id, "ENTREGADO"])
                })
                
            elif m.estado == 'ENTREGADO':
                acciones_mesero.append({
                    "type": "modal",
                    "label": "Ver / agregar pedido",
                    "icon": "bi bi-receipt",
                    "target": "#verOrdenModal",
                    "data": {
                        "mesa-id": m.id,
                        "mesa-numero": m.numero,
                        "modo": "ver",  # opcional
                    }
                })
                acciones_mesero.append({
                    "type": "link",
                    "label": "Solicitar cuenta",
                    "icon": "bi bi-cash-coin",
                    "href": reverse("solicitar_cuenta", args=[m.id])
                })

            elif m.estado == 'PENDIENTE_PAGO':
                acciones_mesero.append({
                    "type": "link",
                    "label": "Realizar pago",
                    "icon": "bi bi-cash-coin",
                    "href": reverse("pedido-checkout", args=[m.id])
                })
            elif m.estado == 'PAGADO':
                acciones_mesero.append({
                    "type": "link",
                    "label": "Reabrir mesa",
                    "icon": "bi bi-arrow-counterclockwise",
                    "href": reverse("cambiar_estado_mesa", args=[m.id, "LIBRE"])
                })

            m.acciones = acciones_mesero

        context = {
            "lista_mesas": mesas,
            "modo": "mesero",
            "platillos": platillos,
        }
        return render(request, "mesas/mesas.html", context)

    # --- Si NO es mesero: admin ve todas ---
    mesas = Mesa.objects.all()

    if search_query:
        mesas = mesas.filter(numero__icontains=search_query)

    asignacion_activa = AsignacionMesa.objects.filter(mesa=OuterRef("pk")).filter(
        Q(fecha_inicio__lte=ahora, fecha_fin__gte=ahora) |
        Q(fecha_inicio__lte=ahora, fecha_fin__isnull=True) |
        Q(es_fija=True)
    )

    mesas = mesas.annotate(tiene_mesero=Exists(asignacion_activa)).order_by("numero")

    lista_meseros = Mesero.objects.filter(activo=True)

    # Acciones admin por mesa
    for m in mesas:
        acciones = []
        if not m.tiene_mesero:
            acciones.append({
                "type": "modal",
                "label": "Asignar mesero",
                "icon": "bi bi-exclamation-triangle-fill text-warning",
                "target": "#asignarMeseroModal",
                "data": {"mesa-id": m.id, "mesa-numero": m.numero},
            })
            acciones.append({"type": "divider"})

        acciones += [
            {"type": "link", "label": "Editar", "icon": "bi bi-pencil", "href": reverse("editar-mesa", args=[m.id])},
            {"type": "modal", "label": "Eliminar", "icon": "bi bi-trash", "target": "#eliminarMesaModal",
             "data": {"id": m.id, "nombre": m.numero}},
        ]
        m.acciones = acciones

    context = {
        "lista_mesas": mesas,
        "lista_meseros": lista_meseros,
        "modo": "admin",
    }
    return render(request, "mesas/mesas.html", context)

def crear_mesa(request):
    print(">>>metodo ", request.method)
    if request.method == 'POST':
        numero = request.POST.get('numero') or ''
        capacidad = request.POST.get('capacidad') or ''
        area_id = request.POST.get('area_id') or ''
        es_vip = request.POST.get('es_vip') == "on"
        estado = request.POST.get('estado')
        
        if numero and estado:
                Mesa.objects.create(
                    numero = numero,
                    capacidad = capacidad,
                    area_id=area_id,
                    es_vip = es_vip,
                    estado = estado,
                )
                messages.success(request, f'Mesa creado con éxito.')
        else:
            messages.error(request, 'El numero y estado del platillo no puede estar vacío.')
            
        # Buena Práctica: Redirigir después de POST para evitar reenvío del formulario
        return redirect('mesas-lista')
        
    area = Area.objects.all()
   
    context = {
        "areas_lista": area,
        "ESTADO_MESA_CHOICES": Mesa.ESTADO_MESA_CHOICES,
    }
    return render(request, 'mesas/formulario.html', context)

def editar_mesa(request, pk):
    print(">>>metodo ", request.method)
    mesa = get_object_or_404(Mesa, pk=pk)
    
    if request.method == 'POST':
        numero = request.POST.get('numero') or ''
        capacidad = request.POST.get('capacidad') or ''
        area_id = request.POST.get('area_id') or ''
        es_vip = request.POST.get('es_vip') == "on"
        estado = request.POST.get('estado')
        
        if numero and estado:
            mesa.numero = numero
            mesa.capacidad = capacidad
            mesa.area_id = area_id
            mesa.es_vip = es_vip
            mesa.estado = estado
            mesa.save()
            messages.success(request, f'Mesa creado con éxito.')
        else:
            messages.error(request, 'El numero y estado del platillo no puede estar vacío.')
            
        # Buena Práctica: Redirigir después de POST para evitar reenvío del formulario
        return redirect('mesas-lista')
        
    area = Area.objects.all()
   
    context = {
        "areas_lista": area,
        "ESTADO_MESA_CHOICES": Mesa.ESTADO_MESA_CHOICES,
        "mesa": mesa
    }
    return render(request, 'mesas/formulario.html', context)

def eliminar_mesa(request, pk):
    print("pk ", pk)
    print("method ", request.method)
    
    if request.method == "POST":
        mesa = get_object_or_404(Mesa, pk=pk)
        mesa_nombre = mesa.numero
        mesa.delete()
        messages.success(request, f'mesa "{mesa_nombre}" eliminado correctamente.')
        
    return redirect('mesas-lista')


###############################################################################################################
#                                         Asignaciones de mesa                                                #
###############################################################################################################
def asignar_mesa_a_mesero(request):
    print("-------------- Metodo API ", request.method)

    if request.method == "POST":
        mesa_id = request.POST.get("mesa_id")
        mesero_id = request.POST.get("mesero_id") or ""
        es_fija = request.POST.get("es_fija") == "on"
        activa = request.POST.get("activa") == "on"

        fecha_inicio = _parse_dt(request.POST.get("fecha_inicio"))
        fecha_fin = _parse_dt(request.POST.get("fecha_fin"))

        # Si no mandan fecha_inicio, usa ahora
        if not fecha_inicio:
            fecha_inicio = timezone.now()

        print("mesa", mesa_id)
        print("mesero", mesero_id)
        print("fecha_inicio", fecha_inicio)
        print("fecha_fin", fecha_fin)
        print("es_fija", es_fija)

        # --- Solapamiento: (existing.start < new.end) AND (existing.end > new.start OR existing.end is null)
        q = (Q(es_fija=False) | Q(es_fija__isnull=True))
        q &= (Q(fecha_fin__gt=fecha_inicio) | Q(fecha_fin__isnull=True))

        # IMPORTANTÍSIMO: solo filtrar start < new_end si new_end existe
        if fecha_fin:
            q &= Q(fecha_inicio__lt=fecha_fin)

        solapamientos = AsignacionMesa.objects.filter(mesa_id=mesa_id).filter(q).exists()

        if solapamientos:
            from django.contrib import messages
            messages.error(request, "Error: La mesa ya está asignada para este período de tiempo.")
            return redirect("mesas-lista")

        if mesa_id and mesero_id:
            AsignacionMesa.objects.create(
                mesa_id=mesa_id,
                mesero_id=mesero_id,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,  # None si viene vacío (correcto)
                es_fija=es_fija,
                activa=activa,
            )
            from django.contrib import messages
            messages.success(request, "Asignación creada con éxito.")
        else:
            from django.contrib import messages
            messages.error(request, "El mesero y mesa no pueden estar vacíos.")

    return redirect("mesas-lista")

def editar_asignacion_mesa_a_mesero(request,pk):
    print("-------------- Metodo API EDITAR ASIGNACIOn", request.method)
    
    asignacion = get_object_or_404(AsignacionMesa, pk=pk)
    print(">>>>>>>>>>> asignacion ", asignacion )
    

    if request.method == "POST":
        mesa_id = request.POST.get("mesa_id")
        mesero_id = request.POST.get("mesero_id") or ""
        es_fija = request.POST.get("es_fija") == "on"
        activa = request.POST.get("activa") == "on"
        fecha_inicio = _parse_dt(request.POST.get("fecha_inicio"))
        fecha_fin = _parse_dt(request.POST.get("fecha_fin"))

        # Si no mandan fecha_inicio, usa ahora
        if not fecha_inicio:
            fecha_inicio = timezone.now()

        print("mesa", mesa_id)
        print("mesero", mesero_id)
        print("fecha_inicio", fecha_inicio)
        print("fecha_fin", fecha_fin)
        print("es_fija", es_fija)

        # --- Solapamiento: (existing.start < new.end) AND (existing.end > new.start OR existing.end is null)
        q = (Q(es_fija=False) | Q(es_fija__isnull=True))
        q &= (Q(fecha_fin__gt=fecha_inicio) | Q(fecha_fin__isnull=True))

        # IMPORTANTÍSIMO: solo filtrar start < new_end si new_end existe
        if fecha_fin:
            q &= Q(fecha_inicio__lt=fecha_fin)

        solapamientos = (
            AsignacionMesa.objects
            .filter(mesa_id=mesa_id)
            .filter(q)
            .exclude(pk=asignacion.pk)  # ✅ para que no choque consigo misma
            .exists()
        )
        if solapamientos:
            from django.contrib import messages
            messages.error(request, "Error: La mesa ya está asignada para este período de tiempo.")
            return redirect("mesas-lista")

        if mesa_id and mesero_id:
            
            asignacion.mesa_id = mesa_id
            asignacion.mesero_id = mesero_id
            asignacion.es_fija = es_fija
            asignacion.activa = activa
            asignacion.fecha_inicio = fecha_inicio
            asignacion.fecha_fin = fecha_fin
            
            asignacion.save()
            
            from django.contrib import messages
            messages.success(request, "Asignación creada con éxito.")
        else:
            from django.contrib import messages
            messages.error(request, "El mesero y mesa no pueden estar vacíos.")
        
        return redirect("asignaciones-lista")
        

    lista_meseros = Mesero.objects.all()
    context = {
        "asignacion":asignacion,
        "lista_meseros": lista_meseros
    }
    
    return render(request, "asignacionMesas\asignacion_mesas.html", context)


def eliminar_asignacion_mesa_a_mesero(request, pk):
    print("pk ", pk)
    print("method ", request.method)
    
    if request.method == "POST":
        asignacion = get_object_or_404(AsignacionMesa, pk=pk)
        asignacion.delete()
        messages.success(request, f'Asignacion eliminada correctamente.')
        
    return redirect('asignaciones-lista')

def listar_asignaciones(request):
    search_query = request.GET.get('search_name')
    if search_query:
        # Filtrar categorías por nombre que contenga la búsqueda (case-insensitive)
        asignaciones = AsignacionMesa.objects.filter(numero__icontains=search_query)
    else:
        asignaciones = AsignacionMesa.objects.all().order_by("pk")
        
    print("LISTAR ASIG", asignaciones)
    lista_meseros = Mesero.objects.all()
    lista_mesas = Mesa.objects.all()
    lista_areas = Area.objects.all()

    context = {
        'lista_mesas': lista_mesas,  # Usamos 'categorias_list' como clave para la plantilla
        "lista_meseros": lista_meseros,
        "asignaciones_lista": asignaciones,
        "lista_areas":lista_areas,
    }
    return render(request, 'asignacionMesas/asignacion_mesas.html', context)

