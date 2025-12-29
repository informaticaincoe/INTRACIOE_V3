from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from decimal import Decimal

class CategoriaMenu(models.Model):
    """Define la categoría a la que pertenece un platillo o bebida (e.g., Entrada, Plato Fuerte)."""
    
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    color = models.CharField(
            max_length=7, 
            default='#007bff', # Color por defecto (ej: azul de Bootstrap)
            verbose_name="Color (Hexadecimal)"
        )
    class Meta:
        verbose_name = "Categoría del Menú"
        verbose_name_plural = "Categorías del Menú"

    def __str__(self):
        return self.nombre

class Mesero(models.Model):
    """Perfil que liga un usuario del sistema al rol de mesero."""
    # Se usa OneToOneField para asegurar que cada usuario sea un Mesero único.
    nombre = models.CharField(max_length=120, null=False, verbose_name="Nombre mesero")
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="codigo de identificaciòn") 
    activo = models.BooleanField(default=True, verbose_name="Mesero Activo")

    class Meta:
        verbose_name = "Mesero"
        verbose_name_plural = "Meseros"
    
    def __str__(self):
        return self.codigo 

class Area(models.Model):
    """Areas del restaurante donde se encuntran las mesas"""
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Número de Mesa")

    class Meta:
        verbose_name = "Area"
        verbose_name_plural = "Areas"
        
    def __str__(self):
        return f"Area: {self.nombre}"
    
class Mesa(models.Model):
    """Representa las mesas físicas o áreas de servicio del restaurante."""
    ESTADO_MESA_CHOICES = [
        ('LIBRE', 'Libre'),
        ('OCUPADA', 'Ocupada'),
        ('PENDIENTE_PAGO', 'Pendiente de Pago'),
        
    ]
    numero = models.CharField(max_length=10, unique=True, verbose_name="Número de Mesa")
    capacidad = models.PositiveSmallIntegerField(default=4, verbose_name="Capacidad de personas")
    area = models.ForeignKey("RESTAURANTE.Area",on_delete=models.SET_NULL,null=True, blank=True,related_name="mesas",
    )
    es_vip = models.BooleanField(default=False, verbose_name="Mesa VIP (Prioridad)")
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_MESA_CHOICES,
        default='LIBRE',
        verbose_name="Estado Actual"
    )
    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        
    def __str__(self):
        return f"Mesa {self.numero} ({self.area})"

class AsignacionMesa(models.Model):
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name="asignaciones")
    mesero = models.ForeignKey(Mesero, on_delete=models.CASCADE, related_name="asignaciones")
    es_fija = models.BooleanField(default=False)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Asignacion de mesa"
        verbose_name_plural = "Asignaciones de mesas"
        
        constraints = [
            models.UniqueConstraint(
                fields=["mesa"],
                condition=Q(activa=True),
                name="uniq_mesa_asignacion_activa"
            )
        ]

class Platillo(models.Model):
    """Representa los ítems vendibles del menú."""
    categoria = models.ForeignKey(CategoriaMenu, on_delete=models.PROTECT, related_name='platillos')
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Platillo")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción o Ingredientes")
    imagen = models.ImageField(upload_to='Menu/', null=True, blank=True)
    precio_venta = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'), 
        verbose_name="Precio de Venta"
    )
    disponible = models.BooleanField(default=True, verbose_name="Disponible para Venta")
    # Indicador para Cocina (si requiere preparación activa vs. es un producto embotellado)
    es_preparado = models.BooleanField(default=True, verbose_name="Requiere Cocina/Preparación")

    class Meta:
        verbose_name = "Platillo / Ítem del Menú"
        verbose_name_plural = "Platillos / Ítems del Menú"

    def __str__(self):
        return self.nombre
    
