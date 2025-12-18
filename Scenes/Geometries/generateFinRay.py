import gmsh
import numpy as np
from Constants import * # --- Inicialización ---
gmsh.initialize()
launchGUI = gmsh.fltk.run 
factory = gmsh.model.occ

# --- Funciones Auxiliares ---
def addLines(PointTags, Close=True):
    N = len(PointTags)
    EndIdx = N if Close else N - 1
    LineTags = [] 
    for i in range(EndIdx):
        LineTags.append(factory.addLine(PointTags[i], PointTags[(i+1)%N]))
    return LineTags

# --- 1. Definición de Geometría 2D (Puntos) ---

# Cálculos auxiliares
InnerGripperHeight = (GripperWidth - WallThickness) / np.cos(Theta)
Phi = np.arctan2(GripperWidth - WallThickness, InnerGripperHeight)

# Puntos de la Pared (Gripper)
P0 = factory.addPoint(GripperWidth - WallThickness, 0, 0)
P1 = factory.addPoint(GripperWidth, 0, 0)
P2 = factory.addPoint(WallThickness, GripperHeight + GripperHeightGift, 0)
P3 = factory.addPoint(0, GripperHeight + GripperHeightGift, 0)
P4 = factory.addPoint(0, InnerGripperHeight, 0)

PointTags = [P0, P1, P2, P3, P4]
PointTags_exterior = PointTags.copy()

# Puntos del Soporte (Base)
soporte1 = factory.addPoint(GripperWidth, -10, 0)
soporte2 = factory.addPoint(GripperWidth - 6, -10, 0)
soporte3 = factory.addPoint(GripperWidth - 6, -7, 0)
soporte4 = factory.addPoint(GripperWidth - 3, -7, 0)
soporte5 = factory.addPoint(GripperWidth - 3, -3, 0)
soporte6 = factory.addPoint(0, -3, 0)
soporte7 = factory.addPoint(0, 0, 0)

point_tag_soporte = [P1, soporte1, soporte2, soporte3, soporte4, soporte5, soporte6, soporte7, P0]

# Puntos de Barras Internas
BarPositions = np.linspace(0, InnerGripperHeight, NBars + 2)

for BarPosition in BarPositions[1:-1]:
    StepWidth = 0.1  
    BarTotalLength = np.tan(Phi) * BarPosition
    
    # Coordenadas relativas
    y_top = InnerGripperHeight - (BarPosition - BarHeightThin / 2)
    y_bot = InnerGripperHeight - (BarPosition + BarHeightThin / 2)
    y_thick_top = InnerGripperHeight - (BarPosition - BarHeightThick / 2)
    y_thick_bot = InnerGripperHeight - (BarPosition + BarHeightThick / 2)
    
    BarTopLength = np.tan(Phi) * (BarPosition - BarHeightThin / 2)
    BarBottomLength = np.tan(Phi) * (BarPosition + BarHeightThin / 2)

    if BarTotalLength < BarThinLength:
        # Barra simple
        pts = [
            factory.addPoint(BarTopLength, y_top, 0),
            factory.addPoint(0, y_top, 0),
            factory.addPoint(0, y_bot, 0),
            factory.addPoint(BarBottomLength, y_bot, 0)
        ]
        PointTags.extend(pts)
    
    else:
        # Barra compleja (gruesa)
        pts = [
            factory.addPoint(BarTopLength, y_top, 0),
            factory.addPoint(BarTopLength - BarThinLength, y_top, 0),
            factory.addPoint(BarTopLength - BarThinLength - StepWidth, y_thick_top, 0),
            factory.addPoint(0, y_thick_top, 0),
            factory.addPoint(0, y_thick_bot, 0),
            factory.addPoint(BarBottomLength - BarThinLength - StepWidth, y_thick_bot, 0),
            factory.addPoint(BarBottomLength - BarThinLength, y_bot, 0),
            factory.addPoint(BarBottomLength, y_bot, 0)
        ]
        PointTags.extend(pts)

factory.synchronize()

# --- 2. Creación de Superficies ---

# Líneas y Wires
WireTag = factory.addWire(addLines(PointTags))
WireTag_soporte = factory.addWire(addLines(point_tag_soporte))
WireTag_exterior = factory.addWire(addLines(PointTags_exterior))

# Superficies planas
SurfaceDimTag = (2, factory.addPlaneSurface([WireTag]))
SurfaceDimTag_soporte = (2, factory.addPlaneSurface([WireTag_soporte]))
SurfaceDimTag_exterior = (2, factory.addPlaneSurface([WireTag_exterior]))

# --- 3. Extrusión a 3D ---

ExtrudeOut = factory.extrude([SurfaceDimTag], 0, 0, Depth)
ExtrudeOut_soporte = factory.extrude([SurfaceDimTag_soporte], 0, 0, Depth + borde)
ExtrudeOut_exterior = factory.extrude([SurfaceDimTag_exterior], 0, 0, Depth + borde)

HalfDimTag = ExtrudeOut[1]
HalfDimTag_soporte = ExtrudeOut_soporte[1]
HalfDimTag_exterior = ExtrudeOut_exterior[1]

# --- 4. Operaciones de Simetría y Fusión (Mitad) ---

# Copiar y simetrizar (Eje X)
CopyDimTags = factory.copy([HalfDimTag])
CopyDimTags_soporte = factory.copy([HalfDimTag_soporte])
CopyDimTags_exterior = factory.copy([HalfDimTag_exterior])

factory.synchronize()
factory.symmetrize(CopyDimTags, 1, 0, 0, 0)
factory.symmetrize(CopyDimTags_soporte, 1, 0, 0, 0)
factory.symmetrize(CopyDimTags_exterior, 1, 0, 0, 0)

