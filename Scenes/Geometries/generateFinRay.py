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

## FUNCION DE CREAR PUNTOS ##
def crear_puntos(coordP2, coordP3, n_barras):
    x0, y0, z0 = coordP2
    print(x0, y0, z0)
    x1, y1, z1 = coordP3
    print(x1, y1, z1)
    ys = np.linspace(y0, y1, n_barras + 2)  
    xs = np.linspace(x0, x1, n_barras + 2)
    print(ys)
    print(xs)
    puntos = []
    #exit()
    for i in range(1, n_barras + 1): 
        puntos.append([xs[i], ys[i], z0])
    return puntos
## FUNCION DE CREAR PUNTOS ##

## FUNCION DE CREAR CILINDROS ##
def extruirCilindro(factory, punto, radio):
    x, y, z = punto
    return factory.addCylinder(x, y , z, 0, 0, Constants.Profundidad, radio)  
## FUNCION DE CREAR CILINDROS ##

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

HalfDimTag = ExtrudeOut[1]
CopyDimTags = factory.copy([HalfDimTag])
factory.symmetrize(CopyDimTags, 1, 0, 0, 0)
factory.fuse(CopyDimTags, [HalfDimTag])
print(f"ExtrudeOut:{ExtrudeOut}")
factory.synchronize()
## DUPLICAR FIGURA ## 

## CREAR GRILLA ## 
coordP2 = [Constants.AnchoPinza, 0, 0]
coordP3 = [Constants.EspesorPared, Constants.AlturaPinza+Constants.AlturaPinzaExtra,0]
puntos_grilla = crear_puntos(coordP2, coordP3, Constants.GrillaHorizontal)

cilindroTags = []
for punto in puntos_grilla:
    tag = extruirCilindro(factory, punto, Constants.radio)
    cilindroTags.append(tag)
## CREAR GRILLA ## 


# --- Definir los vértices del rectángulo de la pared --- #
p_sup_izq = [Constants.EspesorPared, 102, Constants.Profundidad]    # Superior izquierdo
p_sup_der = [Constants.AnchoPinza, 0, Constants.Profundidad]     # Superior derecho
p_inf_izq = [Constants.EspesorPared, 102, 0]     # Inferior izquierdo
p_inf_der = [Constants.AnchoPinza, 0, 0]      # Inferior derecho


# --- BARRAS HORIZONTALES (de lado a lado, siguiendo la inclinación) --- #
xs_izq = np.linspace(p_inf_izq[0], p_sup_izq[0], Constants.GrillaVertical + 2)
ys_izq = np.linspace(p_inf_izq[1], p_sup_izq[1], Constants.GrillaVertical + 2)
zs_izq = np.linspace(p_inf_izq[2], p_sup_izq[2], Constants.GrillaVertical + 2)

xs_der = np.linspace(p_inf_der[0], p_sup_der[0], Constants.GrillaVertical + 2)
ys_der = np.linspace(p_inf_der[1], p_sup_der[1], Constants.GrillaVertical + 2)
zs_der = np.linspace(p_inf_der[2], p_sup_der[2], Constants.GrillaVertical + 2)

for i in range(1, Constants.GrillaVertical + 1):
    p_ini = [xs_izq[i], ys_izq[i], zs_izq[i]]
    p_fin = [xs_der[i], ys_der[i], zs_der[i]]
    dx = p_fin[0] - p_ini[0]
    dy = p_fin[1] - p_ini[1]
    dz = p_fin[2] - p_ini[2]
    factory.addCylinder(p_ini[0], p_ini[1], p_ini[2], dx  , dy  , dz , Constants.radio)




## MOSTRAR ## 
#defineMeshSizes(2)
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