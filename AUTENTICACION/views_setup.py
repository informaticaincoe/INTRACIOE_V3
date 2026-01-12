from django.core.management import call_command
from django.contrib.auth.models import Group
from django.db.utils import OperationalError
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from FE.models import (
    Departamento, Emisor_fe, Ambiente, Municipio, ActividadEconomica,
    TiposEstablecimientos, TiposDocIDReceptor, Pais
)
from .models import ConfiguracionServidor, UsuarioEmisor

User = get_user_model()

@csrf_exempt
def crear_tipo_documento(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        descripcion = request.POST.get("descripcion")
        tipo = TiposDocIDReceptor.objects.create(codigo=codigo, descripcion=descripcion)
        return JsonResponse({"id": tipo.id, "descripcion": tipo.descripcion})
    return JsonResponse({"error": "Método no permitido"}, status=400)

def crear_pais(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        descripcion = request.POST.get("descripcion")
        pais = Pais.objects.create(codigo=codigo, descripcion=descripcion)
        return JsonResponse({"id": pais.id, "descripcion": pais.descripcion})
    return JsonResponse({"error": "Método no permitido"}, status=405)

def crear_tipo_establecimiento(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        descripcion = request.POST.get("descripcion")
        tipo = TiposEstablecimientos.objects.create(codigo=codigo, descripcion=descripcion)
        return JsonResponse({"id": tipo.id, "descripcion": tipo.descripcion})
    return JsonResponse({"error": "Método no permitido"}, status=405)

def crear_departamento(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        descripcion = request.POST.get("descripcion")
        pais_id = request.POST.get("pais")  # vendrá del select
        departamento = Departamento.objects.create(
            codigo=codigo, descripcion=descripcion, pais_id=pais_id
        )
        return JsonResponse({"id": departamento.id, "descripcion": departamento.descripcion})
    return JsonResponse({"error": "Método no permitido"}, status=405)


def crear_ambiente(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        descripcion = request.POST.get("descripcion")
        ambiente = Ambiente.objects.create(codigo=codigo, descripcion=descripcion)
        return JsonResponse({"id": ambiente.id, "descripcion": ambiente.descripcion})
    return JsonResponse({"error": "Método no permitido"}, status=405)

def crear_municipio(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        descripcion = request.POST.get("descripcion")
        municipio = Municipio.objects.create(codigo=codigo, descripcion=descripcion, departamento_id=1)  
        # ⚠️ Aquí debes asignar un departamento válido por defecto o capturar desde el modal
        return JsonResponse({"id": municipio.id, "descripcion": municipio.descripcion})
    return JsonResponse({"error": "Método no permitido"}, status=405)

def crear_actividad(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        descripcion = request.POST.get("descripcion")
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
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            role = request.POST["role"]

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
            emisor = Emisor_fe.objects.create(
                nit=request.POST["nit"],
                nrc=request.POST.get("nrc"),
                nombre_razon_social=request.POST["nombre_razon_social"],
                tipoestablecimiento_id=request.POST["tipoestablecimiento"],
                municipio_id=request.POST["municipio"],
                direccion_comercial=request.POST["direccion_comercial"],
                telefono=request.POST.get("telefono"),
                email=request.POST.get("email"),
                codigo_establecimiento=request.POST.get("codigo_establecimiento"),
                codigo_punto_venta=request.POST.get("codigo_punto_venta"),
                ambiente_id=request.POST["ambiente"],
                nombre_comercial=request.POST.get("nombre_comercial"),
                nombre_establecimiento=request.POST.get("nombre_establecimiento"),
                tipo_documento_id=request.POST["tipo_documento"],
            )

            # ManyToMany actividades
            actividades_ids = request.POST.getlist("actividades_economicas")
            emisor.actividades_economicas.set(actividades_ids)

            # Vincular con admin existente
            admin = User.objects.filter(is_superuser=True).first()
            if admin:
                UsuarioEmisor.objects.create(user=admin, emisor=emisor, es_predeterminado=True)

            messages.success(request, "Empresa creada y vinculada ✅")
            return redirect("/setup/?step=servidor")

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

    # Paso 3: Configuración del servidor
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
