"""
MmmmTools Riveter - Makes "rivets", which are locators that follow a specific point on a surface via uvs
Written by Joe Crawford, originally in 2009, but kept up to date for the present.
This script is part of the MmmmTools package.

This script makes locators which will follow each selected vertex.
(It can create multiple locators for multiple selected verticies)

"""
import maya.cmds as cmds
import maya.OpenMaya as api
import pymel.all as pm


def getT(node):
      """
      Get The Transform Node associated with a given PyNode, if given a list, return the first transform found

      usage:   yourTransform = getT( yourPyNode )      
      
      """
      if node.nodeType() == 'transform':
        ## In this case, we are simple verifying and ensuring that the node is a transform node, so just return what was given
        return node      
      
      elif type(node) == type( ["word"] ):
        ## In this case, since the node is a list, return the first transform found in the list
        for item in node:
          ##  **** Consider adding a recursive function here to get a transform from selections of multiple shapes etc...
          ## Keep checking the items and once a transform is found, return it
          if item.nodeType() == 'transform':
            isNodeFound = True
            return item
      
      ## Neither of the above special cases are true. More work is required.
      else:
        try:
          ## Some objects have a very easy 'getParent()' function, so we'll use it if we can
          parentNode = node.getParent()
        except:
          ## When 'getParent()' doesn't work, we can use list connections, and get the first shape it gives us     
          parentNode = node.listConnections(type='shape')[0]
        finally:
          ## This block always executes  -  check to make sure we actually got a transform, and if we did, return it
          if parentNode.nodeType() == 'transform':
            return parentNode
          else:
            ## No transform was found, raise error and print warning
            print( "Error!  Can't find transform!")
            raise Exception, "Could not get transform node"
            return None


class RiggerRiveter(object):
    """
    Riveter - factory class for creating rivets.
    
    usage:  r = MmmmRiveter(run=True)
    
            or, for gui:
            
    soon to be added as a new feature....   usage:  r = MmmmRiveter(gui=True)
    
    """
    def __init__(self, run=True):
        """
        Initialize Riveter, and optionally continue to create the option rivets. See docs above for MmmmRiveter class.       
        """
        self.lastRivetsCreated = []
        self.msgSucess = "Rivets all sucessfully created."
        self.emsgPleaseSelect = """
        
                Please select mesh verticies or nurbs CVs and try again.
        
                """
        #self.ui = MmmmRiveterUi()  ####  **** It's dead simple to put a ui in, this will be added soon
        if run:
            self.createRivet()
    
    def createRivet(self):
        """
        Create one rivet for each selected vertex
        """
        selObjs = pm.ls(selection=True)
        if not selObjs:
            ## Nothing is selected, so print out warning and raise error        
            print( self.emsgPleaseSelect )
            return
            #raise Exception, self.emsgPleaseSelect
        self.originalSel = selObjs  #### Store this step of of the selection in case we want it again later

        uvs = []
        
                
        uvs.extend( pm.polyListComponentConversion( selObjs, tuv=True )  ) #### Change this to the full version
              
        #uvs.extend( [uv for uv in selObjs if '.uv' in uv] )  #### This is a very good list comprehension, perhaps expand it though
            ## the extend method of a list adds all items from another given list to the list

        uvsFromNurbs = []
        for i in selObjs:
            if pm.objectType( i ) == 'nurbsSurface' :
                uvs.append( i )

        
        ##  select our new, smaller/filtered uvs       
        pm.select( uvs )
        uvs = pm.ls( flatten = True, selection = True )  ## The flatten command returns each component individually in the list, rather than using strings that specify ranges of selections.  It takes more RAM but is often much more suitable to work with.

        ## Create a group so that we can organize the rivets  -  **** Note that this should be improved with the MmmmTools upcoming unique naming system
        if not pm.objExists('_follicle_grp'):    #### This line and the next should eventually be improved to not use a hardcoded name
            group = pm.group( em = True, w=True, n='_follicle_grp' )    #### **** Totally recreate this line, use a variable name or at least a unique one
        else:
            group = pm.PyNode('_follicle_grp')
            
        rivets = []
        
        pm.select( selObjs )

        failCount = 0

        ## Give an error msg if the user didn't use the script on a compatible selection
        if not uvs:
            failCount += 1
            print( self.emsgPleaseSelect )

        ## Everything is good, proceed to investigate and create rivets
        for uv in uvs:
                ## The commented out print line are simple useful for debugging
                print pm.objectType( uv )                
                
                objShapeName, index = tuple( uv.split( '.', 1 )  )
                obj = pm.PyNode( objShapeName )
                loc = pm.createNode( 'locator' )
                tr = getT( loc ) 
                #print( "Transform was: " + tr )
                hair = pm.createNode( 'follicle', parent = tr )
                pm.parent( tr, group )  ####  This line sucks because it's using a fucking stupid name again
                rivets.append( tr )
                
                ## Poly mesh handler
                if pm.objectType( obj ) == 'mesh':
                    obj.outMesh >> hair.inputMesh
                    uvPos = pm.polyEditUV( uv, query=True )
                ## Nurbs surface handler
                elif pm.objectType( obj ) == 'nurbsSurface':
                    obj.local >> hair.inputSurface
                    ## The index is a messy string, so we need to pull uv data out of it
                    uvTuple = ( index.strip('.uv[]').split('][')  )
                    ## We need to create the tuple as floats, because we got it as strings
                    uvPos = (    float(uvTuple[0]), float(uvTuple[1])     )
                    #uvPos = ( uvTuple[0], uv[1] )#index.strip('.uv[]').split('][')

                    ## Handle conditions where the uvs aren't normalized, this may not be required often
                    maxU = float(  obj.maxValueU.get()     )
                    maxV = float(  obj.maxValueV.get()     )
                    uvPos = (    uvPos[0]/maxU,  uvPos[1]/maxV   )
                ## Handle other cases, where this script can't do anything useful
                else:
                    print( obj + ' with uv: ' + uv + \
                        '   was incompatible, it much be either polygons or Nurbs' )
                    failCount += 1                        
                    continue
                    
                u, v = uvPos                    

                ## Make the hair follow the model, both by parenting, and by keeping its translate and rotate matched
                obj.worldMatrix >> hair.inputWorldMatrix
                hair.outTranslate >> tr.translate
                hair.outRotate >> tr.rotate   ## Note:  The hair has no outScale
                
                ## Set the u and v parameters of the hair so that it sticks to the correct place on the model
                hair.parameterU.set( u )
                hair.parameterV.set( v )
                
                ## Put the rivet into a group so we can select it afterwards
                self.lastRivetsCreated.append( loc )
           
        ## Select all the new rivets we created
        pm.select( self.lastRivetsCreated, replace=True )
        if failCount:
            print( str(failCount) + """ rivets failed to be created. Most likely because the selection was not correct. Try selecting vertices on a nurbs surface or a polygon mesh and running the script again. """)
        else:
            print( self.msgSucess )
        return       

## If running the script directly, use this next line:
