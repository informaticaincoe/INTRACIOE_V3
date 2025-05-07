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
