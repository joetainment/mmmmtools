def getFaceCenter( roundNumbersForCenters=True, precision=1):

    faceCenter = []

    selection = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(selection)
    #print ("Number of objects in selection: %s " % selection.length())

    iter = OpenMaya.MItSelectionList (selection, OpenMaya.MFn.kMeshPolygonComponent)

    while not iter.isDone():
        #status = OpenMaya.MStatus
        dagPath = OpenMaya.MDagPath()
        component = OpenMaya.MObject()

        iter.getDagPath(dagPath, component)

        polyIter = OpenMaya.MItMeshPolygon(dagPath, component)

        while not polyIter.isDone():

            i = 0
            i = polyIter.index()

            center = OpenMaya.MPoint
            center = polyIter.center(OpenMaya.MSpace.kWorld)
            #print( "center is: " + str(center) )
            point = [0.0,0.0]
            if roundNumbersForCenters==True:
                point[0] = round( center.x, roundingDecimalPlaces )
                point[1] = round( center.y, roundingDecimalPlaces )
                point[2] = round( center.z, roundingDecimalPlaces )
            else:
                point[0] = center.x
                point[1] = center.y
                point[2] = center.z
            faceCenter = point
            
            polyIter.next()
            
        iter.next()
        
    return str(faceCenter)
    

#def getFaceCenters( faces=None ):
#    selection_at_func_begin = pm.ls(selection=True)
#    
#    if faces==None:
#        faces = pm.ls(selection=True, flatten=True )
#        
#    for face in faces:
#        pm.select( face )
#        centers.append( 
        