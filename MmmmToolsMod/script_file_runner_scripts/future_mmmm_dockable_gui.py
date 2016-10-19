import maya.cmds as cmds

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


class MmmmMainDockableWindow(object):
    def __init__(self, mmmm=None, parentRef=None):
        
        self.widgets = {}
        self.subs = {}
        ## Create Main Widgets
        win = self.widgets['win'] = pm.window( )
        ##
        scroll = self.widgets['scroll'] = pm.scrollLayout( parent = win )
        ## The dock must be created after the window's layout
        dock = self.widgets['dock'] = pm.dockControl(
            'MmmmTools Dock',
            area='left', content=win, allowedArea=['right', 'left']
        )    

        col = self.widgets['col'] = pm.columnLayout( parent = scroll )
        
        #self.mainFrame = MmmmMainDockableWindowSub( )
        #self.mainFrame
        #self.mainFrame = 
        #self.makeMainFrame( parentLayout=col )
        
        mmmm = MmmmToolsMod.Dynamic.GetInstance()
        modellerFrame = pm.frameLayout( label="Modeler", collapsable=True, parent=col )
        modellerCol = pm.columnLayout( parent = modellerFrame )
        f1 = pm.frameLayout( label="Grid Tools", collapsable=True, parent=modellerCol )   
        mmmm.modeler.runGridTools( makeUi=True, parentWidget=f1 )
        f2 = pm.frameLayout( label="Retopo Tools", collapsable=True, parent=modellerCol )   
        mmmm.modeler.runRetoper( makeUi=True, parentWidget=f2 )
        f2 = pm.frameLayout( label="Mirror Tools", collapsable=True, parent=modellerCol )   
        mmmm.modeler.runMirrorer( makeUi=True, parentWidget=f2 )

        

dockable = MmmmMainDockableWindow()

