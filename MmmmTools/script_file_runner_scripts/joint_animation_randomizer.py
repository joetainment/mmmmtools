import pymel.all as pm
import random

oSel = pm.ls(selection=True)
objs = oSel[:]  ## copies the list

globalIntensity = 0.3

timeStep = 4

startTime, endTime = 1, 100

initialPositions = { }


#randomSeed = 2
#randomJumpAhead = 0

#random.seed( randomSeed )
#random.jumpahead( randomJumpAhead)


for obj in objs:
    initialPositions[obj.name()] = obj.translate.get()
    

for obj in objs:
    
    initPos = initialPositions[obj.name()]
    
    pm.select( obj )
    for i in range( startTime, endTime+1 ):
        if i==startTime or i==endTime or i % timeStep==0:
            pm.currentTime( i )
            
            ix = initPos[0]
            iy = initPos[1]
            iz = initPos[2]
            
            rx = random.uniform( -1.0, 1.0 )
            ry = random.uniform( -1.0, 1.0 )
            rz = random.uniform( -1.0, 1.0 )
            
            mult = obj.movementIntensity.get() * globalIntensity
            
            
            if i != endTime:
                obj.translate.set(
                    [ 
                        ix + rx*mult,
                        iy + ry*mult,
                        iz + rz*mult,
                    ]
                )
                obj.translate.setKey()
            elif i==startTime:
                pm.currentTime( endTime )
                obj.translate.set(
                    [ 
                        ix + rx*mult,
                        iy + ry*mult,
                        iz + rz*mult,
                    ]
                )                        
                obj.translate.setKey()
            
            ##           	for conn in obj.translateX.listConnections():
            ##           	    print( conn )
            #            curve.setPostInfinityType('cycle', change=None)
        
            
pm.select( oSel )
            
            