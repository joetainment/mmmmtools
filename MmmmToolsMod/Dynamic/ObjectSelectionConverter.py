## convert object selection to polygons only
import pymel.all as pm


class MmmmObjectSelectionConverter():
    def __init__(self):
        #self.toPolygons()
        self.toJoints()
        
    def toMeshes(self):
        self.toPolygons()
        
    def toJoints(self):
        objs = pm.ls( selection=True )
        
        converted = []
        is_confirmed = False
        #print pm.ls( selection=True, showType=True )
        for obj in objs:
            if obj.type()=='joint':
                t = obj
                is_confirmed = True
                
            if self.checkIfGivenNodeIsShape(obj)==True:
                t = obj.getParent()
                if t.type()=='joint':
                    is_confirmed = True
            if is_confirmed = True:
                converted.append( obj )
        
    def toPolygons(self):
        ## could have feature added to select joints if they have poly shape nodes
        
        objs = pm.ls( selection=True )
        
        converted = []
        #print pm.ls( selection=True, showType=True )
        for obj in objs:
            print obj.type()
            is_confirmed_as_mesh = False 
            if obj.type()=='transform':
                s = obj.getShape()
            if obj.type()=='mesh':
                s = obj
                obj = s.getParent()
                is_confirmed_as_mesh = True
                
            if is_confirmed_as_mesh==False:
               if s.type()=='mesh':
                   is_confirmed_as_mesh = True
            
            if is_confirmed_as_mesh==True:
                converted.append( obj )
                
        pm.select( converted )
        

    def checkIfGivenNodeIsShape( node ): 
        nodeIsShape = False
        if node.getParent()!=None:
            if node.type()!='transform' and node.type()!='joint':
                nodeIsShape = True


        return nodeIsShape
            
                
                
     
    
    #print(    help( type(obj) )    )
    #try:
    #    s = obj.getShape()
    #    if isinstance



#polyObjs = pm.ls( objs, typ='mesh' )
#print( polyObjs )
#pm.select( polyObjs )

x = MmmmObjectSelectionConverter()
