from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Producto, MovimientoInventario, Compra, DevolucionVenta, DevolucionCompra, Categoria, UnidadMedida, Impuesto, Almacen

# Listar productos
def listar_productos(request):
    query = request.GET.get('q', '')  # Capturar el valor del buscador
    productos_list = Producto.objects.all()

    # Filtrar por código o descripción si se ingresó un criterio de búsqueda
    if query:
        productos_list = productos_list.filter(codigo__icontains=query) | productos_list.filter(descripcion__icontains=query)

    # Paginación
    paginator = Paginator(productos_list, 10)  # Mostrar 10 productos por página
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)

    return render(request, 'productos/lista.html', {
        'productos': productos,
        'query': query
    })

# Crear producto
def crear_producto(request):
    categorias = Categoria.objects.all()
    unidades_medida = UnidadMedida.objects.all()
    #descuentos = Descuento.objects.all()
    impuestos = Impuesto.objects.all()
    almacenes = Almacen.objects.all()

    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        descripcion = request.POST.get('descripcion')
        categoria_id = request.POST.get('categoria')
        unidad_medida_id = request.POST.get('unidad_medida')
        precio_compra = request.POST.get('precio_compra')
        precio_venta = request.POST.get('precio_venta')
        stock = request.POST.get('stock')
        stock_minimo = request.POST.get('stock_minimo')
        stock_maximo = request.POST.get('stock_maximo')
        #tiene_descuento = request.POST.get('tiene_descuento') == 'on'
        #descuento_id = request.POST.get('descuento') if tiene_descuento else None
        impuesto_ids = request.POST.getlist('impuestos')
        maneja_lotes = request.POST.get('maneja_lotes') == 'on'
        fecha_vencimiento = request.POST.get('fecha_vencimiento') if maneja_lotes else None
        almacen_ids = request.POST.getlist('almacenes') if maneja_lotes else []
        imagen = request.FILES.get('imagen')

        producto = Producto.objects.create(
            codigo=codigo,
            descripcion=descripcion,
            categoria_id=categoria_id,
            unidad_medida_id=unidad_medida_id,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            stock=stock,
            stock_minimo=stock_minimo,
            stock_maximo=stock_maximo,
            # tiene_descuento=tiene_descuento,
            # escuento_id=descuento_id,
            maneja_lotes=maneja_lotes,
            fecha_vencimiento=fecha_vencimiento,
            imagen=imagen
        )

        producto.impuestos.set(impuesto_ids)
        producto.almacenes.set(almacen_ids)

        return redirect('productos-lista')

    return render(request, 'productos/formulario.html', {
        'categorias': categorias,
        'unidades_medida': unidades_medida,
        #'descuentos': descuentos,
        'impuestos': impuestos,
        'almacenes': almacenes
    })

# Editar producto sin forms.py
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.codigo = request.POST.get('codigo')
        producto.descripcion = request.POST.get('descripcion')
        producto.precio_venta = request.POST.get('precio_venta')
        producto.stock = request.POST.get('stock')
        producto.save()
        return redirect('productos-lista')
    return render(request, 'productos/formulario.html', {'producto': producto})

# Eliminar producto
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos-lista')
    return render(request, 'productos/confirmar_eliminar.html', {'producto': producto})

# Listar movimientos de inventario
def listar_movimientos(request):
    movimientos = MovimientoInventario.objects.all()
    return render(request, 'inventario/lista.html', {'movimientos': movimientos})