# Fusión de mitades
garra_final = factory.fuse(CopyDimTags, [HalfDimTag])[0]
soporte_final = factory.fuse(CopyDimTags_soporte, [HalfDimTag_soporte])[0]
exterior_final = factory.fuse(CopyDimTags_exterior, [HalfDimTag_exterior])[0]

# Fusión total de componentes
garra_soporte_final = factory.fuse(garra_final, soporte_final)[0]
total_final = factory.fuse(garra_soporte_final, exterior_final)[0]

factory.synchronize()

# --- 5. Operaciones de Simetría (Garra Completa - Eje Z) ---

# Asegurar formato (dim, tag)
final_entity = total_final[0] if isinstance(total_final, list) else total_final

# Simetría final para grosor completo
CopyDimTags_finaltotal = factory.copy([final_entity])
factory.synchronize()
factory.symmetrize(CopyDimTags_finaltotal, 0, 0, -1, Depth + borde)

# Fusión final
fuse_full_gripper = factory.fuse([final_entity], CopyDimTags_finaltotal)
full_gripper = fuse_full_gripper[0]

factory.synchronize()

# ==============================================================================
#                        AGREGAR PARCHE MAGTEC (LATERAL)
# ==============================================================================

# 1. Calcular geometría y posición
x1, y1 = GripperWidth, 0
x2, y2 = WallThickness, GripperHeight + GripperHeightGift

dx = x2 - x1
dy = y2 - y1
wall_angle = np.arctan2(dy, dx) 

mid_x = (x1 + x2) / 2
mid_y = (y1 + y2) / 2
z_pos = (Depth + borde) - (PatchWidth / 2)

# 2. Crear el parche ORIGINAL
patch_tag = factory.addBox(-PatchLength/2, 0, z_pos, PatchLength, PatchHeight, PatchWidth)

# 3. Orientar y Posicionar el parche original
factory.rotate([(3, patch_tag)], 0, 0, 0, 0, 0, 1, wall_angle)
factory.translate([(3, patch_tag)], mid_x, mid_y, 0)

# ------------------------------------------------------------------
# TRUCO: Copiar el parche antes de fusionarlo.
# 'patch_iso' quedará suelto en el mundo para poder exportarlo solo.
# ------------------------------------------------------------------
patch_iso = factory.copy([(3, patch_tag)])

# 4. Fusionar el parche ORIGINAL con la GARRA COMPLETA
# (El patch_tag original se consume aquí y pasa a ser parte de result_mesh)
full_gripper_with_patch = factory.fuse(full_gripper, [(3, patch_tag)])
result_mesh = full_gripper_with_patch[0]

factory.synchronize()
print("Parche MagTec agregado y preparado para exportación independiente.")
# ==============================================================================

# --- 6. Generación de Malla y Exportación ---

output_file_stl = "Tesis/Scenes/Geometries/FinRay.stl"
output_file_patch = "Tesis/Scenes/Geometries/MagTecPatch.stl" # Nuevo archivo
output_file_vtk = "Tesis/Scenes/Geometries/FinRay.vtk"

# IMPORTANTE: Configuración para guardar solo lo que queremos
# Mesh.SaveAll = 0 hace que Gmsh solo guarde lo que está en un "Physical Group"
gmsh.option.setNumber("Mesh.SaveAll", 0) 

# --- A) Mallado de Superficie (STL) ---
print(f"Mallando superficie...")
gmsh.option.setNumber("Mesh.CharacteristicLengthFactor", densidad_malla_stl)  
factory.synchronize()
gmsh.model.mesh.generate(2) # Generamos malla 2D

# 1. EXPORTAR SOLO EL PARCHE (MagTecPatch.stl)
# Obtenemos las superficies del parche aislado (copia)
surfaces_patch = gmsh.model.getBoundary(patch_iso, combined=True, oriented=False)
tags_patch = [t[1] for t in surfaces_patch]
# Creamos un grupo físico temporal solo para el parche
pg_patch = gmsh.model.addPhysicalGroup(2, tags_patch)
print(f"Guardando {output_file_patch}...")
gmsh.write(output_file_patch)
# Borramos el grupo físico para no ensuciar el siguiente paso
gmsh.model.removePhysicalGroups([(2, pg_patch)])

# 2. EXPORTAR LA GARRA COMPLETA FUSIONADA (FinRay.stl)
# Obtenemos las superficies de la garra final (que ya incluye el parche fusionado)
surfaces_gripper = gmsh.model.getBoundary(result_mesh, combined=True, oriented=False)
tags_gripper = [t[1] for t in surfaces_gripper]
# Creamos un grupo físico temporal
pg_gripper = gmsh.model.addPhysicalGroup(2, tags_gripper)
print(f"Guardando {output_file_stl}...")
gmsh.write(output_file_stl)
gmsh.model.removePhysicalGroups([(2, pg_gripper)])


# --- B) Mallado de Volumen (VTK) ---
print(f"Mallando volumen (VTK)...")
gmsh.model.mesh.clear() # Limpiar malla 2D anterior
gmsh.option.setNumber("Mesh.CharacteristicLengthFactor", densidad_malla_vtk)  
factory.synchronize()
gmsh.model.mesh.generate(3) # Generar 3D

# 3. EXPORTAR VOLUMEN COMPLETO (FinRay.vtk)
# Creamos grupo físico del volumen final
pg_vol = gmsh.model.addPhysicalGroup(3, [result_mesh[0][1]])
print(f"Guardando {output_file_vtk}...")
gmsh.write(output_file_vtk)
gmsh.model.removePhysicalGroups([(3, pg_vol)])

# Finalización
factory.synchronize()
launchGUI()
exit()