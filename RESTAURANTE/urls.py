from django.urls import path

from . import views

urlpatterns = [
    # categorias para el menu
    path('categorias', views.listar_categorias, name='categorias-menu'),
    path('categoria/nueva', views.crear_categoria, name='crear-categoria'),
    path('categoria/<int:pk>/editar/', views.editar_categoria, name='editar-categoria'),
    path('categoria/<int:pk>/eliminar/', views.eliminar_categoria, name='eliminar-categoria'), 
    
    # Menu
    path('menu', views.listar_menu, name='menu'),
    path('menu/nueva', views.crear_menu, name='crear-menu'),
    path('menu/<int:pk>/editar/', views.editar_menu, name='editar-menu'),
    path('menu/<int:pk>/eliminar/', views.eliminar_menu, name='eliminar-menu'), 
    
    # Meseros
    path('meseros', views.listar_meseros, name='meseros-lista'),
    path('mesero/nuevo', views.crear_mesero, name='crear-mesero'),
    path('mesero/<int:pk>/eliminar/', views.eliminar_mesero, name='eliminar-mesero'),
    path('mesero/<int:pk>/editar/', views.editar_mesero, name='editar-mesero'),
 
    # Area
    path('areas', views.listar_areas, name='areas'),
    path('area/nuevo', views.crear_area, name='crear-area'),
    path('area/<int:pk>/eliminar/', views.eliminar_area, name='eliminar-area'),
    path('area/<int:pk>/editar/', views.editar_area, name='editar-area'),
       
    # Mesas
    path('mesas', views.listar_mesas, name='mesas-lista'),  
    path('mesa/crear', views.crear_mesa, name='crear-mesa'),    
      
    
    #Asignacion mesas
    path('mesa/mesero/asignar', views.asignar_mesa_a_mesero, name='asignar-mesa-a-mesero'),    
    
    
]