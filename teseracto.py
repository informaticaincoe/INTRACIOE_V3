import itertools
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# === 1. Generar vértices del teseracto (4D) ===
def generate_tesseract_vertices():
    return np.array(list(itertools.product([-1, 1], repeat=4)))

# === 2. Rotación en 4D (plano XY, XW, etc.) ===
def rotation_matrix_4d(angle, plane=(0, 3)):
    """
    Devuelve una matriz de rotación 4D en el plano especificado.
    - plane=(i, j): coordenadas que forman el plano de rotación
    """
    R = np.identity(4)
    i, j = plane
    R[i, i] = np.cos(angle)
    R[j, j] = np.cos(angle)
    R[i, j] = -np.sin(angle)
    R[j, i] = np.sin(angle)
    return R

# === 3. Proyección de 4D a 3D (perspectiva) ===
def project_4d_to_3d(vertices, w=2):
    projected = []
    for x, y, z, w_coord in vertices:
        factor = w / (w + w_coord)
        projected.append([x * factor, y * factor, z * factor])
    return np.array(projected)

# === 4. Dibujar teseracto proyectado ===
def plot_tesseract(angle=0.5):
    vertices4D = generate_tesseract_vertices()

    # Rotación en el plano XW
    R = rotation_matrix_4d(angle, plane=(0, 3))
    vertices4D_rot = vertices4D @ R.T

    # Proyección a 3D
    vertices3D = project_4d_to_3d(vertices4D_rot)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Dibujar vértices
    ax.scatter(vertices3D[:, 0], vertices3D[:, 1], vertices3D[:, 2], c="red", s=50)

    # Dibujar aristas
    for i, v1 in enumerate(vertices4D):
        for j, v2 in enumerate(vertices4D):
            if np.sum(v1 != v2) == 1:  # difieren en 1 coordenada → arista
                ax.plot([vertices3D[i, 0], vertices3D[j, 0]],
                        [vertices3D[i, 1], vertices3D[j, 1]],
                        [vertices3D[i, 2], vertices3D[j, 2]], c="blue", alpha=0.6)

    ax.set_title("Teseracto (proyección 4D → 3D)", fontsize=14)
    plt.show()

if __name__ == "__main__":
    plot_tesseract(angle=1.0)
