## IMPORT E INICIO ##
import gmsh
import numpy as np
import Constants
gmsh.initialize()
launchGUI = gmsh.fltk.run 
factory = gmsh.model.occ
## IMPORT E INICIO ##

## FUNCION DE MALLADO ##
def defineMeshSizes(lc=0.5):   
    #-------------------
    # MeshSizes 
    #-------------------
    gmsh.model.mesh.field.add("Box", 6)
    gmsh.model.mesh.field.setNumber(6, "VIn", lc)
    gmsh.model.mesh.field.setNumber(6, "VOut", lc)
    gmsh.model.mesh.field.setNumber(6, "XMin", -100)
    gmsh.model.mesh.field.setNumber(6, "XMax", 100)
    gmsh.model.mesh.field.setNumber(6, "YMin", 0)
    gmsh.model.mesh.field.setNumber(6, "YMax", 100)
    gmsh.model.mesh.field.setNumber(6, "ZMin", -3*100)
    gmsh.model.mesh.field.setNumber(6, "ZMax", 100)    
    gmsh.model.mesh.field.setNumber(6, "Thickness", 0.3)
    gmsh.model.mesh.field.setAsBackgroundMesh(6)
    gmsh.option.setNumber("Mesh.CharacteristicLengthExtendFromBoundary", 0)
    gmsh.option.setNumber("Mesh.CharacteristicLengthFromPoints", 0)
    gmsh.option.setNumber("Mesh.CharacteristicLengthFromCurvature", 0)
## FUNCION DE MALLADO ##

## FUNCION DE AGREGADO DE LINEAS ##
def addLines(PointTags, Close=True):
    N = len(PointTags)
    EndIdx = N
    LineTags = [] 
    if Close is False:
        EndIdx = EndIdx-1
    for i in range(EndIdx):
        print(i)
        LineTags.append(factory.addLine(PointTags[i], PointTags[(i+1)%N]))  
    return LineTags
## FUNCION DE AGREGADO DE LINEAS ##

##          Creacion de cilindros y guardado de tags para corte       ##
cilindros_tags = []
def crear_grilla_cilindros_y_guardar(factory, lado_ini1, lado_fin1, lado_ini2, lado_fin2, n_barras,radio):
    xs1 = np.linspace(lado_ini1[0], lado_fin1[0], n_barras + 2)
    ys1 = np.linspace(lado_ini1[1], lado_fin1[1], n_barras + 2)
    zs1 = np.linspace(lado_ini1[2], lado_fin1[2], n_barras + 2)

    xs2 = np.linspace(lado_ini2[0], lado_fin2[0], n_barras + 2)
    ys2 = np.linspace(lado_ini2[1], lado_fin2[1], n_barras + 2)
    zs2 = np.linspace(lado_ini2[2], lado_fin2[2], n_barras + 2)

    tags = []
    for i in range(1, n_barras + 1):
        p1 = [xs1[i], ys1[i], zs1[i]]
        p2 = [xs2[i], ys2[i], zs2[i]]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dz = p2[2] - p1[2]
        # Guardar el tag del cilindro creado
        tag = factory.addCylinder(p1[0], p1[1], p1[2], dx, dy, dz, Constants.radio)
        tags.append((3, tag))  # (dim=3, tag)
    return tags
##          Creacion de cilindros y guardado de tags para corte       ##

## VALORES CREACION PINZA ##     
AlturaInternaPinza = (Constants.AnchoPinza-Constants.EspesorPared)/np.cos(Constants.Theta)
Phi = np.arctan2(Constants.AnchoPinza-Constants.EspesorPared,AlturaInternaPinza)
P0 = factory.addPoint(Constants.AnchoPinza-Constants.EspesorPared, 0, 0)
#Puntos 2 y 3 ##################################
P1 = factory.addPoint(Constants.AnchoPinza, 0, 0)
P2= factory.addPoint(Constants.EspesorPared, Constants.AlturaPinza+Constants.AlturaPinzaExtra,0)
#######################################

P3= factory.addPoint(0, Constants.AlturaPinza+Constants.AlturaPinzaExtra,0)
P4 = factory.addPoint(0, AlturaInternaPinza, 0)
PointTags = [P0,P1,P2,P3,P4]
BarPositions = np.linspace(0, AlturaInternaPinza, Constants.NBars+2)
## VALORES CREACION PINZA ## 

