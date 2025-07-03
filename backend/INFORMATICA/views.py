import os
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db import connections
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
#from weasyprint import HTML

@login_required
def listar_bases_datos(request):
    # Obtener los nombres de todas las bases de datos
    with connections['brilo_sqlserver'].cursor() as cursor:
        cursor.execute("SELECT name FROM sys.databases;")
        bases_datos = cursor.fetchall()
    
    # Configurar paginación (por ejemplo, 10 bases de datos por página)
    paginator = Paginator(bases_datos, 10)  # Cambia el número si deseas más o menos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Renderizar el template con la paginación
    return render(request, 'listar_bases_datos.html', {'page_obj': page_obj})

@login_required
def ver_estructura_base_datos(request, nombre_db):
    with connections['brilo_sqlserver'].cursor() as cursor:
        # Cambiar el contexto de la conexión a la base de datos deseada
        cursor.execute(f"SELECT TABLE_NAME FROM [{nombre_db}].INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';")
        tablas = cursor.fetchall()
    
    # Pasar las tablas al template
    return render(request, 'ver_estructura_base_datos.html', {'nombre_db': nombre_db, 'tablas': tablas})

@login_required
def buscar_tablas(request, nombre_db):
    termino = request.GET.get('q', '')  # Obtiene el término de búsqueda desde la solicitud AJAX
    with connections['brilo_sqlserver'].cursor() as cursor:
        # Ejecuta una consulta para buscar tablas que contengan el término
        cursor.execute(f"""
            SELECT TABLE_NAME 
            FROM [{nombre_db}].INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE' 
            AND TABLE_NAME LIKE %s
        """, [f'%{termino}%'])
        tablas = cursor.fetchall()
    
    # Prepara los nombres de las tablas para el response
    resultados = [{'nombre': tabla[0]} for tabla in tablas]
    
    return JsonResponse(resultados, safe=False)  # Retorna los resultados como JSON

@login_required
def ver_contenido_tabla(request, nombre_db, nombre_tabla):
    with connections['brilo_sqlserver'].cursor() as cursor:
        cursor.execute(f"""
            SELECT COLUMN_NAME 
            FROM [{nombre_db}].INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = '{nombre_tabla}';
        """)
        columnas = [col[0] for col in cursor.fetchall()]
        
        cursor.execute(f"SELECT * FROM [{nombre_db}].[dbo].[{nombre_tabla}];")
        datos = cursor.fetchall()

    # Configurar la paginación
    paginator = Paginator(datos, 25)  # Muestra 25 filas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ver_estructura_tabla.html', {
        'nombre_db': nombre_db,
        'nombre_tabla': nombre_tabla,
        'columnas': columnas,
        'page_obj': page_obj
    })
