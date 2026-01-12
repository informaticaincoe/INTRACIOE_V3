import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Exists, OuterRef, Q
from django.contrib import messages
from django.utils import timezone
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from RESTAURANTE.models import Area, AsignacionMesa, CategoriaMenu, Mesa, Mesero, Platillo

###############################################################################################################
#                                                  CATEGORIA                                                  #
###############################################################################################################
def listar_categorias(request):
    
    search_query = request.GET.get('search_name')
    if search_query:
        # Filtrar categorías por nombre que contenga la búsqueda (case-insensitive)
        categorias = CategoriaMenu.objects.filter(nombre__icontains=search_query)
    else:
        categorias = CategoriaMenu.objects.all().order_by("pk")
    
    context = {
        'categorias_list': categorias  # Usamos 'categorias_list' como clave para la plantilla
    }
    return render(request, 'categorias_menu.html', context)

def crear_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre') or ''
        color = request.POST.get('color') or '#007bff'
        
        if nombre:
                CategoriaMenu.objects.create(nombre=nombre, color=color)
                messages.success(request, f'Categoría "{nombre}" creada con éxito.')
        else:
            messages.error(request, 'El nombre de la categoría no puede estar vacío.')
            
        # Redirigir después de POST para evitar reenvío del formulario
        return redirect('categorias-menu')
        
    # Si se accede por GET (lo cual no debería ocurrir con un modal), simplemente redirecciona
    return redirect('categorias-menu')

def editar_categoria(request, pk):
    categoria = get_object_or_404(CategoriaMenu, pk=pk)
    
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        color = request.POST.get("color")
        
        if nombre:
            categoria.nombre = nombre
            categoria.color = color
        
            categoria.save()
            
            messages.success(request, f'Categoría "{nombre}" actualizada con éxito.')
        else:
            messages.error(request, 'El nombre de la categoría no puede estar vacío.')
        
        return redirect('categorias-menu')
        
    # Si se accede por GET (directamente a la URL de edición), 
    # se podría renderizar un formulario específico, pero aquí redirigimos al listado.
    return redirect('categorias-menu')
            
            
def eliminar_categoria(request, pk):
    print("delete")
    print("request.method", request.method)
    
    if request.method == "POST":
        print("delete")
        
        categoria = get_object_or_404(CategoriaMenu, pk=pk)
        area_nombre = categoria.nombre
        categoria.delete()
        messages.success(request, f'Categoría "{area_nombre}" eliminada correctamente.')
        
    return redirect('categorias-menu')

###############################################################################################################
#                                                    Areas                                                    #
###############################################################################################################
def listar_areas(request):
    
    search_query = request.GET.get('search_name')
    if search_query:
        # Filtrar categorías por nombre que contenga la búsqueda (case-insensitive)
        areas = Area.objects.filter(nombre__icontains=search_query)
    else:
        areas = Area.objects.all().order_by("pk")
    
    context = {
        'areas_list': areas  # Usamos 'categorias_list' como clave para la plantilla
    }
    return render(request, 'area/area.html', context)

