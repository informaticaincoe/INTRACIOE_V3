
from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from INVENTARIO.models import Producto, TipoItem, TipoUnidadMedida
from RESTAURANTE.models import Area, AreaCocina, CategoriaMenu, Platillo
from django.core.paginator import Paginator
from django.db.models import Q
###############################################################################################################
#                                            CONFIG RESTAURANTE                                               #
###############################################################################################################
"""
MANEJO DE:
    - Areas
    - CategoriaMenu
    - Platillo (menú)
"""

def listar_categorias(request):
    
    search_query = request.GET.get('search_name')
    if search_query:
        categorias = CategoriaMenu.objects.filter(nombre__icontains=search_query) # Busqueda por nombre
    else:
        categorias = CategoriaMenu.objects.all().order_by("pk")
    
    context = {
        'categorias_list': categorias  # lista que contiene todas las categorias
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
        
    # Si se accede por GET, simplemente redirecciona
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
        'areas_list': areas  # lista de areas
    }
    return render(request, 'area/area.html', context)

def crear_area(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre') or ''
        
        if nombre:
            Area.objects.create(nombre=nombre)
            messages.success(request, f'Area "{nombre}" creada con éxito.')
        else:
            messages.error(request, 'El nombre del area no puede estar vacío.')
            
        # Redirigir después de POST para evitar reenvío del formulario
        return redirect('areas')
        
    # Si se accede por GET, simplemente redirecciona
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
        
    # Redirigir después de POST para evitar reenvío del formulario 
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
#                                                    Areas                                                    #
###############################################################################################################
def listar_areas_cocina(request):
    search_query = request.GET.get('search_name')
    if search_query:
        # Filtrar categorías por nombre que contenga la búsqueda (case-insensitive)
        areas_cocina = AreaCocina.objects.filter(area_cocina__icontains=search_query)
    else:
        areas_cocina = AreaCocina.objects.all().order_by("pk")
    
    context = {
        'areas_cocina_list': areas_cocina  # lista de areas
    }
    return render(request, 'area_cocina/list.html', context)

def crear_area_cocina(request):
    if request.method == 'POST':
        print("AAAAAA")
        
        nombre = request.POST.get('nombre') or ''
        print("nombre ", nombre)
        
        if nombre:
            AreaCocina.objects.create(area_cocina=nombre)
            messages.success(request, f'Area de cocina "{nombre}" creada con éxito.')
            
        else:
            messages.error(request, 'El nombre del area no puede estar vacío.')
            
        # Redirigir después de POST para evitar reenvío del formulario
        return redirect('areas-cocina')
        
    # Si se accede por GET, simplemente redirecciona
    return redirect('areas-cocina')

def editar_area_cocina(request, pk):
    area_cocina = get_object_or_404(AreaCocina, pk=pk)
    
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        
        if area_cocina:
            area_cocina.area_cocina = nombre
        
            area_cocina.save()
            
            messages.success(request, f'Area "{nombre}" actualizada con éxito.')
        else:
            messages.error(request, 'El nombre del area no puede estar vacío.')
        
        return redirect('areas-cocina')
        
    # Redirigir después de POST para evitar reenvío del formulario 
    return redirect('areas-cocina')
            
            
def eliminar_area_cocina(request, pk):
    print("delete")
    print("request.method", request.method)
    
    if request.method == "POST":
        print("delete")
        
        area = get_object_or_404(AreaCocina, pk=pk)
        area_cocina = area.area_cocina
        area.delete()
        messages.success(request, f'Categoría "{area_cocina}" eliminada correctamente.')
        
    return redirect('areas-cocina')

###############################################################################################################
#                                                     MENU                                                    #
###############################################################################################################
#Funcion para determinar el color de letra que queda mejor dependiendo de la saturacion del fondo
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
    q = (request.GET.get('q') or '').strip()
    print("Filtros q: ", q)
    qs = Platillo.objects.filter(nombre__icontains=q) # Filtrar categorías por nombre
    if q:
        qs = qs.filter(Q(nombre__contains=q) | Q(codigo__contains=q))
    qs = qs.order_by('id')
    paginator = Paginator(qs, 10)
    page = paginator.get_page(request.GET.get('page'))
    
    for platillo in qs:
        platillo.categoria_text_color = "#111" if _is_light(platillo.categoria.color) else "#fff"

    context = {
        'lista_platillos': page,
        'q': q,
        'page':page,        
    }
    return render(request, 'menu/menu.html', context)

def crear_menu(request):
    print(">>>metodo ", request.method)
    if request.method == 'POST':
        codigo = request.POST.get('codigo') or ''
        nombre = request.POST.get('nombre') or ''
        categoria = request.POST.get('categoria') or ''
        descripcion = request.POST.get('descripcion') or ''
        precio_venta = request.POST.get('precio_venta') or ''
        disponible = request.POST.get('disponible') == 'on'
        es_preparado = request.POST.get('es_preparado') == 'on'
        imagen = request.FILES.get('imagen')
        area_cocina_id = request.POST.get("area_cocina") or None
        
        tipo_item = get_object_or_404(TipoItem, codigo="1") #tipo bien
        unidad_medida = get_object_or_404(TipoUnidadMedida, codigo="59") #tipo bien
        
        if es_preparado and not platillo.area_cocina:
            raise ValidationError("El platillo preparado debe tener un área de cocina.")

        if nombre and precio_venta:
                Platillo.objects.create(
                    codigo = codigo,
                    nombre = nombre,
                    categoria_id = categoria,
                    referencia_interna = codigo,
                    imagen=imagen,
                    tipo_item=tipo_item,
                    unidad_medida=unidad_medida,
                    descripcion = descripcion,
                    precio_venta = precio_venta,
                    disponible = disponible,
                    es_preparado = es_preparado,
                    area_cocina = area_cocina_id 
                )
                messages.success(request, f'Platillo creado con éxito.')
        else:
            messages.error(request, 'El nombre y precio del platillo no puede estar vacío.')
            
        # Redirigir después de POST para evitar reenvío del formulario
        return redirect('menu')
        
    categorias = CategoriaMenu.objects.all()
    areas_cocina = AreaCocina.objects.all()
   
    context = {
        "categorias": categorias,
        'areas_cocina': areas_cocina,
    }
    return render(request, 'menu/formulario.html', context)

def editar_menu(request, pk):
    if request.method == "POST":
        codigo = request.POST.get('codigo') or ''
        nombre = request.POST.get('nombre') or ''
        categoria = request.POST.get('categoria') or ''
        descripcion = request.POST.get('descripcion') or ''
        precio_venta = request.POST.get('precio_venta') or ''
        disponible = request.POST.get('disponible') == 'on'
        es_preparado = request.POST.get('es_preparado') == 'on'
        imagen = request.FILES.get('imagen')
        area_cocina_id = request.POST.get("area_cocina") or None
        
        if nombre and precio_venta:
            platillo = get_object_or_404(Platillo, pk=pk)
            platillo.codigo = codigo
            platillo.nombre = nombre
            if imagen: 
                platillo.imagen = imagen
            platillo.categoria_id = categoria            
            platillo.descripcion = descripcion
            platillo.precio_venta = precio_venta
            platillo.disponible = disponible
            platillo.es_preparado = es_preparado
            platillo.area_cocina = area_cocina_id 
            
            producto = get_object_or_404(Producto, codigo=codigo)
            
            producto.codigo = codigo
            producto.descripcion = nombre
            producto.preunitario = precio_venta
            producto.precio_venta = precio_venta
            producto.imagen = imagen

            if platillo.es_preparado and not platillo.area_cocina:
                raise ValidationError("El platillo preparado debe tener un área de cocina.")

            platillo.save()
            producto.save()
            
            messages.success(request, f'Platillo creado con éxito.')
            
        
        else:
            messages.error(request, 'El nombre y precio del platillo no puede estar vacío.')
            
        # redirigir después de POST para evitar reenvío del formulario
        return redirect('menu')
   
    platillo = get_object_or_404(Platillo, pk=pk)
    categorias = CategoriaMenu.objects.all()
    areas_cocina = AreaCocina.objects.all()

    context = {
        "obj": platillo,
        "categorias": categorias,    
        'areas_cocina': areas_cocina,
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
