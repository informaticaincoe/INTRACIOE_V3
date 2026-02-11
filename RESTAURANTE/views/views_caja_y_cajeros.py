from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from AUTENTICACION import models
from RESTAURANTE.models import (
    BilletesYMonedas,
    Caja,
    CajaDetalleArqueo,
    Cajero,
    MovimientosCaja,
    Pedido,
)

def caja(request):
    return render(request, "caja/apertura_caja.html")

def _get_perfil(request):
    # Si no tienes related_name, ajusta aquí:
    return request.user.perfilusuario

def _get_caja_abierta(perfil):
    return (
        Caja.objects
        .filter(estado="ABIERTA")
        .order_by("-fecha_apertura")
        .first()
    )

##########################################################################################################
#                                               caja views                                              #
##########################################################################################################
def caja_dashboard(request):
    perfil = _get_perfil(request)
    caja = _get_caja_abierta(perfil)

    # Si no hay caja abierta, manda a apertura
    if not caja:
        return redirect("caja") 

    # Totales de movimientos
    tot_ingresos = (
        MovimientosCaja.objects
        .filter(caja=caja, tipo_movimiento="INGRESO")
        .aggregate(s=Coalesce(Sum("monto"), Decimal("0.00")))["s"]
    )
    
    tot_retiros = (
        MovimientosCaja.objects
        .filter(caja=caja, tipo_movimiento="RETIRO")
        .aggregate(s=Coalesce(Sum("monto"), Decimal("0.00")))["s"]
    )

    # Esperado: monto inicial + efectivo + ingresos - retiros
    esperado = (
        (caja.monto_inicial or Decimal("0.00")) +
        (caja.total_efectivo or Decimal("0.00")) +
        (tot_ingresos or Decimal("0.00")) -
        (tot_retiros or Decimal("0.00"))
    ).quantize(Decimal("0.01"))

    # Detalle apertura (para mostrar el arqueo inicial)
    detalle_apertura = (
        CajaDetalleArqueo.objects
        .filter(caja=caja, tipo="APERTURA")
        .select_related("denominacion")
        .order_by(F("denominacion__valor").desc())
    )

    # Movimientos recientes
    movimientos = (
        MovimientosCaja.objects
        .filter(caja=caja)
        .select_related("autorizado_por")
        .order_by("-fecha")[:30]
    )

    context = {
        "caja": caja,
        "tot_ingresos": (tot_ingresos or Decimal("0.00")).quantize(Decimal("0.01")),
        "tot_retiros": (tot_retiros or Decimal("0.00")).quantize(Decimal("0.01")),
        "esperado": esperado,
        "detalle_apertura": detalle_apertura,
        "movimientos": movimientos,
    }
    return render(request, "caja/dashboard_caja.html", context)