def crear_area(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre') or ''
        
        if nombre:
                Area.objects.create(nombre=nombre)
                messages.success(request, f'Aera "{nombre}" creada con éxito.')
        else:
            messages.error(request, 'El nombre del area no puede estar vacío.')
            
        # Buena Práctica: Redirigir después de POST para evitar reenvío del formulario
        return redirect('areas')
        
    # Si se accede por GET (lo cual no debería ocurrir con un modal), simplemente redirecciona
    return redirect('areas')

def editar_area(request, pk):
    area = get_object_or_404(Area, pk=pk)
    
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        
        if nombre:
            area.nombre = nombre
        
            area.save()
            
            messages.success(request, f'Area "{nombre}" actualizada con éxito.')
        else:
            messages.error(request, 'El nombre del area no puede estar vacío.')
        
        return redirect('areas')
        
    # Si se accede por GET (directamente a la URL de edición), 
    # se podría renderizar un formulario específico, pero aquí redirigimos al listado.
    return redirect('areas')
            
            
def eliminar_area(request, pk):
    print("delete")
    print("request.method", request.method)
    
    if request.method == "POST":
        print("delete")
        
        areas = get_object_or_404(Area, pk=pk)
        areas_nombre = areas.nombre
        areas.delete()
        messages.success(request, f'Categoría "{areas_nombre}" eliminada correctamente.')
        
    return redirect('areas')

###############################################################################################################
#                                                     MENU                                                    #
###############################################################################################################
def _is_light(hex_color: str) -> bool:
    hex_color = (hex_color or "").lstrip("#")
    if len(hex_color) != 6:
        return False
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    # luminancia aproximada (perceptual)
    luminance = (0.299*r + 0.587*g + 0.114*b)
    return luminance > 160  # umbral (ajustable)

def listar_menu(request):
    search_query = request.GET.get('search_name')
    if search_query:
        # Filtrar categorías por nombre que contenga la búsqueda (case-insensitive)
        menu = Platillo.objects.filter(nombre__icontains=search_query)
    else:
        menu = Platillo.objects.all().order_by("pk")
    
    for p in menu:
        p.categoria_text_color = "#111" if _is_light(p.categoria.color) else "#fff"

    context = {
        'lista_platillos': menu  # Usamos 'categorias_list' como clave para la plantilla
    }
    return render(request, 'menu/menu.html', context)

def crear_menu(request):
    print(">>>metodo ", request.method)
    if request.method == 'POST':
        nombre = request.POST.get('nombre') or ''
        categoria = request.POST.get('categoria') or ''
        descripcion = request.POST.get('descripcion') or ''
        precio_venta = request.POST.get('precio_venta') or ''
        disponible = request.POST.get('disponible') == 'on'
        es_preparado = request.POST.get('es_preparado') == 'on'
        imagen = request.FILES.get('imagen')
        
        print(">>>>>>>>>>>>>>>>>>>>>>", imagen)
        
        if nombre and precio_venta:
                Platillo.objects.create(
                    nombre = nombre,
                    categoria_id = categoria,
                    imagen=imagen,
                    descripcion = descripcion,
                    precio_venta = precio_venta,
                    disponible = disponible,
                    es_preparado = es_preparado,
                )
                messages.success(request, f'Platillo creado con éxito.')
        else:
            messages.error(request, 'El nombre y precio del platillo no puede estar vacío.')
            
        # Buena Práctica: Redirigir después de POST para evitar reenvío del formulario
        return redirect('menu')
        
    categorias = CategoriaMenu.objects.all()
   
    context = {
        "categorias": categorias    
    }
    return render(request, 'menu/formulario.html', context)

def editar_menu(request, pk):        
    print("request", request.method)
    print("request 2", request.POST.get("imagen"))
    
    if request.method == "POST":
        nombre = request.POST.get('nombre') or ''
        categoria = request.POST.get('categoria') or ''
        descripcion = request.POST.get('descripcion') or ''
        precio_venta = request.POST.get('precio_venta') or ''
        disponible = request.POST.get('disponible') == 'on'
        es_preparado = request.POST.get('es_preparado') == 'on'
        imagen = request.FILES.get('imagen')
        
        if nombre and precio_venta:
            platillo = get_object_or_404(Platillo, pk=pk)
            platillo.nombre = nombre
            if imagen: 
                platillo.imagen = imagen
            platillo.categoria_id = categoria            
            platillo.descripcion = descripcion
            platillo.precio_venta = precio_venta
            platillo.disponible = disponible
            platillo.es_preparado = es_preparado
            
            platillo.save()

            messages.success(request, f'Platillo creado con éxito.')
        else:
            messages.error(request, 'El nombre y precio del platillo no puede estar vacío.')
            
        # redirigir después de POST para evitar reenvío del formulario
        return redirect('menu')
   
    platillo = get_object_or_404(Platillo, pk=pk)
    print(">>>>> platillo: ", platillo.precio_venta)
    categorias = CategoriaMenu.objects.all()
   
    context = {
        "obj": platillo,
        "categorias": categorias    
    }
    return render(request, 'menu/formulario.html', context)
            
            
def eliminar_menu(request, pk):
    print("pk ", pk)
    print("method ", request.method)
    
    if request.method == "POST":
        platillo = get_object_or_404(Platillo, pk=pk)
        platillo_nombre = platillo.nombre
        platillo.delete()
        messages.success(request, f'Categoría "{platillo_nombre}" eliminada correctamente.')
        
    return redirect('menu')

###############################################################################################################
#                                                 Meseros                                                     #
###############################################################################################################
def listar_meseros(request):
    search_query = request.GET.get('search_name')
    if search_query:
        # Filtrar categorías por nombre que contenga la búsqueda (case-insensitive)
        meseros = Mesero.objects.filter(nombre__icontains=search_query)
    else:
        meseros = Mesero.objects.all().order_by("pk")
    context = {
        'lista_meseros': meseros  # Usamos 'categorias_list' como clave para la plantilla
    }
    return render(request, 'meseros/meseros.html', context)


def crear_mesero(request):
    print(">>>metodo ", request.method)
    if request.method == 'POST':
        nombre = request.POST.get('nombre') or ''
        codigo = request.POST.get('codigo') or ''
        activo = request.POST.get('activo') == "on"
        
        if nombre and codigo:
                Mesero.objects.create(
                    nombre = nombre,
                    codigo = codigo,
                    activo=activo,
                )
                messages.success(request, f'Mesero creado con exito.')
        else:
            messages.error(request, 'El nombre y codigo del mesero no pueden estar vacíos.')
            
        # Buena Práctica: Redirigir después de POST para evitar reenvío del formulario
        return redirect('meseros-lista')
        
    return render(request, 'meseros/formulario.html')

def editar_mesero(request, pk):        
    print("request", request.method)
    print("request 2", request.POST.get("imagen"))
    
    if request.method == "POST":
        nombre = request.POST.get('nombre') or ''
        codigo = request.POST.get('codigo') or ''
        activo = request.POST.get('activo') == "on"
        
        
        if nombre and codigo:
            mesero = get_object_or_404(Mesero, pk=pk)
            mesero.nombre = nombre
            mesero.codigo = codigo            
            mesero.activo = activo
            mesero.save()

            messages.success(request, f'Mesero creado con éxito.')
        else:
            messages.error(request, 'El nombre y codigo del mesero no puede estar vacío.')
            
        # redirigir después de POST para evitar reenvío del formulario
        return redirect('meseros-lista')
   
    mesero = get_object_or_404(Mesero, pk=pk)
    context = {
        "mesero": mesero    
    }
    return render(request, 'meseros/formulario.html', context)

def eliminar_mesero(request, pk):
    print("pk ", pk)
    print("method ", request.method)
    
    if request.method == "POST":
        mesero = get_object_or_404(Mesero, pk=pk)
        mesero_nombre = mesero.nombre
        mesero.delete()
        messages.success(request, f'Mesero "{mesero_nombre}" eliminado correctamente.')
        
    return redirect('meseros-lista')

###############################################################################################################
#                                                  Mesas                                                      #
###############################################################################################################
def _parse_dt(value: str | None):
    """
    Convierte strings tipo '2025-12-16T09:43' a datetime aware (con TZ).
    Si viene vacío => None.
    """
    if not value:
        return None

    dt = parse_datetime(value)  # intenta parsear ISO
    if dt is None:
        # fallback para datetime-local sin segundos
        dt = datetime.fromisoformat(value)

    # Si viene naive (sin tz) lo asumimos en zona horaria local del sistema
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_current_timezone())

    return dt


