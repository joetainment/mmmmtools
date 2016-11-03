import pymel
import pymel.all as pm
import maya.cmds as cmds
import maya
import maya.OpenMaya as om


import MmmmToolsMod

"""
def fButton( parentForm )

myWindow = cmds.window()
buttonForm = cmds.formLayout( parent = myWindow )
cmds.button( parent = buttonForm )
cmds.button( parent = buttonForm )
allowedAreas = 'all' ##
"""

## The sub is a subsection of the dockable window
## these, ideally, can be populated by GUIs, 
## the same GUIs that are often used as windows
## instead of subs
## we can call upon those to populate the the main
## dockable window's subs dict
class MmmmMainDockableWindowSub( object ):
    def __init__( parentLayout ):
        self.widgets = {}
        self.subs = {}    
        self.makeFrame( parentLayout )
    def makeFrame( parentLayout ):
        #f = pm.frameLayout( label="test - - - - -", collapsable=True, parent=col )   
        frameOrWin = self.widgets['frameOrWin'] = parentLayout
        ##scroll = self.widgets['scroll'] = pm.scrollLayout( parent = frameOrWin )
        col = self.widgets['col'] = pm.columnLayout( parent = frameOrWin )


class UiDockable(object):
    def __init__(self, mmmm=None, parentRef=None, makeUi=False):
        self.parent = parentRef
        self.mmmm = self.parent
        if makeUi==True:
            self.create()
    
    def create(self):
        self.createNew()
    
    def createNew(self,floating=False):
        
        if self.mmmm==None:
            self.mmmm = MmmmToolsMod.Dynamic.GetInstance()
        mmmm = self.mmmm            
        self.widgets = {}
        self.subs = {}
        ## Create Main Widgets
        win = self.widgets['win'] = pm.window( )
        ##
        scroll = self.widgets['scroll'] = pm.scrollLayout( parent = win, horizontalScrollBarThickness=0 )
        ## The dock must be created after the window's layout
        dock = self.widgets['dock'] = pm.dockControl(
            'MmmmTools Dock',
            floating=floating,
            area='left', content=win, allowedArea=['right', 'left']
        )    

        col = self.widgets['col'] = pm.columnLayout( parent = scroll )
        
        #self.mainFrame = MmmmMainDockableWindowSub( )
        #self.mainFrame
        #self.mainFrame = 
        #self.makeMainFrame( parentLayout=col )
        
        
        modellerFrame = pm.frameLayout( label="Modeler",
            collapsable=True,
            parent=col,
            marginWidth=10,
        )
        modellerCol = pm.columnLayout( parent = modellerFrame )
        
        f0 = pm.frameLayout( label="Modeler Actions", marginWidth=10, collapsable=True, parent=modellerCol )
        commander = self.mmmm.commander
        cmdEntries = commander.entries
        prefix = 'Modeler/'
        for name, entry in cmdEntries.items():
            if name.startswith(prefix):
                uiLabel = entry.get( 'uiLabel' )
                if uiLabel==None:
                    ## Trim modeler from name
                    uiLabel = name[ len(prefix) : ]
                pm.button( label=uiLabel, parent=f0, command=commander.commandsMelNames[name] )
                
        
        
        f1 = pm.frameLayout( label="Grid Tools", marginWidth=10, collapsable=True, parent=modellerCol )   
        mmmm.modeler.runGridTools( makeUi=True, parentWidget=f1 )
        f2 = pm.frameLayout( label="Retopo Tools", marginWidth=10, collapsable=True, parent=modellerCol )   
        mmmm.modeler.runRetoper( makeUi=True, parentWidget=f2 )
        f3 = pm.frameLayout( label="Mirror Tools", marginWidth=10, collapsable=True, parent=modellerCol )   
        mmmm.modeler.runMirrorer( makeUi=True, parentWidget=f3 )

        pm.windowPref( win, width=500, height= 500 )
        win.setWidth( 500 )
        win.setHeight( 800 )