@transaction.atomic
def apertura_caja(request):
    # 1. Obtener el PERFIL real, no el User
    # Usamos la función que ya tienes definida o el related_name
    try:
        perfil_instancia = request.user.perfilusuario 
    except AttributeError:
        messages.error(request, "Tu usuario no tiene un perfil asociado.")
        return redirect("index")
    print("USUsARIO CAJA ", perfil_instancia)
    print("user role ", request.user.role)
    
    # 2. Seguridad de rol (Corregido el error de lógica anterior)
    if request.user.role not in ("cajero", "admin", "supervisor"):
        messages.error(request, "No tienes permisos para manejar caja.")
        print("No tiene permisos caja")
        
        return redirect("index")
        
    # 3. Evitar doble apertura
    if Caja.objects.filter(estado="ABIERTA").exists():
        print("Cajaa ya abierta")
        messages.info(request, "Ya existe una caja abierta.")
        return redirect("caja-dashboard")
        
    denominaciones = BilletesYMonedas.objects.all().order_by("-valor")
    
    # Buscamos la denominación de $1.00 para usarla como "Monto Global" si el usuario no desglosa
    den_global = BilletesYMonedas.objects.filter(valor=Decimal("1.00")).first()

    if request.method == "POST":
        # Capturamos lo que viene del input "Monto Global"
        monto_input = Decimal(request.POST.get("monto_inicial") or "0").quantize(Decimal("0.01"))
        
        total_desglose = Decimal("0.00")
        registros_detalles = []
        hubo_desglose_manual = False

        # 1. Procesar billetes primero
        for den in denominaciones:
            qty_str = request.POST.get(f"den_{den.id}")
            if qty_str and int(qty_str) > 0:
                qty = int(qty_str)
                hubo_desglose_manual = True
                
                # Solo preparamos el objeto, no lo guardamos aún
                registros_detalles.append(CajaDetalleArqueo(
                    denominacion=den,
                    tipo="APERTURA",
                    cantidad=qty
                ))
                total_desglose += (den.valor * qty)

        total_desglose = total_desglose.quantize(Decimal("0.01"))

        # 2. DEFINIR MONTO REAL DE APERTURA
        # Si el usuario desglosó billetes, el monto real es esa suma.
        # Si no desglosó, usamos el monto escrito manualmente.
        monto_final_apertura = total_desglose if hubo_desglose_manual else monto_input

        if monto_final_apertura <= 0:
            messages.error(request, "El monto de apertura debe ser mayor a 0.")
            return render(request, "caja/apertura_caja.html", {"denominaciones": denominaciones})

        # 3. CREAR LA CAJA
        caja = Caja.objects.create(
            usuario=perfil_instancia,
            monto_inicial=monto_final_apertura,
            estado="ABIERTA",
        )

        # 4. GUARDAR DETALLES
        if hubo_desglose_manual:
            # Asignamos la caja creada a cada detalle
            for detalle in registros_detalles:
                detalle.caja = caja
            CajaDetalleArqueo.objects.bulk_create(registros_detalles)
        else:
            # Si no hubo desglose, usamos la moneda de $1.00 como comodín
            if den_global:
                CajaDetalleArqueo.objects.create(
                    caja=caja,
                    denominacion=den_global,
                    tipo="APERTURA",
                    cantidad=monto_final_apertura
                )
            else:
                transaction.set_rollback(True)
                messages.error(request, "Falta configuración de denominación de $1.00.")
                return render(request, "caja/apertura_caja.html", {"denominaciones": denominaciones})

        messages.success(request, f"Caja abierta exitosamente con ${monto_final_apertura}")
        return redirect("caja-dashboard")

    return render(request, "caja/apertura_caja.html", {"denominaciones": denominaciones})

@transaction.atomic
def caja_registrar_movimiento(request):
    perfil = _get_perfil(request)
    caja = _get_caja_abierta(perfil)
    if not caja:
        messages.error(request, "No hay caja abierta.")
        return redirect("caja")

    if request.method != "POST":
        return redirect("caja-dashboard")

    tipo = request.POST.get("tipo_movimiento")  # INGRESO / RETIRO
    categoria = request.POST.get("categoria") or "OTROS"
    motivo = (request.POST.get("motivo") or "").strip()
    monto = Decimal(request.POST.get("monto") or "0")

    if tipo not in ("INGRESO", "RETIRO"):
        messages.error(request, "Tipo de movimiento inválido.")
        return redirect("caja-dashboard")

    if monto <= 0:
        messages.error(request, "El monto debe ser mayor a 0.")
        return redirect("caja-dashboard")

    if not motivo:
        messages.error(request, "Debes ingresar un motivo.")
        return redirect("caja-dashboard")

    MovimientosCaja.objects.create(
        caja=caja,
        tipo_movimiento=tipo,
        categoria=categoria,
        motivo=motivo,
        monto=monto,
        autorizado_por=perfil,
    )

    messages.success(request, f"{tipo.title()} registrado.")
    return redirect("caja-dashboard")