# Crear movimiento de inventario sin forms.py
def crear_movimiento(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        cantidad = request.POST.get('cantidad')
        tipo = request.POST.get('tipo')
        referencia = request.POST.get('referencia', '')
        producto = get_object_or_404(Producto, pk=producto_id)
        MovimientoInventario.objects.create(
            producto=producto, cantidad=cantidad, tipo=tipo, referencia=referencia
        )
        return redirect('movimientos-lista')
    return render(request, 'inventario/formulario.html')

# Listar compras
def listar_compras(request):
    compras = Compra.objects.all()
    return render(request, 'compras/lista.html', {'compras': compras})

# Crear compra sin forms.py
def crear_compra(request):
    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor')
        total = request.POST.get('total')
        Compra.objects.create(proveedor_id=proveedor_id, total=total)
        return redirect('compras-lista')
    return render(request, 'compras/formulario.html')

# Listar devoluciones de venta
def listar_devoluciones_venta(request):
    devoluciones = DevolucionVenta.objects.all()
    return render(request, 'devoluciones_venta/lista.html', {'devoluciones': devoluciones})

# Crear devolución de venta sin forms.py
def crear_devolucion_venta(request):
    if request.method == 'POST':
        num_factura = request.POST.get('num_factura')
        motivo = request.POST.get('motivo')
        DevolucionVenta.objects.create(num_factura=num_factura, motivo=motivo)
        return redirect('devoluciones-venta-lista')
    return render(request, 'devoluciones_venta/formulario.html')

# Listar devoluciones de compra
def listar_devoluciones_compra(request):
    devoluciones = DevolucionCompra.objects.all()
    return render(request, 'devoluciones_compra/lista.html', {'devoluciones': devoluciones})

# Crear devolución de compra sin forms.py
def crear_devolucion_compra(request):
    if request.method == 'POST':
        compra_id = request.POST.get('compra')
        motivo = request.POST.get('motivo')
        DevolucionCompra.objects.create(compra_id=compra_id, motivo=motivo)
        return redirect('devoluciones-compra-lista')
    return render(request, 'devoluciones_compra/formulario.html')


# ---- VISTAS PARA CATEGORÍAS ----
def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/lista.html', {'categorias': categorias})

def crear_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        Categoria.objects.create(nombre=nombre, descripcion=descripcion)
        return redirect('categorias-lista')
    return render(request, 'categorias/formulario.html')

def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.nombre = request.POST.get('nombre')
        categoria.descripcion = request.POST.get('descripcion')
        categoria.save()
        return redirect('categorias-lista')
    return render(request, 'categorias/formulario.html', {'categoria': categoria})

def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categorias-lista')
    return render(request, 'categorias/confirmar_eliminar.html', {'categoria': categoria})

# ---- VISTAS PARA UNIDADES DE MEDIDA ----
def listar_unidades_medida(request):
    unidades = UnidadMedida.objects.all()
    return render(request, 'unidades_medida/lista.html', {'unidades': unidades})

def crear_unidad_medida(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        abreviatura = request.POST.get('abreviatura')
        UnidadMedida.objects.create(nombre=nombre, abreviatura=abreviatura)
        return redirect('unidades-lista')
    return render(request, 'unidades_medida/formulario.html')

def editar_unidad_medida(request, pk):
    unidad = get_object_or_404(UnidadMedida, pk=pk)
    if request.method == 'POST':
        unidad.nombre = request.POST.get('nombre')
        unidad.abreviatura = request.POST.get('abreviatura')
        unidad.save()
        return redirect('unidades-lista')
    return render(request, 'unidades_medida/formulario.html', {'unidad': unidad})

def eliminar_unidad_medida(request, pk):
    unidad = get_object_or_404(UnidadMedida, pk=pk)
    if request.method == 'POST':
        unidad.delete()
        return redirect('unidades-lista')
    return render(request, 'unidades_medida/confirmar_eliminar.html', {'unidad': unidad})

# ---- VISTAS PARA IMPUESTOS ----
def listar_impuestos(request):
    impuestos = Impuesto.objects.all()
    return render(request, 'impuestos/lista.html', {'impuestos': impuestos})

def crear_impuesto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        porcentaje = request.POST.get('porcentaje')
        Impuesto.objects.create(nombre=nombre, porcentaje=porcentaje)
        return redirect('impuestos-lista')
    return render(request, 'impuestos/formulario.html')

def editar_impuesto(request, pk):
    impuesto = get_object_or_404(Impuesto, pk=pk)
    if request.method == 'POST':
        impuesto.nombre = request.POST.get('nombre')
        impuesto.porcentaje = request.POST.get('porcentaje')
        impuesto.save()
        return redirect('impuestos-lista')
    return render(request, 'impuestos/formulario.html', {'impuesto': impuesto})

def eliminar_impuesto(request, pk):
    impuesto = get_object_or_404(Impuesto, pk=pk)
    if request.method == 'POST':
        impuesto.delete()
        return redirect('impuestos-lista')
    return render(request, 'impuestos/confirmar_eliminar.html', {'impuesto': impuesto})

# ---- VISTAS PARA ALMACENES ----
def listar_almacenes(request):
    almacenes = Almacen.objects.all()
    return render(request, 'almacenes/lista.html', {'almacenes': almacenes})

def crear_almacen(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        ubicacion = request.POST.get('ubicacion')
        responsable = request.POST.get('responsable')
        codigo = request.POST.get('codigo')
        Almacen.objects.create(nombre=nombre, ubicacion=ubicacion, responsable=responsable, codigo=codigo)
        return redirect('almacenes-lista')
    return render(request, 'almacenes/formulario.html')

def editar_almacen(request, pk):
    almacen = get_object_or_404(Almacen, pk=pk)
    if request.method == 'POST':
        almacen.nombre = request.POST.get('nombre')
        almacen.ubicacion = request.POST.get('ubicacion')
        almacen.responsable = request.POST.get('responsable')
        almacen.codigo = request.POST.get('codigo')
        almacen.save()
        return redirect('almacenes-lista')
    return render(request, 'almacenes/formulario.html', {'almacen': almacen})

def eliminar_almacen(request, pk):
    almacen = get_object_or_404(Almacen, pk=pk)
    if request.method == 'POST':
        almacen.delete()
        return redirect('almacenes-lista')
    return render(request, 'almacenes/confirmar_eliminar.html', {'almacen': almacen})
