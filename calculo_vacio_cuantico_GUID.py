import tkinter as tk
from tkinter import ttk
import numpy as np
import scipy.constants as const

# Funciones físicas
def energia_punto_cero(frecuencia):
    return 0.5 * const.h * frecuencia

def energia_vacio(L, N):
    c = const.c
    energia = 0
    for n in range(1, N + 1):
        f_n = n * c / (2 * L)
        energia += energia_punto_cero(f_n)
    return energia

def fuerza_casimir(area, distancia):
    return - (const.pi ** 2 * const.hbar * const.c) / (240 * distancia ** 4) * area

# Función para calcular y mostrar resultados
def calcular():
    try:
        frecuencia = float(entry_frecuencia.get())
        distancia = float(entry_distancia.get())
        area = float(entry_area.get())
        modos = int(entry_modos.get())

        zpe = energia_punto_cero(frecuencia)
        energia_vac = energia_vacio(distancia, modos)
        fuerza = fuerza_casimir(area, distancia)

        resultado.set(
            f"🔹 Energía del punto cero (ZPE): {zpe:.4e} J\n"
            f"🔹 Energía del vacío (modos={modos}): {energia_vac:.4e} J\n"
            f"🔹 Fuerza de Casimir: {fuerza:.4e} N"
        )
    except Exception as e:
        resultado.set(f"Error: {str(e)}")

# Interfaz gráfica con Tkinter
ventana = tk.Tk()
ventana.title("Simulación de la Nada Cuántica - Ing. Flores")
ventana.geometry("480x350")
ventana.resizable(False, False)

ttk.Label(ventana, text="Frecuencia (Hz):").pack()
entry_frecuencia = ttk.Entry(ventana)
entry_frecuencia.insert(0, "1e14")
entry_frecuencia.pack()

ttk.Label(ventana, text="Distancia entre placas (m):").pack()
entry_distancia = ttk.Entry(ventana)
entry_distancia.insert(0, "1e-7")
entry_distancia.pack()

ttk.Label(ventana, text="Área de placas (m²):").pack()
entry_area = ttk.Entry(ventana)
entry_area.insert(0, "1e-4")
entry_area.pack()

ttk.Label(ventana, text="Número de modos:").pack()
entry_modos = ttk.Entry(ventana)
entry_modos.insert(0, "1000")
entry_modos.pack()

ttk.Button(ventana, text="Calcular", command=calcular).pack(pady=10)

resultado = tk.StringVar()
etiqueta_resultado = ttk.Label(ventana, textvariable=resultado, wraplength=460, justify="left")
etiqueta_resultado.pack(pady=5)

ventana.mainloop()