def cierre_caja(request):
    perfil = _get_perfil(request)
    # Obtener la caja abierta del usuario actual
    caja = get_object_or_404(Caja, estado='ABIERTA')

    # Calcular totales de movimientos usando Sum y Coalesce (como lo tienes arriba)
    pedidos_abiertos = Pedido.objects.filter(estado="ABIERTO")
    
    if pedidos_abiertos.exists():
        # Cambié success por error porque es un impedimento
        messages.error(
            request, 
            "No se puede cerrar la caja: Existen pedidos abiertos en el sistema.", 
            extra_tags="cierre_pedidos_pendientes"
        )
        return redirect('caja-dashboard')
    
    ingresos_manuales = (
        MovimientosCaja.objects
        .filter(caja=caja, tipo_movimiento="INGRESO")
        .aggregate(s=Coalesce(Sum("monto"), Decimal("0.00")))["s"]
    )
    
    retiros_manuales = (
        MovimientosCaja.objects
        .filter(caja=caja, tipo_movimiento="RETIRO")
        .aggregate(s=Coalesce(Sum("monto"), Decimal("0.00")))["s"]
    )
    
    # SALDO ESPERADO = Inicial + Efectivo + Ingresos - Retiros
    # Usamos valores por defecto en caso de que algún campo sea None
    monto_inicial = caja.monto_inicial or Decimal("0.00")
    total_efectivo = caja.total_efectivo or Decimal("0.00")
    
    esperado = (monto_inicial + total_efectivo + ingresos_manuales - retiros_manuales).quantize(Decimal("0.01"))

    if request.method == 'POST':
        with transaction.atomic():
            total_fisico = Decimal('0.00')
            denominaciones = BilletesYMonedas.objects.all()

            for den in denominaciones:
                # Obtenemos la cantidad del POST
                qty_str = request.POST.get(f'den_{den.id}', '0')
                cantidad = int(qty_str) if qty_str.isdigit() else 0
                
                if cantidad > 0:
                    # Guardar detalle de arqueo de CIERRE
                    CajaDetalleArqueo.objects.create(
                        caja=caja,
                        denominacion=den,
                        tipo='CIERRE',
                        cantidad=cantidad
                    )
                    total_fisico += den.valor * cantidad

            # Actualizar datos finales de la caja
            caja.monto_final = total_fisico.quantize(Decimal("0.01"))
            caja.diferencia = (total_fisico - esperado).quantize(Decimal("0.01"))
            caja.monto_cierre = total_fisico.quantize(Decimal("0.01"))
            caja.observaciones = request.POST.get('observaciones', '')
            caja.fecha_cierre = timezone.now()
            caja.estado = 'CERRADA'
            caja.save()

            messages.success(request, f"Caja #{caja.id} cerrada con éxito.")
            return redirect('caja-dashboard') 

    # GET: Preparar datos para el template
    denominaciones = BilletesYMonedas.objects.all().order_by('-valor')
    print(">>>>>>>>>>>>>> ", MovimientosCaja.objects.filter(caja=caja, tipo_movimiento="RETIRO"))
    print(">>>>>>>>>>>>>> ", MovimientosCaja.objects.filter(caja=caja, tipo_movimiento="INGRESO"))
    print(">>>>>>>>>>>>>> ", ingresos_manuales)
    
    context = {
        'caja': caja,
        'denominaciones': denominaciones,
        'esperado': esperado,
        'tot_ingresos': ingresos_manuales,
        'tot_retiros': retiros_manuales,
        'retiros_lista': MovimientosCaja.objects.filter(caja=caja, tipo_movimiento="RETIRO"),
        'ingresos_lista': MovimientosCaja.objects.filter(caja=caja, tipo_movimiento="INGRESO")
    }
    return render(request, 'caja/cierre_caja.html', context)

