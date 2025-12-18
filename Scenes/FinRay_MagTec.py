import Sofa

import os
path = os.path.dirname(os.path.abspath(__file__))+'/mesh/'

def createScene(rootNode):

                rootNode.addObject('RequiredPlugin', pluginName='SofaPython3 SoftRobots SoftRobots.Inverse ' + 'Sofa.Component Sofa.GL.Component ' + 'Sofa.GUI.Component Sofa.GUI.Qt')
                rootNode.addObject('InteractiveCamera',name='camera', position=[0,50,-200],lookAt=([0, 50, 0]))
                rootNode.findData('dt').value = 0.01
                rootNode.findData('gravity').value = [0, -9810, 0]
                rootNode.addObject('LightManager')
                rootNode.addObject(
                    "PositionalLight",
                    name="light1",
                    color="0.8 0.8 0.8",
                    # position=[0, Const.Thickness, 3],
                    position=[0, 50, -200 ],

                )
                rootNode.addObject(
                    "PositionalLight",
                    name="light2",
                    color="0.8 0.8 0.8",
                    position=[50, 50, 0],
                )
                rootNode.addObject('VisualStyle', displayFlags='showVisualModels showCollisionModels hideBoundingCollisionModels showForceFields showInteractionForceFields hideWireframe')
                rootNode.addObject('FreeMotionAnimationLoop')
                rootNode.addObject('GenericConstraintSolver', maxIterations=100, tolerance = 0.0000001)

		#model
                model = rootNode.addChild('model')
                model.addObject('EulerImplicitSolver', name='odesolver')
                model.addObject('MeshVTKLoader', name='loader', filename='Geometries/FinRay.vtk')
                model.addObject('TetrahedronSetTopologyContainer', src='@loader', name='container')
                model.addObject('TetrahedronSetTopologyModifier')
                model.addObject('MechanicalObject', name='tetras', template='Vec3', showIndices=False)
                model.addObject('UniformMass', totalMass=0.5)
                # model.addObject('TetrahedronFEMForceField', template='Vec3', name='FEM', method='large', poissonRatio=0.3,  youngModulus=40*1000)
                
                model.addObject('BoxROI', name='boxROI', box=[-50, -5, -30,  50, 2, 30], drawBoxes=True, position="@tetras.rest_position", tetrahedra="@container.tetrahedra")
                model.addObject('RestShapeSpringsForceField', points='@boxROI.indices', stiffness=1e12)
                model.addObject('SparseLDLSolver', name='preconditioner')
                model.addObject('LinearSolverConstraintCorrection', linearSolver='@preconditioner')

                ##########################################
                # Visualization                          #
                ##########################################

                modelVisu = model.addChild('visu')
                modelVisu.addObject('MeshSTLLoader', filename="Geometries/FinRay.stl", name="loader", rotation=[0,0,0])
                modelVisu.addObject('OglModel', src="@loader", scale3d=[1, 1, 1])
                modelVisu.addObject('BarycentricMapping')


                # MagTecPatch STL
                # -----------------------------------------------------
                # VISUALIZACIÓN 2: El Parche (MagTecPatch)
                # -----------------------------------------------------
                
                # Cargamos el STL del parche
                model.addObject('MeshSTLLoader',name="ROILoader", filename="Geometries/MagTecPatch.stl")#,scale3d = [1.1,1.1,1.1])
                # model.addObject('OglModel', name="VisualModel", src="@ROILoader", scale3d=[1, 1, 1], color=[1.0, 0.0, 0.0, 0.5]) # Rojo sólido
                boxTip = model.addObject(
                    'MeshROI',
                    name="ROIm",
                    drawBox="0",
                    drawEdges="0",
                    drawTriangles="0",
                    drawTetrahedra="1",
                    drawOut="0",
                    drawPoints="1",
                    drawSize = "10",
                    computeMeshROI="1",  # Change to 1 to compute the ROI
                    doUpdate="0",
                    position="@loader.position",
                    tetrahedra="@container.tetrahedra",
                    # If you need to use ROILoader for selection:
                    ROIposition="@ROILoader.position", 
                    ROItriangles="@ROILoader.triangles"
                )
                boxTip.init()

                print("boxTip",boxTip.indices.value)
                

                model.addObject('IndexValueMapper', 
                    name="ind_Out", 
                    indices="@ROIm.tetrahedronOutIndices", 
                    value=20.0*2*5)
                model.addObject('IndexValueMapper', 
                    name="ind_Total", 
                    inputValues="@ind_Out.outputValues", 
                    indices="@ROIm.tetrahedraIndices", 
                    value=1.0)      #modificar YoungModulus de FEM , ya que solo toma valor 1 esto.
                print("ind_Out outputValues:", model.ind_Out.outputValues.value)
                print("ind_Out indices:", model.ind_Out.indices.value)
                print("ind_Total outputValues:", model.ind_Total.outputValues.value)
                print("ind_Total indices:", model.ind_Total.indices.value)
                print("Total tetrahedra in model:", len(model.container.tetrahedra.value))

                model.addObject('TetrahedronFEMForceField', 
                    template='Vec3', 
                    name='FEM', 
                    method='large', 
                    poissonRatio=0.3, 
                    youngModulus=1.0*1000,  
                    localStiffnessFactor="@ind_Total.outputValues" 
                )
                return rootNode
