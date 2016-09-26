## type a number in for the distance between offsets
## in the dialog box that pops up


import pymel.all as pm

dist = input()
oSel = pm.ls(selection=True)
objs = oSel[:]  ## copy oSel list

for i, obj in enumerate(objs):
    
    vecList = [
        [1,0,0], [0,1,0], [0,0,1],
        [-1,0,0], [0,-1,0], [0,0,-1],
    ]
    
    hiObj = pm.PyNode( obj.name() + "_hi" )
    xMovement = 3 + i*dist
    pair = [obj,hiObj]
    for item in pair:
        #pm.move(item, [0,0,0] , absolute=True, worldSpace=True )
        vec = vecList[i%len(vecList)]
        multVec = [ vec[0]*dist, vec[1]*dist, vec[2]*dist]
        pm.move(
            item, multVec,
            relative=True, worldSpace=True
        )