##########################################################################################################
#                                        Billetes y monedas views                                        #
##########################################################################################################
def billetes_y_monedas_list(request):
    if request.method == "GET":
        billetes_Y_monedas_list = BilletesYMonedas.objects.all()
        context = {
            "billetas_Y_monedas_list": billetes_Y_monedas_list 
        }
        
        return render(request, "caja/billetes_y_monedas_list.html", context)

def billetes_y_monedas_crear(request):    
    nombre = request.POST.get("nombre")
    valor = request.POST.get("valor")
        
    if request.method == "POST":
        
        BilletesYMonedas.objects.create(nombre=nombre, valor=valor)
        messages.success(request, "Billete/Moneda creado con éxito.")
        return redirect("billetes-y-monedas-list")
    
    return redirect("billetes-y-monedas-list")
    
    
def billetes_y_monedas_editar(request, pk):
    billete = get_object_or_404(BilletesYMonedas, pk=pk)
    
    if request.method == "POST":
        billete.nombre = request.POST.get("nombre")
        billete.valor = request.POST.get("valor")
        billete.save()
        messages.success(request, f'Registro "{billete.nombre}" actualizado.')
        return redirect("billetes-y-monedas-list")
    
    return redirect("billetes-y-monedas-list")

def billetes_y_monedas_eliminar(request, pk):
    if request.method == "POST":
        billete = get_object_or_404(BilletesYMonedas, pk=pk)
        nombre_tmp = billete.nombre
        billete.delete()
        messages.success(request, f'Se eliminó "{nombre_tmp}" correctamente.')
    return redirect("billetes-y-monedas-list")

##########################################################################################################
#                                            Cajeros views                                              #
##########################################################################################################
def listar_cajeros(request):
    search_query = request.GET.get('search_name')
    if search_query:
        cajero = Cajero.objects.filter(nombre__icontains=search_query) # Filtrar cajero por nombre
    else:
        cajero = Cajero.objects.all().order_by("pk")
        
    print(">>>>>>>>>> CAJERO ", cajero)
    context = {
        'lista_cajero': cajero  # Lista de cajero
    }
    return render(request, 'cajero/cajero.html', context)


def crear_cajero(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre') or ''
        pin = request.POST.get('pin') or ''
        activo = request.POST.get('activo') == "on"
        
        print("pin")
        
        if nombre and pin:
                Cajero.objects.create(
                    nombre = nombre,
                    pin = pin,
                    activo=activo,
                )
                messages.success(request, f'Cajero creado con exito.')
        else:
            messages.error(request, 'El nombre y pin del cajero no pueden estar vacíos.')
            
        # Redirigir después de POST para evitar reenvío del formulario
        return redirect('cajero-lista')
        
    return render(request, 'cajero/formulario.html')

def editar_cajero(request, pk):
    if request.method == "POST":
        nombre = request.POST.get('nombre') or ''
        pin = request.POST.get('pin') or ''
        activo = request.POST.get('activo') == "on"
        
        
        if nombre and pin:
            cajero = get_object_or_404(Cajero, pk=pk)
            cajero.nombre = nombre
            cajero.pin = pin            
            cajero.activo = activo
            cajero.save()

            messages.success(request, f'Cajero ha sido creado con éxito.')
        else:
            messages.error(request, 'El nombre y pin del cajeros no puede estar vacío.')
            
        # redirigir después de POST para evitar reenvío del formulario
        return redirect('cajero-lista')
   
    cajero = get_object_or_404(Cajero, pk=pk)
    context = {
        "cajero": cajero    
    }
    return render(request, 'cajero/formulario.html', context)

def eliminar_cajero(request, pk):
    print("pk ", pk)
    print("method ", request.method)
    
    if request.method == "POST":
        cajero = get_object_or_404(Cajero, pk=pk)
        cajero_nombre = cajero.nombre
        cajero.delete()
        messages.success(request, f'cajero "{cajero_nombre}" eliminado correctamente.')
        
    return redirect('cajero-lista')