from django.core.management import call_command
from django.contrib.auth.models import Group
from django.db.utils import OperationalError
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from django.utils import timezone
from FE.models import (
    Departamento, Emisor_fe, Ambiente, Municipio, ActividadEconomica,
    TiposEstablecimientos, TiposDocIDReceptor, Pais
)
from .models import ConfiguracionServidor, UsuarioEmisor, Plan, Suscripcion

User = get_user_model()

def _validar_codigo_descripcion(request):
    """Retorna (codigo, descripcion) o JsonResponse de error si faltan campos."""
    codigo = (request.POST.get("codigo") or "").strip()
    descripcion = (request.POST.get("descripcion") or "").strip()
    if not codigo:
        return None, None, JsonResponse({"error": "El campo código es obligatorio."}, status=400)
    if not descripcion:
        return None, None, JsonResponse({"error": "El campo descripción es obligatorio."}, status=400)
    return codigo, descripcion, None


def crear_tipo_documento(request):
    if request.method == "POST":
        codigo, descripcion, err = _validar_codigo_descripcion(request)
        if err:
            return err
        tipo = TiposDocIDReceptor.objects.create(codigo=codigo, descripcion=descripcion)
        return JsonResponse({"id": tipo.id, "descripcion": tipo.descripcion})
    return JsonResponse({"error": "Método no permitido"}, status=405)

def crear_pais(request):
    if request.method == "POST":
        codigo, descripcion, err = _validar_codigo_descripcion(request)
        if err:
            return err
        pais = Pais.objects.create(codigo=codigo, descripcion=descripcion)
        return JsonResponse({"id": pais.id, "descripcion": pais.descripcion})
    return JsonResponse({"error": "Método no permitido"}, status=405)

def crear_tipo_establecimiento(request):
    if request.method == "POST":
        codigo, descripcion, err = _validar_codigo_descripcion(request)
        if err:
            return err
        tipo = TiposEstablecimientos.objects.create(codigo=codigo, descripcion=descripcion)
        return JsonResponse({"id": tipo.id, "descripcion": tipo.descripcion})
    return JsonResponse({"error": "Método no permitido"}, status=405)

def crear_departamento(request):
    if request.method == "POST":
        codigo, descripcion, err = _validar_codigo_descripcion(request)
        if err:
            return err
        pais_id = (request.POST.get("pais") or "").strip()
        if not pais_id:
            return JsonResponse({"error": "El campo país es obligatorio."}, status=400)
        departamento = Departamento.objects.create(
            codigo=codigo, descripcion=descripcion, pais_id=pais_id
        )
        return JsonResponse({"id": departamento.id, "descripcion": departamento.descripcion})
    return JsonResponse({"error": "Método no permitido"}, status=405)


def crear_ambiente(request):
    if request.method == "POST":
        codigo, descripcion, err = _validar_codigo_descripcion(request)
        if err:
            return err
        ambiente = Ambiente.objects.create(codigo=codigo, descripcion=descripcion)
        return JsonResponse({"id": ambiente.id, "descripcion": ambiente.descripcion})
    return JsonResponse({"error": "Método no permitido"}, status=405)

def crear_municipio(request):
    if request.method == "POST":
        codigo, descripcion, err = _validar_codigo_descripcion(request)
        if err:
            return err
        departamento_id = (request.POST.get("departamento") or "").strip()
        if not departamento_id:
            return JsonResponse({"error": "El campo departamento es obligatorio."}, status=400)
        municipio = Municipio.objects.create(
            codigo=codigo, descripcion=descripcion, departamento_id=departamento_id
        )
        return JsonResponse({"id": municipio.id, "descripcion": municipio.descripcion})
    return JsonResponse({"error": "Método no permitido"}, status=405)

def crear_actividad(request):
    if request.method == "POST":
        codigo, descripcion, err = _validar_codigo_descripcion(request)
        if err:
            return err
        act = ActividadEconomica.objects.create(codigo=codigo, descripcion=descripcion)
        return JsonResponse({"id": act.id, "descripcion": f"{act.codigo} - {act.descripcion}"})
    return JsonResponse({"error": "Método no permitido"}, status=405)