def listar_mesas(request):
    search_query = request.GET.get('search_name')
    if search_query:
        # Filtrar categorías por nombre que contenga la búsqueda (case-insensitive)
        mesas = Mesa.objects.filter(numero__icontains=search_query)
    else:
        mesas = Mesa.objects.all().order_by("pk")
        
    ahora = timezone.localtime()

    asignacion_activa = AsignacionMesa.objects.filter(
    mesa=OuterRef("pk")
    ).filter(
        # Opción A: Es una asignación de tiempo DEFINIDO y está en curso
        Q(
            fecha_inicio__lte=ahora,  # 1. La fecha de inicio ya pasó o es ahora (Comienzo del rango)
            fecha_fin__gte=ahora      # 2. La fecha de fin aún no llega o es ahora (Fin del rango)
        )
        # Opción B: Es una asignación INDEFINIDA (solo tiene fecha_inicio, fecha_fin es NULL)
        | Q(
            fecha_inicio__lte=ahora,  # 1. La fecha de inicio ya pasó o es ahora
            fecha_fin__isnull=True    # 2. No tiene fecha de fin
        )
        # Opción C: Es una asignación FIJA (Si 'es_fija' anula la verificación de tiempo)
        # NOTA: Si 'es_fija' solo significa que el tiempo se ignora, la lógica de tiempo es suficiente.
        # Si significa que debe estar activa independientemente de la fecha_inicio/fin, la dejamos separada.
        | Q(es_fija=True)
    )
    
    mesas = Mesa.objects.annotate(
        tiene_mesero=Exists(asignacion_activa)
    ).order_by("numero")
    
    print("mesas", mesas)
    
    lista_meseros = Mesero.objects.filter(activo=True)

    context = {
        'lista_mesas': mesas,  # Usamos 'categorias_list' como clave para la plantilla
        "lista_meseros": lista_meseros
    }
    return render(request, 'mesas/mesas.html', context)

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

# ASIGNACIONES
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
    # print(">>>>>>>>>>> request.POST.get(activa)", asignacion. )
    

    if request.method == "POST":
        mesa_id = request.POST.get("mesa_id")
        mesero_id = request.POST.get("mesero_id") or ""
        es_fija = request.POST.get("es_fija") == "on"
        activa = request.POST.get("activa") == "on"
        fecha_inicio = _parse_dt(request.POST.get("fecha_inicio"))
        fecha_fin = _parse_dt(request.POST.get("fecha_fin"))

        print(">>>>>>>>>>> activa", request.POST.get("activa") )
        print(">>>>>>>>>>> es_fija", request.POST.get("es_fija") )
        print(">>>>>>>>>>> es_fija 2", es_fija )

        print(">>>>>>>>>>> objeto ", activa )
        print(">>>>>>>>>>> objeto ", activa )
        
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