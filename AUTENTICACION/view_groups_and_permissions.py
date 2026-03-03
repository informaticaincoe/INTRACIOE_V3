from django.contrib.auth.models import Group, Permission
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

def groups_list(request):
    grupos = Group.objects.all()
    return render(request, "grupos/lista_grupos.html", {"grupos": grupos})

def permisos_list(request):
    permisos = Permission.objects.all()
    
    content_types_list = ContentType.objects.exclude(
        app_label__in=[ 'sessions', 'contenttypes']
    ).order_by('app_label', 'model')
    
    
    
    paginator = Paginator(content_types_list, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    permisos = Permission.objects.filter(content_type__in=page_obj.object_list).select_related('content_type')
    
        
    return render(request, "grupos/lista_permisos.html", {"permisos": permisos})


def permisos_ny_grupo_list(request):    
    grupos = Group.objects.prefetch_related('permissions').annotate(total_permisos=Count('permissions')).all()
    return render(request, 'grupos/list_grupos_x_permisos.html', {'grupos': grupos})

def editar_permisos_grupo(request, grupo_id):
    grupo = get_object_or_404(Group, id=grupo_id)
    permisos_grupo_ids = grupo.permissions.values_list('id', flat=True)
    
    # 1. Obtenemos los modelos y los paginamos
    content_types_list = ContentType.objects.exclude(
        app_label__in=[ 'sessions', 'contenttypes']
    ).order_by('app_label', 'model') # Importante ordenar para la paginación
    
    paginator = Paginator(content_types_list, 20) # Mostrar 10 modelos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 2. Construimos la matriz SOLO para los modelos de la página actual
    matriz = {}
    for ct in page_obj:
        perms_modelo = Permission.objects.filter(content_type=ct)
        
        matriz[ct.model] = {
            'app': ct.app_label,
            'view':   perms_modelo.filter(codename__startswith='view_').first(),
            'add':    perms_modelo.filter(codename__startswith='add_').first(),
            'change': perms_modelo.filter(codename__startswith='change_').first(),
            'delete': perms_modelo.filter(codename__startswith='delete_').first(),
        }
        
        # Optimizamos la verificación: usamos los IDs cargados previamente
        for accion in ['view', 'add', 'change', 'delete']:
            p = matriz[ct.model][accion]
            if p and p.id in permisos_grupo_ids:
                p.active = True

    usuarios_del_grupo = grupo.user_set.all()
    
    print("***** usuarios_del_grupo ", usuarios_del_grupo)
    
    return render(request, 'grupos/permisos.html', {
        'matriz_permisos': matriz, 
        'grupo': grupo,
        'page_obj': page_obj,  # Pasamos el objeto de página para los controles
        'usuarios': usuarios_del_grupo
    })
    
@require_POST
def actualizar_permiso_ajax(request):
    print("REQuEST")
    grupo_id = request.POST.get('grupo_id')
    permiso_id = request.POST.get('permiso_id')
    action = request.POST.get('action') # 'add' o 'remove'
    
    grupo = get_object_or_404(Group, id=grupo_id)
    permiso = get_object_or_404(Permission, id=permiso_id)
    
    if action == 'add':
        grupo.permissions.add(permiso)
    else:
        grupo.permissions.remove(permiso)
        
    return JsonResponse({'status': 'success'})