def setup_wizard(request):
    step = request.GET.get("step", "usuario")

    # 🚀 Migraciones automáticas si no existen tablas
    try:
        User.objects.exists()
    except OperationalError:
        call_command("makemigrations", interactive=False, verbosity=0)
        call_command("migrate", interactive=False, verbosity=0)
        messages.info(request, "Se aplicaron las migraciones iniciales automáticamente.")

    # 🚀 Crear roles si no existen
    for nombre in ["Administrador", "Vendedor", "Supervisor", "Cliente"]:
        Group.objects.get_or_create(name=nombre)

    # Paso 1: Crear usuario admin
    if step == "usuario":
        if request.method == "POST":
            username = (request.POST.get("username") or "").strip()
            email = (request.POST.get("email") or "").strip()
            password = request.POST.get("password") or ""
            role = (request.POST.get("role") or "").strip()

            if not username:
                messages.error(request, "El nombre de usuario es obligatorio.")
                return redirect("/setup/?step=usuario")
            if not password or len(password) < 8:
                messages.error(request, "La contraseña debe tener al menos 8 caracteres.")
                return redirect("/setup/?step=usuario")
            if not role:
                messages.error(request, "El rol es obligatorio.")
                return redirect("/setup/?step=usuario")
            if User.objects.filter(username=username).exists():
                messages.error(request, "Ya existe un usuario con ese nombre.")
                return redirect("/setup/?step=usuario")

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=True,
                is_superuser=True
            )

            # Asignar grupo al usuario
            grupo = Group.objects.get(name=role)
            user.groups.add(grupo)

            messages.success(request, "Usuario administrador creado ✅")
            return redirect("/setup/?step=empresa")

        grupos = Group.objects.all()
        return render(request, "setup/usuario.html", {"grupos": grupos})

    # Paso 2: Crear empresa
    elif step == "empresa":
        if request.method == "POST":
            campos_requeridos = {
                "nit": "El NIT es obligatorio.",
                "nombre_razon_social": "La razón social es obligatoria.",
                "tipoestablecimiento": "El tipo de establecimiento es obligatorio.",
                "municipio": "El municipio es obligatorio.",
                "direccion_comercial": "La dirección comercial es obligatoria.",
                "ambiente": "El ambiente es obligatorio.",
                "tipo_documento": "El tipo de documento es obligatorio.",
            }
            for campo, mensaje in campos_requeridos.items():
                if not (request.POST.get(campo) or "").strip():
                    messages.error(request, mensaje)
                    return redirect("/setup/?step=empresa")

            emisor = Emisor_fe.objects.create(
                nit=request.POST["nit"].strip(),
                nrc=request.POST.get("nrc"),
                nombre_razon_social=request.POST["nombre_razon_social"].strip(),
                tipoestablecimiento_id=request.POST["tipoestablecimiento"],
                municipio_id=request.POST["municipio"],
                direccion_comercial=request.POST["direccion_comercial"].strip(),
                telefono=request.POST.get("telefono"),
                email=request.POST.get("email"),
                codigo_establecimiento=request.POST.get("codigo_establecimiento"),
                codigo_punto_venta=request.POST.get("codigo_punto_venta"),
                ambiente_id=request.POST["ambiente"],
                nombre_comercial=request.POST.get("nombre_comercial"),
                nombre_establecimiento=request.POST.get("nombre_establecimiento"),
                tipo_documento_id=request.POST["tipo_documento"],
                color_topbar=request.POST.get("color_topbar", "#0d47a1"),
                color_sidebar=request.POST.get("color_sidebar", "#ffffff"),
            )

            # ManyToMany actividades
            actividades_ids = request.POST.getlist("actividades_economicas")
            emisor.actividades_economicas.set(actividades_ids)

            # Vincular con admin existente
            admin = User.objects.filter(is_superuser=True).first()
            if admin:
                UsuarioEmisor.objects.create(user=admin, emisor=emisor, es_predeterminado=True)

            messages.success(request, "Empresa creada y vinculada ✅")
            return redirect("/setup/?step=plan")

        context = {
            "departamentos": Departamento.objects.all(),
            "paises": Pais.objects.all(),
            "ambientes": Ambiente.objects.all(),
            "municipios": Municipio.objects.all(),
            "actividades": ActividadEconomica.objects.all(),
            "tipos_est": TiposEstablecimientos.objects.all(),
            "tipos_doc": TiposDocIDReceptor.objects.all(),
        }
        return render(request, "setup/empresa.html", context)

    # Paso 3: Plan y suscripción
    elif step == "plan":
        if request.method == "POST":
            nombre_plan = (request.POST.get("nombre_plan") or "").strip()
            if not nombre_plan:
                messages.error(request, "El nombre del plan es obligatorio.")
                return redirect("/setup/?step=plan")

            plan = Plan.objects.create(
                nombre=nombre_plan,
                descripcion=request.POST.get("descripcion_plan", ""),
                tiene_facturacion="tiene_facturacion" in request.POST,
                tiene_ventas="tiene_ventas" in request.POST,
                tiene_compras="tiene_compras" in request.POST,
                tiene_inventario="tiene_inventario" in request.POST,
                tiene_contabilidad="tiene_contabilidad" in request.POST,
                tiene_rrhh="tiene_rrhh" in request.POST,
                tiene_restaurante="tiene_restaurante" in request.POST,
            )

            emisor = Emisor_fe.objects.first()
            if emisor:
                fecha_fin_str = request.POST.get("fecha_fin", "").strip()
                Suscripcion.objects.create(
                    emisor=emisor,
                    plan=plan,
                    fecha_inicio=timezone.now().date(),
                    fecha_fin=fecha_fin_str if fecha_fin_str else None,
                    activo=True,
                )

            messages.success(request, "Plan y suscripción configurados ✅")
            return redirect("/setup/?step=servidor")

        return render(request, "setup/plan.html")

    # Paso 4: Configuración del servidor
    elif step == "servidor":
        claves_fijas = [
            "email_host_fe",
            "consulta_dte",
            "schema_json",
            "user_agent",
            "hacienda_contingencia_url",
            "json_facturas_firmadas",
            "version_evento_contingencia",
            "url_invalidar_dte",
            "content_type",
            "headers",
            "url_autenticacion",
            "version_evento_invalidacion",
            "hacienda_url_prod",
            "hacienda_url_test",
            "certificado",
            "server_url",
            "firmador",
            "json_factura",
            "ruta_comprobante_json",
            "ruta_comprobantes_dte",
        ]

        if request.method == "POST":
            for i, clave in enumerate(claves_fijas, start=1):
                ConfiguracionServidor.objects.create(
                    clave=clave,
                    valor=request.POST.get(f"valor_{i}", ""),
                    url=request.POST.get(f"url_{i}", ""),
                    url_endpoint=request.POST.get(f"url_endpoint_{i}", ""),
                    contraseña=request.POST.get(f"contraseña_{i}", ""),
                    descripcion=request.POST.get(f"descripcion_{i}", ""),
                )
            messages.success(request, "Servidor configurado ✅ Setup completo 🎉")
            return redirect("/")  

        return render(request, "setup/servidor.html", {"claves_fijas": claves_fijas})

    return render(request, "setup/usuario.html")
