## This class is just started, and needs a lot of additional work!
## also, there is a mix of cmds and pymel.  In some cases it is required
## but should be cleaned up where possible
import pymel.all as pm
import maya.cmds as cmds
import traceback

class RendererVertexColorTools(object):
    def applyVertexColorAttributeToSelection(self=None):

        sel = pm.ls(selection=True)

        shapesToAdd = []

        for obj in sel:
            try:
                shape = obj.getShape()
                shapesToAdd.append( shape )
            except:
                pass

        print( shapesToAdd )
        print( sel )

        selWithShapes = sel + shapesToAdd
        print(selWithShapes)

        shapes = pm.ls(selWithShapes, shapes=True )

        print( shapes )

        for obj in shapes:
            try:
                obj.mmmmExportVertexColorsForMr.get()
                try:
                    obj.mmmmExportVertexColorsForMr.set(True)
                except:
                    pass
            except:
                obj.addAttr( 'mmmmExportVertexColorsForMr', attributeType=bool, defaultValue=True )
                
    def createOrRefreshVertexColorNodes(self=None):
        import pymel.all as pm
        import maya.cmds as cmds
        import traceback


        selectionToRestore = cmds.ls(selection=True)


        #### Get a list of all the old things to delete
        cmds.select( clear=True )
        try:
            cmds.select( "*__ExportForMesh__*" )    
        except:
            cmds.select( clear=True )
        try:
            exportsFound = cmds.ls( selection=True )
        except:
            exportsFound = [ ]


        ## Get the existing vertex colors pool or make a new one
        try:
            vertexColorsPool = pm.PyNode('vertexColorsPool')
        except:
            vertexColorsPool = pm.shadingNode( 'plusMinusAverage', asUtility=True )
            vertexColorsPool.rename( 'vertexColorsPool' )

        cmds.select( clear=True )

        ## Delete any exportsFound  
        ##     Maya behaves funny and deleted the
        ##     plusMinusAverage node when we clean
        ##     up our shaders!  arrrg!
        ##     We need to lock it while deleting
        pm.lockNode( vertexColorsPool, lock=True )    
        for v in exportsFound:
            #print v
            cmds.delete( v )
        pm.lockNode( vertexColorsPool, lock=True ) 

                
        """
        if len(exportsFound):
            #cmds.delete( exportsFound )
            print( len(exportsFound) )
            print( "Exports found are:" )
            print( "Exports found: " )
            pass
        """
            

        ## Don't restore selection here, restore it at the very end!
        ## instead just clear it for now
        cmds.select( clear=True )




        selOrig = pm.ls(selection=True)
        sel = pm.ls(selection=True)


        """
        try:
            print( vertexColorPool )
            print( vertexColorPool.name() )
        except:
            print( "vertexColorPool var does not exist" )

        try:
            vertexColorPool = pm.PyNode('vertexColorPool')
            print( "vertexColorPool found!" )
        except:  
            #vertexColorPool = c.shadingNode( 'plusMinusAverage', asUtility=True )
            ## This rename should only happen when the exception was thrown.
            ## It seems to fuck shit up otherwise
            #vertexColorPool.rename( 'vertexColorPool' )
            #delete vertexColorPool
            pass
        """

        foundVertexColorPoolList = cmds.ls( 'vertexColorPool' )
        if not len(foundVertexColorPoolList):
            new = cmds.createNode( 'plusMinusAverage' )
            cmds.rename( new, 'vertexColorPool' )
            
        foundVertexColorPoolList = cmds.ls( 'vertexColorPool' )

        assert foundVertexColorPoolList
            
            
        pm.select( selOrig )


        ## Select all the nodes that have exportVertexColors
        nodesFlagged = []
        allObjs = pm.ls()
        for obj in allObjs:
            try:
                v = obj.mmmmExportVertexColorsForMr.get()
            except:
                v = False
            if v == True:
                nodesFlagged.append( obj )




        ## delete old __ExportForMesh__ named vertex color nodes
        """
        pm.select( clear=True )
        try:
            exportsFound = pm.ls( "*__ExportForMesh__*" )
            pm.delete( exportsFound )
        except:
            print( "... Nothing to delete, no vertexColorNodes named as:  *__ExportForMesh__*   continuing... ")

        pm.select( clear=True )

        """









        """
        shapesToAdd = []
        for obj in selOrig:
            try:
                shape = obj.getShape( )
                pm.select( shape, add=True )
            except:
                print( "... no shape found for transform, continuing... " )

        sel = pm.ls(selection=True)
        print(sel)
        #selWithShapesAdded = sel + shapesToAdd
        """



        shapes = pm.ls( nodesFlagged, shapes=True )


        pm.select( sel )  ## restore selection


        vertexColorNodes = []  ## Keep track of all the vertex color nodes we made
        for obj in shapes:
            objName = obj.name()
            ## Detect color sets on the mesh and make a list of them
            sourceColorSets = []
            for i in range(5):
                sourceColorSet = objName + '.colorSet[' + str(i) + '].colorName'
                try:
                    foundSet = cmds.getAttr( sourceColorSet )
                    ## If the set we found has a name that isn't null
                    ## add it to our count
                    if foundSet:
                        sourceColorSets.append( foundSet )
                        print( "Found set:  "  + foundSet )
                    else:
                        print( "Found set was: " + foundSet )
                except:
                    print(  "...sourceColorSet not found for this attempt,  " + str(sourceColorSet) + "  continuing..." )


            print( sourceColorSets )
            #### Now that we know how many color sets we have, hook them up
            for i in range( len(sourceColorSets) ):
                sourceColorSet = objName + '.colorSet[' + str(i) + '].colorName'
                
                vertexColorNodeName = pm.mel.eval( 'mrCreateCustomNode -asTexture "" mentalrayVertexColors;' )
                pm.select(sel)  ## The last command break the select so we restore it
                vertexColorNode = pm.PyNode( vertexColorNodeName )
                vertexColorNode.rename( 'mentalRayVertexColors__ExportForMesh__' + objName + '__' + sourceColorSets[i] )
                vertexColorNode.defaultColor.set( 0,0,0 )            
                vertexColorNodes.append( vertexColorNode )
                
                sourceColorSet = objName + '.colorSet[' + str(i) + '].colorName'
                foundSet = cmds.getAttr( sourceColorSet )
                print( "Found set is:" + str(foundSet)  )
                cs = cmds.connectAttr(
                    sourceColorSet,
                    vertexColorNode.name()+ '.cpvSets[' + str(i) + ']'
                 )
                 
            
            
        ## Now that we have processed all the shapes and made vertex color nodes for them,
        ## pool them all into one additive node
        #print(  pm.listConnections( vertexColorPool )  )
        vertexColorsPool = pm.PyNode('vertexColorPool' )
        vertexColorsPool.i3.disconnect()     

        for i,v in enumerate( vertexColorNodes ):
            try:
                #print( vertexColorPool.name()  )
                #pm.connectAttr( v.outColor, vertexColorPool.i3[i] )
                #cmds.disconnectAttr( 
                cmds.connectAttr( v.name() + '.outColor', 'vertexColorsPool' + '.i3[' + str(i) + ']' )
            except:
                print( "Couldn't make connection")
                print( traceback.format_exc() )
            #cs = pm.getAttr( obj, 'colorSet' )
        #except:
        #    print(  traceback.format_exc()  )
               

        ## Restore the original selection 
        try:
            cmds.select( selectionToRestore )
        except:
            cmds.select( clear=True ) 
         
pass