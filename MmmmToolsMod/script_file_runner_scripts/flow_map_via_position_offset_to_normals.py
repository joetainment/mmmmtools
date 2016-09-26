
def lss():
    return pm.ls(selection=True)

oSel = lss()
objs = oSel[:]

pairs = [ [objs[0], objs[1]] ]


for pair in pairs:
    nRoot = pair[0]
    nTip = pair[1]
    sNRoot = nRoot.getShape()
    sNTip = nTip.getShape()
    
    indexes = sNRoot.getVertices()
    
    offsets = [ ]
    
    numVerts = sNRoot.numVertices()
    
    for i in range(numVerts):
    
        rootVertPos = sNRoot.vtx[i].getPosition(space='world')#.homogen()
        tipVertPos = sNTip.vtx[i].getPosition(space='world')#.homogen()
        #print( rootVertPos )
        #print( tipVertPos )
        #print(    help(  type( tipVertPos )  )    )
        
        offset = tipVertPos - rootVertPos
        #offset = offset.homogen()
        normal = offset.normal()
        #print( offset )
        
        offsets.append( offset )
        #v = Vector(offset.normalized() )
        #print offset
        #print( i )
        #Vector = pm.core.datatypes.Vector

        sNRoot.setVertexNormal( normal, i )
        

    #print(   help( type(sNTip)  )    )
    