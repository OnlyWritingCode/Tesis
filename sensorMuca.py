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
im = plt.imshow(np.empty((ImgRows,ImgCols)),cmap='gray', vmin=15, vmax=60, animated=True, aspect="auto")
plt.axis([-0.5, ImgCols-0.5, -0.5, ImgRows-0.5])
Back = np.zeros((MucaRows,MucaCols))
Matrix = np.zeros((MucaRows,MucaCols))
Iteration = 0
WaitFrames = 20
Mask = np.loadtxt(ThisPath+"Mask.txt")

def getWeightedAverage(IdxList, Matrix):
    WeightList = []

    for IdxPair in IdxList:
        # print("check",IdxPair)
        # print("Check matrix", Matrix)
        Weight = Matrix[IdxPair[0], IdxPair[1]]
        if Weight < 0:
            Weight = 0
        WeightList.append(Weight)

    WeightList = np.array(WeightList)/np.sum(WeightList)
    # np.savetxt("Code/Python/WeightList.txt", WeightList)
    # np.savetxt("Code/Python/IdxList.txt", IdxList, fmt='%i')

    # print(f"WeightList:{WeightList}")
    
    WeightedAverageCoords = np.array([0,0], dtype=float)
    
    for (IdxPair, Weight) in zip(IdxList,WeightList):
        WeightedAverageCoords += Weight*np.array(IdxPair)
    
    TactileBits = [0,0,0]
    # Cavity 1
    if WeightedAverageCoords[0]>8.3 and WeightedAverageCoords[1] <= 4:
        TactileBits[0] = 1
    # Cavity 2
    if WeightedAverageCoords[0]<8.6 and WeightedAverageCoords[0] + WeightedAverageCoords[1] <= 10 and WeightedAverageCoords[0]>=5:
        TactileBits[1] = 1
    # Cavity 3
    if WeightedAverageCoords[0]<3 and WeightedAverageCoords[1]>=7:
        TactileBits[2] = 1
    
    np.savetxt("TactileBits.txt", TactileBits)
    
    
    return WeightedAverageCoords

    

def getNeighborIdxs(IdxX, IdxY, TouchResolution=(ImgCols,ImgRows)): 
    
    IdxList = []
    for i in range(IdxX-1, IdxX+2):
        for j in range(IdxY-1, IdxY+2):
            if not i<0 and not j<0 and not i>TouchResolution[0]-1 and not j>TouchResolution[1]-1:
                IdxList.append([i,j])
    return IdxList

def getTouchCoords(Matrix):
    TouchResolution = (ImgCols,ImgRows)
    LinearIdxMax = np.argmax(Matrix)
    # print(f'LinearIdxMaX: {LinearIdxMax}')
  
    IdxMaxX = (LinearIdxMax)//TouchResolution[1] 
    IdxMaxY = (LinearIdxMax)%TouchResolution[1] 
    
    Value = Matrix[IdxMaxX,IdxMaxY]
    return IdxMaxX, IdxMaxY, Value
    # return Value

def updatefig(*args):
    global Back, First, Iteration
    Line = SerialObj.readline()    
    # print("Line", Line)    
    try:
        Decoded = Line.decode()

        SplitStr = Decoded.split(',')
        Floats = np.array([float(i) for i in SplitStr])
        #Pressures = Floats[:4]
        #np.savetxt(PressureDataPath,Pressures)
        
        if (len(Floats)>16):
            FloatsMuCa = Floats
            Matrix = np.reshape(FloatsMuCa,(MucaRows,MucaCols)) - Back        
            
            if Iteration == WaitFrames:
                Back = Matrix            
            
            Matrix = Matrix.transpose()
            print(Matrix)        
            
            np.savetxt(MuCaDataPath,Matrix)
            # Matrix[:5,:5] = 
            # CutMatrix = Matrix[:ImgRows,:ImgCols] * Mask.transpose()
            CutMatrix = np.fliplr(np.flipud(Matrix[:ImgRows,:ImgCols].transpose()))
            # CutMatrix = Matrix[:ImgRows,:ImgCols]

            # print(CutMatrix.shape)
            # print(Mask.shape)
            # print("Cutmatrix: ",CutMatrix)
            
            IdxMaxX, IdxMaxY, Value = getTouchCoords(CutMatrix.reshape(ImgRows,ImgCols))

            NeighborIdxList = getNeighborIdxs(IdxMaxX, IdxMaxY)

            # print(IdxMaxX, IdxMaxY, Value)
            # print("NeighborIdxList",NeighborIdxList)
            TouchThreshold = 30
            if Value>TouchThreshold:
                WeightedAverageCoords = getWeightedAverage(NeighborIdxList, CutMatrix)
            else:
                WeightedAverageCoords = [-1,-1]

            np.savetxt(ThisPath+"Coord.txt", WeightedAverageCoords)
            # print("Wheigth  ",WeightedAverageCoords)
            im.set_array(CutMatrix)        
        
        
    except Exception as ex:    
        print(ex)
        pass
    Iteration += 1
    return im,


ani = animation.FuncAnimation(fig, updatefig, interval=1, blit=True)

plt.show()