## CREAR BARRAS INTERNAS ## 
for BarPosition in BarPositions[1:-1]:
    print(f"BarPosition:{BarPosition}")
    StepWidth = 0.1
    BarTotalLength = np.tan(Phi)*BarPosition
    BarTopLength = np.tan(Phi)*(BarPosition-Constants.AlturaBarraDelgada/2)
    BarBottomLength = np.tan(Phi)*(BarPosition+Constants.AlturaBarraDelgada/2)
    
    if BarTotalLength < Constants.LargoBarraDelgada:
        P0Bar = factory.addPoint(BarTopLength,AlturaInternaPinza-(BarPosition-Constants.AlturaBarraDelgada/2),0)
        P1Bar = factory.addPoint(0,AlturaInternaPinza-(BarPosition-Constants.AlturaBarraDelgada/2),0)
        P2Bar = factory.addPoint(0,AlturaInternaPinza-(BarPosition+Constants.AlturaBarraDelgada/2),0)
        P3Bar = factory.addPoint(BarBottomLength,AlturaInternaPinza-(BarPosition+Constants.AlturaBarraDelgada/2),0)
    
        PointTags += [P0Bar, P1Bar, P2Bar,P3Bar]
    
    if BarTotalLength > Constants.LargoBarraDelgada:
        P0Bar = factory.addPoint(BarTopLength,AlturaInternaPinza-(BarPosition-Constants.AlturaBarraDelgada/2),0)
        P1Bar = factory.addPoint(BarTopLength-Constants.LargoBarraDelgada,AlturaInternaPinza-(BarPosition-Constants.AlturaBarraDelgada/2),0)
        P2Bar = factory.addPoint(BarTopLength-Constants.LargoBarraDelgada-StepWidth,AlturaInternaPinza-(BarPosition-Constants.AlturaBarraGruesa/2),0)        
        P3Bar = factory.addPoint(0,AlturaInternaPinza-(BarPosition-Constants.AlturaBarraGruesa/2),0)
        P4Bar = factory.addPoint(0,AlturaInternaPinza-(BarPosition+Constants.AlturaBarraGruesa/2),0)        
        P5Bar = factory.addPoint(BarBottomLength-Constants.LargoBarraDelgada-StepWidth,AlturaInternaPinza-(BarPosition+Constants.AlturaBarraGruesa/2),0)        
        P6Bar = factory.addPoint(BarBottomLength-Constants.LargoBarraDelgada,AlturaInternaPinza-(BarPosition+Constants.AlturaBarraDelgada/2),0)  
        P7Bar = factory.addPoint(BarBottomLength,AlturaInternaPinza-(BarPosition+Constants.AlturaBarraDelgada/2),0)
        
        PointTags += [P0Bar, P1Bar, P2Bar, P3Bar, P4Bar,P5Bar,P6Bar,P7Bar]
## CREAR BARRAS INTERNAS ## 

## DUPLICAR FIGURA ## 
LineTags = addLines(PointTags)
WireTag = factory.addWire(LineTags)
SurfaceDimTag = (2,factory.addPlaneSurface([WireTag]))
ExtrudeOut = factory.extrude([SurfaceDimTag], 0, 0, Constants.Profundidad)
volumen_pared = ExtrudeOut[1]  # (dim, tag)

HalfDimTag = ExtrudeOut[1]
CopyDimTags = factory.copy([HalfDimTag])
factory.symmetrize(CopyDimTags, 1, 0, 0, 0)
factory.fuse(CopyDimTags, [HalfDimTag])
print(f"ExtrudeOut:{ExtrudeOut}")
factory.synchronize()
## DUPLICAR FIGURA ## 


##                  CREAR GRILLAS               ##

# --- VÉRTICES DE LA PARED (ya PARAMETRIZADOS) --- #
p_sup_izq = [Constants.EspesorPared, 102, Constants.Profundidad]       # Superior izquierdo
p_sup_der = [Constants.AnchoPinza, 0, Constants.Profundidad]           # Superior derecho
p_inf_izq = [Constants.EspesorPared, 102, 0]                           # Inferior izquierdo
p_inf_der = [Constants.AnchoPinza, 0, 0]                               # Inferior derecho

# --- Grilla vertical --- #
cilindros_tags += crear_grilla_cilindros_y_guardar(factory,p_inf_izq, p_sup_izq,p_inf_der, p_sup_der,Constants.GrillaVertical,Constants.radio)
# --- Grilla horizontal --- #
cilindros_tags += crear_grilla_cilindros_y_guardar(factory,p_inf_izq, p_inf_der,p_sup_izq, p_sup_der,Constants.GrillaHorizontal,Constants.radio)
factory.synchronize()

# --- 4. REALIZAR EL CORTE (boolear: pared - cilindros) --- #
pared_con_canaletas = factory.cut([volumen_pared], cilindros_tags, removeObject=True, removeTool=True)
factory.synchronize()
##                  CREAR GRILLAS               ##

## MOSTRAR ## 
defineMeshSizes(2)
gmsh.model.mesh.generate(3)
gmsh.write("FinRay.vtk")
gmsh.model.mesh.clear()
gmsh.model.mesh.generate(2)
gmsh.model.mesh.refine()
gmsh.model.mesh.refine()
gmsh.write("FinRay.stl")
factory.synchronize()
launchGUI()
## MOSTRAR ## 