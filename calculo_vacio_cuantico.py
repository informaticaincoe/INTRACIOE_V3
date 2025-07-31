import numpy as np
import scipy.constants as const

# 1. Energía del punto cero (ZPE) de un modo cuántico
def energia_punto_cero(frecuencia):
    return 0.5 * const.h * frecuencia

# 2. Energía del vacío entre dos placas paralelas (simplificación 1D)
def energia_vacio(L, N):
    # L = distancia entre placas en metros
    # N = número de modos considerados
    c = const.c
    h = const.h
    energia = 0
    for n in range(1, N + 1):
        f_n = n * c / (2 * L)
        energia += energia_punto_cero(f_n)
    return energia

# 3. Fuerza de Casimir entre dos placas (fórmula idealizada)
def fuerza_casimir(area, distancia):
    # A = área de las placas en m^2
    # d = distancia entre las placas en m
    return - (const.pi ** 2 * const.hbar * const.c) / (240 * distancia ** 4) * area

# Valores de entrada
frecuencia_ejemplo = 1e14  # Hz (frecuencia de oscilador cuántico)
distancia_placas = 1e-7    # metros (100 nm)
area_placas = 1e-4         # metros cuadrados (1 cm²)
modos = 1000               # número de modos para energía de vacío

# Cálculos
zpe = energia_punto_cero(frecuencia_ejemplo)
energia_vac = energia_vacio(distancia_placas, modos)
fuerza = fuerza_casimir(area_placas, distancia_placas)

# Resultados
print("=== Simulación de la Nada Cuántica ===")
print(f"Energía del punto cero (ZPE) para f={frecuencia_ejemplo:.2e} Hz: {zpe:.4e} J")
print(f"Energía del vacío entre placas (N={modos} modos): {energia_vac:.4e} J")
print(f"Fuerza de Casimir para d={distancia_placas:.1e} m y A={area_placas:.1e} m²: {fuerza:.4e} N")



################################################################################################

# Este código simula la energía del vacío cuántico y la fuerza de Casimir entre dos placas paralelas.
# Utiliza la energía del punto cero de un oscilador cuántico y la energía del vacío entre placas.
# La fuerza de Casimir se calcula usando una fórmula idealizada.
# Los resultados se imprimen en la consola.
# Se pueden ajustar los parámetros de entrada para explorar diferentes configuraciones.
# La simulación es una simplificación y no tiene en cuenta todos los efectos cuánticos complejos.
# Se recomienda usar este código como base para estudios más profundos en física cuántica y teoría de campos.
# La energía del vacío cuántico es un tema fascinante y complejo que sigue siendo objeto de investigación.
# La fuerza de Casimir es un fenómeno observable que ha sido confirmado experimentalmente.
# Este código es un ejemplo educativo y no debe usarse para aplicaciones prácticas sin una comprensión adecuada.
# La física cuántica es un campo en constante evolución y se recomienda mantenerse actualizado con la literatura científica.
# La simulación es una herramienta útil para visualizar conceptos cuánticos y entender la naturaleza del vacío.
# La energía del vacío cuántico tiene implicaciones en cosmología, física de partículas y teoría de cuerdas.
# La fuerza de Casimir tiene aplicaciones en nanotecnología y física de materiales.

# Lista vacía para almacenar los carros
carros = []

# Bucle while para ingresar carros
while True:
    print("\nIngrese los datos del carro")
    marca = input("Marca: ")
    modelo = input("Modelo: ")

    # Crear diccionario y agregarlo a la lista
    carro = {"marca": marca, "modelo": modelo}
    carros.append(carro)

    # Preguntar si desea agregar otro
    continuar = input("¿Desea agregar otro carro? (s/n): ")
    if continuar.lower() != 's':
        break

# Convertir la lista en una tupla
carros_tupla = tuple(carros)

# Mostrar los carros usando for
print("\nLista de carros registrados:")
for c in carros_tupla:
    print(f"Marca: {c['marca']}, Modelo: {c['modelo']}")

# Definir la clase Carro
class Carro:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    def anunciar(self):
        print(f"El carro {self.marca} modelo {self.modelo} está listo.")

# Crear objetos Carro y usar el método
print("\nCreando objetos de tipo Carro...")
for c in carros_tupla:
    carro_obj = Carro(c["marca"], c["modelo"])
    carro_obj.anunciar()