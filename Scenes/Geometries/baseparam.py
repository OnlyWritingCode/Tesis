import gmsh
import cbase
import math

gmsh.initialize()
gmsh.model.add("LaRealRealBase") 

CajaBase = gmsh.model.occ.addBox(0, 0, 0, cbase.largo_base, cbase.ancho_base, cbase.altura_base)
CajaLateral = gmsh.model.occ.addBox(0, 0, 0, -cbase.largo_pared_lateral, cbase.ancho_base, cbase.altura_pared_lateral)
FuseOut = gmsh.model.occ.fuse([(3, CajaBase)], [(3, CajaLateral)])
FusedBaseTag = FuseOut[0][0][1]

# Crear la cavidad desde la parte superior hacia abajo
CavidadTag = gmsh.model.occ.addBox(1, 1, cbase.altura_base, cbase.largo_base - 2, cbase.ancho_base - 2, -3)

# Restar la cavidad de la base fusionada
CutOut = gmsh.model.occ.cut([(3, FusedBaseTag)], [(3, CavidadTag)])
CutBaseTag = CutOut[0][0][1]

CylinderTag2 = gmsh.model.occ.addCylinder(-14, 6, 0, 0, 0, cbase.altura_cilindro, cbase.radio_cilindro)

# Fusionar el cilindro con la base cortada
FuseOut2 = gmsh.model.occ.fuse([(3, CutBaseTag)], [(3, CylinderTag2)])
FinalBaseTag = FuseOut2[0][0][1]

Caja_cilindro = gmsh.model.occ.addBox(-14, 10, 30, 1, -4, 1)
FuseOut3 = gmsh.model.occ.fuse([(3, FinalBaseTag)], [(3, Caja_cilindro)])
fintag = FuseOut3[0][0][1]

Caja_soportecable = gmsh.model.occ.addBox(
    cbase.largo_base, 0, 0,
    cbase.largo_base_cable,
    cbase.ancho_base,
    cbase.altura_base + cbase.altura_base_cable
)
FuseOut4 = gmsh.model.occ.fuse([(3, fintag)], [(3, Caja_soportecable)])
newtag = FuseOut4[0][0][1]

############################ AQUI ME GUSTARIA AGREGAR LA FORMA DE DONUT ##############################################

# Definir los radios mayor y menor del toroide
r_major = cbase.ancho_base / 6       # Radio mayor
r_minor = cbase.largo_base_cable / 4  # Radio menor

# Crear el toroide en el origen
torus_tag = gmsh.model.occ.addTorus(0, 0, 0, r_major, r_minor)

# Rotar el toroide 90 grados alrededor del eje Y en el origen
gmsh.model.occ.rotate(
    [(3, torus_tag)],
    0, 0, 0,
    0, 1, 0,
    -math.pi / 2
)

# Trasladar el toroide a la posición deseada
torus_cx = cbase.largo_base + cbase.largo_base_cable / 2
torus_cy = cbase.ancho_base / 2
torus_cz = cbase.altura_base + cbase.altura_base_cable / 2 + 2  # Subimos el toroide 2 mm

gmsh.model.occ.translate(
    [(3, torus_tag)],
    torus_cx,
    torus_cy,
    torus_cz
)

# Sincronizar y visualizar antes de fusionar
gmsh.model.occ.synchronize()
gmsh.fltk.run()

# Usar fragment en lugar de fuse para evitar problemas de facetas superpuestas
FragmentOut = gmsh.model.occ.fragment([(3, newtag)], [(3, torus_tag)])
final_tag = FragmentOut[0][0][1]

# Eliminar entidades redundantes
gmsh.model.occ.removeAllDuplicates()

############################ FIN DE LA SECCIÓN DEL TOROIDE ###########################################################

# Sincronizar antes de generar la malla
gmsh.model.occ.synchronize()

# Generar la malla
gmsh.model.mesh.generate(3)

gmsh.write("BasePotencio.step")
# Visualizar el modelo final
gmsh.fltk.run()

# Finalizar Gmsh
gmsh.finalize()
