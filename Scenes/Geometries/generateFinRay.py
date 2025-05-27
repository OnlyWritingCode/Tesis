import gmsh
import numpy as np
import Constants
gmsh.initialize()

launchGUI = gmsh.fltk.run 
factory = gmsh.model.occ

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


def puntosEntreP2yP3(coordP2, coordP3, n_barras):
    x0, y0, z0 = coordP2
    x1, y1, z1 = coordP3
    ys = np.linspace(y0, y1, n_barras + 2)  
    xs = np.linspace(x0, x1, n_barras + 2)
    puntos = []
    for i in range(1, n_barras + 1): 
        puntos.append([xs[i], ys[i], z0])
    return puntos

def extruirBarra(factory, punto, ancho, espesor):
    x, y, z = punto
    return factory.addBox(x, y - espesor/2, z, ancho, espesor, Constants.Profundidad)  

        
        
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


coordP2 = [Constants.AnchoPinza, 0, 0]
coordP3 = [Constants.EspesorPared, Constants.AlturaPinza+Constants.AlturaPinzaExtra,0]

puntos_grilla = puntosEntreP2yP3(coordP2, coordP3, Constants.GrillaHorizontal)

for punto in puntos_grilla:
    extruirBarra(factory, punto, ancho=1, espesor=Constants.AnchoBarraGrilla)


LineTags = addLines(PointTags)
WireTag = factory.addWire(LineTags)
SurfaceDimTag = (2,factory.addPlaneSurface([WireTag]))
ExtrudeOut = factory.extrude([SurfaceDimTag], 0, 0, Constants.Profundidad)

#HalfDimTag = ExtrudeOut[1]
#CopyDimTags = factory.copy([HalfDimTag])
#factory.symmetrize(CopyDimTags, 1, 0, 0, 0)
#factory.fuse(CopyDimTags, [HalfDimTag])
#print(f"ExtrudeOut:{ExtrudeOut}")
factory.synchronize()

# defineMeshSizes(2)
gmsh.model.mesh.generate(3)
gmsh.write("FinRay.vtk")
gmsh.model.mesh.clear()
gmsh.model.mesh.generate(2)
gmsh.model.mesh.refine()
gmsh.model.mesh.refine()
gmsh.write("FinRay.stl")

factory.synchronize()

launchGUI()