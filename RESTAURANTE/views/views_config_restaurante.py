
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from INVENTARIO.models import Producto
from RESTAURANTE.models import Area, CategoriaMenu, Platillo

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
                messages.success(request, f'Aera "{nombre}" creada con éxito.')
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
    search_query = request.GET.get('search_name')
    if search_query:
        menu = Platillo.objects.filter(nombre__icontains=search_query) # Filtrar categorías por nombre
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
        codigo = request.POST.get('codigo') or ''
        nombre = request.POST.get('nombre') or ''
        categoria = request.POST.get('categoria') or ''
        descripcion = request.POST.get('descripcion') or ''
        precio_venta = request.POST.get('precio_venta') or ''
        disponible = request.POST.get('disponible') == 'on'
        es_preparado = request.POST.get('es_preparado') == 'on'
        imagen = request.FILES.get('imagen')
        
        if nombre and precio_venta:
                Platillo.objects.create(
                    codigo = codigo,
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
            
        # Redirigir después de POST para evitar reenvío del formulario
        return redirect('menu')
        
    categorias = CategoriaMenu.objects.all()
   
    context = {
        "categorias": categorias    
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
            
            producto = get_object_or_404(Producto, codigo=codigo)
            
            producto.codigo = codigo
            producto.descripcion = nombre
            producto.preunitario = precio_venta
            producto.precio_venta = precio_venta
            producto.imagen = imagen

            platillo.save()
            producto.save()
            
            messages.success(request, f'Platillo creado con éxito.')
            
        
        else:
            messages.error(request, 'El nombre y precio del platillo no puede estar vacío.')
            
        # redirigir después de POST para evitar reenvío del formulario
        return redirect('menu')
   
    platillo = get_object_or_404(Platillo, pk=pk)
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