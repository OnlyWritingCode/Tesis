# import numpy as np
# import serial
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation

# import os

# ThisPath = os.path.dirname(os.path.abspath(__file__))+'/'
# ScenePath = os.path.dirname(os.path.abspath(__file__))+'/Scenes/'
# PressureDataPath = ScenePath + 'PressureData.txt'
# MuCaDataPath = ScenePath + 'MuCaData.txt'


# SerialObj = serial.Serial('/dev/ttyACM1',115200,timeout=0.1)


# print("Start")

# MucaCols = 12
# MucaRows = 21

# ImgRows = 6
# ImgCols = 6

# Counter = 0

# fig = plt.figure()
# fig.suptitle('Capacitive Sensor Data', fontsize=16)
# im = plt.imshow(np.empty((ImgRows,ImgCols)),cmap='gray', vmin=20, vmax=70, animated=True)
# plt.axis([-0.5, ImgCols-0.5, -0.5, ImgRows-0.5])
# Back = np.zeros((MucaRows,MucaCols))
# Matrix = np.zeros((MucaRows,MucaCols))
# Iteration = 0
# WaitFrames = 20
# Mask = np.loadtxt(ThisPath+"Mask.txt")
# Mask = np.ones((ImgCols, ImgRows))
# def getWeightedAverage(IdxList, Matrix):
#     WeightList = []
    
#     for IdxPair in IdxList:
#         Weight = Matrix[IdxPair[0], IdxPair[1]]
#         if Weight < 0:
#             Weight = 0
#         WeightList.append(Weight)
    
#     WeightList = np.array(WeightList)/np.sum(WeightList)
    
#     print(WeightList)
    
#     WeightedAverageCoords = np.array([0,0], dtype=float)
    
#     for (IdxPair, Weight) in zip(IdxList,WeightList):
#         WeightedAverageCoords += Weight*np.array(IdxPair)
    
#     TactileBits = [0,0,0]
#     # Cavity 1
#     if WeightedAverageCoords[0]>8.3 and WeightedAverageCoords[1] <= 4:
#         TactileBits[0] = 1
#     # Cavity 2
#     if WeightedAverageCoords[0]<8.6 and WeightedAverageCoords[0] + WeightedAverageCoords[1] <= 10 and WeightedAverageCoords[0]>=5:
#         TactileBits[1] = 1
#     # Cavity 3
#     if WeightedAverageCoords[0]<3 and WeightedAverageCoords[1]>=7:
#         TactileBits[2] = 1
    
#     np.savetxt("TactileBits.txt", TactileBits)
    
    
#     return WeightedAverageCoords

    

# def getNeighborIdxs(IdxX, IdxY, TouchResolution=(ImgRows,ImgCols)): 
    
#     IdxList = []
#     for i in range(IdxX-1, IdxX+2):
#         for j in range(IdxY-1, IdxY+2):
#             if not i<0 and not j<0 and not i>TouchResolution[0]-1 and not j>TouchResolution[1]-1:
#                 IdxList.append([i,j])
#     return IdxList

# def getTouchCoords(Matrix):
#     TouchResolution = (ImgRows,ImgCols)
#     LinearIdxMax = np.argmax(Matrix)
#     print(f'LinearIdxMaX: {LinearIdxMax}')
  
#     IdxMaxX = (LinearIdxMax)//TouchResolution[1] 
#     IdxMaxY = (LinearIdxMax)%TouchResolution[1] 
    
#     Value = Matrix[IdxMaxX,IdxMaxY]
    
#     return IdxMaxX, IdxMaxY, Value
#     # return Value

# def updatefig(*args):
#     global Back, First, Iteration, Counter
#     Line = SerialObj.readline()    
#     #print(Line) 
#     try:
#         Decoded = Line.decode()

#         SplitStr = Decoded.split(',')
#         Floats = np.array([float(i) for i in SplitStr])
#         #Pressures = Floats[:4]
#         #np.savetxt(PressureDataPath,Pressures)
        
#         if (len(Floats)>4):
#             FloatsMuCa = Floats
#             Matrix = np.reshape(FloatsMuCa,(MucaRows,MucaCols)) - Back        
            
#             if Iteration == WaitFrames:
#                 Back = Matrix            
            
#             Matrix = Matrix.transpose()
#             # print(Matrix)        
            
#             np.savetxt(MuCaDataPath,Matrix)
#             # Matrix[:5,:5] = 
#             CutMatrix = Matrix[:ImgRows,:ImgCols] * Mask.transpose()
#             CutMatrix = np.flipud(CutMatrix.transpose())
#             # print(CutMatrix.shape)
#             # print(Mask.shape)
#             print(CutMatrix)
            
            
#             CutMatrixTC = CutMatrix.reshape(ImgRows,ImgCols)
#             CutMatrixWeights = np.copy(CutMatrixTC)
#             im.set_array(CutMatrix)        
#             NoMoreContacts = False
#             ContactCoordinates = []
#             MaxIdxs = []
#             while not NoMoreContacts:                
#                 IdxMaxX, IdxMaxY, Value = getTouchCoords(CutMatrixTC)
#                 NeighborIdxList = getNeighborIdxs(IdxMaxX, IdxMaxY)
#                 print(IdxMaxX, IdxMaxY, Value)
#                 print(NeighborIdxList)
#                 TouchThreshold = 20
#                 if Value>TouchThreshold:
#                     WeightedAverageCoords = getWeightedAverage(NeighborIdxList, CutMatrixWeights)
#                     ContactCoordinates.append(WeightedAverageCoords)
#                     for NeighborIdx in NeighborIdxList:
#                         CutMatrixTC[NeighborIdx] = 0
#                     CutMatrixWeights[IdxMaxX, IdxMaxY] = 0
#                 else:
#                     WeightedAverageCoords = [-1,-1]
#                     NoMoreContacts = True
                    

            
#             print(f"NContacst: {len(ContactCoordinates)}")
#             if len(ContactCoordinates) == 0 :    
#                 Actividad = [0]
#             else :
#                 Actividad = [1]
#             print("Actividad = ",Actividad)
#             np.savetxt("Actividad.txt",Actividad)
                
