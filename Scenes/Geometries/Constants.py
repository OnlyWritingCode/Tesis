import numpy as np

# --- Dimensiones Generales ---
GripperHeight = 100     # Altura garra
GripperWidth = 30       # Ancho garra
Depth = 12              # Profundidad

# --- Ángulos ---
# Nota: Phi no se incluye porque el script principal lo recalcula localmente
Theta = np.arctan2(GripperHeight, GripperWidth)

# --- Geometría y Paredes ---
GripperHeightGift = 2
WallThickness = 2       # Espesor pared
borde = 1               # Separación en mm para el extrude exterior/soporte

# --- Barras Internas (Costillas) ---
BarHeightThick = 2
BarHeightThin = 1
BarThinLength = 3
NBars = 8

# --- MagTecPatch ---
PatchLength = 50
PatchWidth = 20
PatchHeight = -2

# --- Densidades de Malla ---
densidad_malla_stl = 0.1  # Malla fina para visualización (STL)
densidad_malla_vtk = 0.5  # Malla optimizada para física (VTK)