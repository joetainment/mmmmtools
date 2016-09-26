import pymel.all as pm
import sys

self = sys.modules[__name__]

#print self  ## this should print the name of this module
## something like:
##    <module 'MmmmTools.ModelerGridTools'
##    from
##    'D:/Dropbox/maya/2012-x64/scripts\MmmmTools\ModelerGridTools.pyc'>

class ModelerGridToolsClam(object):
    @classmethod
    def reset(cls):
        pm.grid(reset=True)
    @classmethod    
    def reset_using_powers_of_two(cls):
        pm.grid(reset=True)
        pm.grid(  size=4096, spacing = 1, divisions = 1 )
    @classmethod    
    def getFullSize(cls):
        """
        This function gets the size of the *entire* grid,
        not the spacing between grid lines.
        """
        return pm.grid( query=True, size=True )
    @classmethod
    def setFullSize(cls, size):
        """
        This function sets the size of the *entire* grid,
        not the spacing between grid lines.
        """
        pm.grid( size=size )
    @classmethod    
    def getSpacing(cls, log=False):
        sp = pm.grid( query=True, spacing=True )
        if log:
            print( "Grid spacing value is: " + str(sp) )
        return sp
    @classmethod    
    def getDivisions(cls, log=False):
        sp = pm.grid( query=True, divisions=True )
        if sp < 1:  ## Just in case maya ever gives us a number lower than the logically smallest
            sp = 1
        if log:
            print( "Grid spacing value is: " + str(sp) )
        return sp
    @classmethod
    def setSpacing(cls, size, setManip=False, log=False):
        if log:
            print( "Grid spacing value is: " + str(sp) )        
        pm.grid( spacing=size )
        if setManip:
            pm.manipMoveContext( 'Move', e=True, snapRelative=True, snapValue=size )
        
        
        
    @classmethod
    def grow(cls, setManip=False, log=False):
        size = cls.getSpacing( log=log)
        new_size = size * 2
        cls.setSpacing( new_size, setManip=setManip )
        if log==True:
            pm.warning(    "Grid spacing value is: " + str(  cls.getSpacing() )    )        
    @classmethod        
    def shrink(cls, setManip=False, log=False):
        size = cls.getSpacing( log=log)
        new_size = size * 0.5
        cls.setSpacing( new_size, setManip=setManip, )
        if log==True:
            pm.warning(    "Grid spacing value is: " + str(  cls.getSpacing()  )    )
            
        
    @classmethod        
    def snapVertsToGrid(cls, log=False):
        originalSelection = pm.ls( selection=True, flatten=True )
        pm.mel.eval('ConvertSelectionToVertices;')
        selVerts = pm.ls( selection=True, flatten=True )
        #objectSelection = pm.ls(selection=True, shapes=True )
        
        #selObjs = originalSelection[:]  ## copy the list
        #selVerts = pm.polyListComponentConversion(
        #    fromFace=True, fromVertex=True, fromEdge=True,
        #    fromVertexFace=True,
        #    toVertex=True )
        #    
        #selVerts = 
            
            
            
        spacing = cls.getSpacing()
        divisions = cls.getDivisions()
        
        spacingOfDivisions = spacing / float(divisions)
        
        for v in selVerts:
            if isinstance( v, pm.MeshVertex ):
                pW = v.getPosition(space='world')
                p = pW.homogenize()  ## Turn it into simply coords
                #print( type(p.x)  )                
                def onGrid(n, s):
                    return (  spacingOfDivisions * float(   round( n/float(s) )  )   )
                p.x = onGrid( p.x, spacingOfDivisions )
                p.y = onGrid( p.y, spacingOfDivisions )
                p.z = onGrid( p.z, spacingOfDivisions )
                #print( p.x, p.y, p.z )                               
                v.setPosition( p.homogenize(), space='world' )
                #print p.x,p.y,p.z
                #print( help(p)  )
                #break
        pm.select( originalSelection )

class ModelerGridTools(ModelerGridToolsClam ):
    def __init__(self, parent=None, makeUi=True):
        self.parent = parent
        self.modeler = self.parent
        self.mmmm = self.modeler.parent
        if makeUi:
            self.ui = ModelerGridToolsUi(self)
        pass

class ModelerGridToolsUi(object):
    def __init__(self, parent):
        self.parent = parent
        self.widgets = { }
        aw = self.addWidget
        win = pm.Window( title="Grid Manager", width=100,height=200)
        with aw( 'win', win):
          with aw( 'col', pm.ColumnLayout() ):
            aw('resetButton', pm.Button(label="Reset (To Maya Defaults)",
                command= lambda x: self.parent.reset()  ) )
            #aw('resetText', pm.Text(label='  '))
            aw('reset2Button', pm.Button(label="Reset (Using Powers Of Two)",
                command= lambda x: self.parent.reset_using_powers_of_two()  ) )
            aw('reset2Text', pm.Text(label='  '))
            aw('snapButton', pm.Button(label="Snap Selected Verts To Grid",
                command= lambda x: self.parent.snapVertsToGrid()  ) )
            aw('snapText', pm.Text(label='  '))
            
            aw('growButton', pm.Button(label="Grow",
                command= lambda x: self.growWithWarning(log=True)  ) )
            aw('shrinkButton', pm.Button(label="Shrink",
                command= lambda x: self.shrinkWithWarning(log=True)  ) )
            
        self.widgets['win'].show()
    
    def growWithWarning(self, log=False):
        self.parent.grow(setManip=True,log=log)
        if log:
            pm.warning( "(You can safely ignore this) Grid size set to: "+ str(self.parent.getSpacing() ) )
    def shrinkWithWarning(self, log=False):
        self.parent.shrink(setManip=True,log=log)
        if log:
            pm.warning( "(You can safely ignore this) Grid size set to: "+ str(self.parent.getSpacing() ) )
            
    def addWidget(self, name, widget):
        #if name is None or name == '':
        #    name = widget
        #if name in widgets.keys():
        #    numDigits = 0
        #    
        #    white name
        #    name = name
        self.widgets[ name ] = widget
        return widget
                

#ModelerGridToolsStatic.grow()
#ModelerGridToolsStatic.shrink()
#gcls = ModelerGridTools()
#gcls.setFullSize( 4096 )

#g = ModelerGridTools()
#g.reset()        
#g.grow()

pass