#             np.savetxt(ScenePath+"WeightedAverageCoords.txt", WeightedAverageCoords)
#             np.savetxt(ScenePath+"ContactCoordinates.txt", ContactCoordinates)
#             print(WeightedAverageCoords)
#             # np.savetxt(ScenePath+"Matrices/Matrix"+str(Counter)+".txt",CutMatrix)
#             Counter += 1
            
#     except Exception as ex:    
#         print(ex)
        
#     Iteration += 1
#     return im,


# ani = animation.FuncAnimation(fig, updatefig, interval=1, blit=True)

# plt.show()



import numpy as np
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

ThisPath = os.path.dirname(os.path.abspath(__file__))+'/'
ScenePath = os.path.dirname(os.path.abspath(__file__))+'/../../Scenes/'
PressureDataPath = ScenePath + 'PressureData.txt'
MuCaDataPath = ThisPath + 'MuCaData.txt'

SerialObj = serial.Serial('/dev/ttyACM1',115200,timeout=0.1)
print("Start")

MucaCols = 12
MucaRows = 21

ImgRows = 6
ImgCols = 6

fig = plt.figure()
fig.suptitle('Capacitive Sensor Data', fontsize=16)
im = plt.imshow(np.empty((ImgRows,ImgCols)), cmap='gray', vmin=15, vmax=60, animated=True, aspect="auto")
plt.axis([-0.5, ImgCols-0.5, -0.5, ImgRows-0.5])

Back = np.zeros((MucaRows,MucaCols))
Matrix = np.zeros((MucaRows,MucaCols))
Iteration = 0
WaitFrames = 20
Mask = np.loadtxt(ThisPath + "Mask.txt")

CoordBuffer = []    # Para mediana temporal
buffer_size = 5
dist_threshold = 0.5

def globalWeightedCoords(cut_mat, threshold=30.0):
    """
    Calcula el promedio ponderado global 
    de todos los puntos por encima de un umbral.
    """
    # Asegurar cut_mat es ImgRows x ImgCols
    coords = []
    weights = []
    for i in range(ImgRows):
        for j in range(ImgCols):
            val = cut_mat[i,j]
            if val > threshold:
                coords.append([i,j])
                weights.append(val)
    if len(coords) == 0:
        return [-1, -1]
    coords = np.array(coords)
    weights = np.array(weights)
    Wsum = np.sum(weights)
    if Wsum == 0:
        return [-1, -1]
    avg_x = np.sum(coords[:,0] * weights) / Wsum
    avg_y = np.sum(coords[:,1] * weights) / Wsum
    return [avg_x, avg_y]

def medianFilterAndDeadZone(newCoord):
    """
    Aplica mediana temporal y zona muerta.
    """
    global CoordBuffer, buffer_size, dist_threshold
    
    # Si no hay contacto
    if newCoord[0] < 0 or newCoord[1] < 0:
        # Mantenemos la mediana si existe
        if len(CoordBuffer) > 0:
            # no agregamos nada nuevo, solo mantenemos
            pass
        else:
            # si no hay nada en el buffer, tomamos -1, -1
            return newCoord
    else:
        # Agregamos al buffer
        CoordBuffer.append(newCoord)
        if len(CoordBuffer) > buffer_size:
            CoordBuffer.pop(0)
    
    if len(CoordBuffer) == 0:
        return [-1, -1]
    
    # Calcular mediana de lo que hay en CoordBuffer
    arr = np.array(CoordBuffer)
    med_x = np.median(arr[:,0])
    med_y = np.median(arr[:,1])
    medianCoord = np.array([med_x, med_y])
    
    # Zona muerta respecto al último valor en el buffer (o la mediana anterior)
    last = arr[-1]  # el último que ingresó
    d = np.linalg.norm(medianCoord - last)
    if d < dist_threshold:
        # Si la distancia es pequeña, usamos el último
        return last
    else:
        # Caso contrario, devolvemos la mediana actual
        return medianCoord

def updatefig(*args):
    global Back, Iteration
    Line = SerialObj.readline()    
    try:
        Decoded = Line.decode()
        SplitStr = Decoded.split(',')
        Floats = np.array([float(i) for i in SplitStr])
        
        if (len(Floats) > 16):
            FloatsMuCa = Floats
            Matrix = np.reshape(FloatsMuCa,(MucaRows,MucaCols)) - Back        
            
            if Iteration == WaitFrames:
                Back = Matrix
            
            Matrix = Matrix.transpose()
            np.savetxt(MuCaDataPath, Matrix)
            
            cut_mat = np.fliplr(np.flipud(Matrix[:ImgRows, :ImgCols].transpose()))
            # Calculamos la coordenada global ponderada
            WeightedCoord = globalWeightedCoords(cut_mat, threshold=30.0)
            
            # Filtro temporal + zona muerta
            finalCoord = medianFilterAndDeadZone(WeightedCoord)
            
            np.savetxt(ThisPath + "Coord.txt", finalCoord)
            im.set_array(cut_mat)

    except Exception as ex:
        print(ex)
        pass
    
    Iteration += 1
    return im,

ani = animation.FuncAnimation(fig, updatefig, interval=1, blit=True)
plt.show()
