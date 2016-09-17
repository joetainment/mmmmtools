import pymel.all as pm
import maya.cmds as cmds
import traceback



"""
Shell Tool for Maya

Part of MmmmTools
http://mmmmtools.celestinestudios.com
http://github.com/joetainment/mmmmtools

Written By Joe Crawford  (username Joetainment)

## Note that development of this tool ends up a bit "lucky"
## because the components on the border edge selection
## aren't really changed by the history, even
## when changing topo in history using
## controls like "divisions".
## Thus, we can easily set those after the fact
## without rerunning any script code.
"""


class MmmmShellThickenUi(object):
    def __init__(self, autorun=True ):
        self.shellThicken = MmmmShellThicken( )
        if autorun==True:
            self.createUi()
        
    def createUi(self):
        self.win = pm.window(title="Mmmm Shell Thicken")
        with self.win:
            self.col = pm.columnLayout()
            with self.col:
                self.thicknessLabel = pm.text( "Thicness:              " )
                self.thicknessFloatField = pm.floatField( value=1.0, precision=9, width=200 )
                self.mergeLabel = pm.text( "Distance (tolerance) for verts merge:" )
                self.mergeFloatField = pm.floatField( value=0.00001, precision=9, width=200 )
                self.btn1 = pm.button(label="Thicken", 
                    command=lambda x: self.shellThicken.shellThicken(
                        thickness=self.thicknessFloatField.getValue(),                        distanceForMerge=self.mergeFloatField.getValue()
                    )
                )
        

class MmmmShellThicken(object):
    @classmethod    
    def shellThicken( cls, thickness=1.0, distanceForMerge=0.00001 ):
        ## Make a shorthand for listing selection
        lss = lambda: pm.ls(selection=True)
        
        ## Get the original selection
        oSel = lss()
        
        ## Copy it so we have a list that's safe to modify
        ## without loosing the original selection
        facesSelAtStart = oSel[:]
        
        
        ## Enfore the fact that this tool only works on shells
        ## if a shell isn't already selected
        pm.mel.eval('ConvertSelectionToShell;')
        shellSelAtStart = lss()
        
        
        pm.polyChipOff(shellSelAtStart, ch=1, keepFacesTogether=1, dup=1, off=0 )
        
        facesDup = lss()
        
        pm.polyExtrudeFacet( facesDup, ch=1, keepFacesTogether=1, smoothingAngle=180, thickness=1.0 )
        
        pm.select( shellSelAtStart )
        pm.polyNormal( shellSelAtStart, normalMode=0, userNormalMode=0 )
        
        ## Select the faces we started with, and the new faces
        pm.select(shellSelAtStart)
        pm.select(facesDup, add=1)
        
        
        ## Keep in mind that at this point, we don't have the side
        ## faces selected yet
        
        ## Converting selections
        ##   Some selection conversions get us there pretty easily.
        ##   These conversions are easiest to do in mel
        ##   and then just capture the result by using ls
        ##   to get the selection
        
        
        ## At this point almost everything is good, but we
        ## need to select the open/border edges and merge them.
        ## Some selection conversions will get us
        ## only the verts that are on this border
        pm.mel.eval('ConvertSelectionToShell;')
        shellSel = lss()
        
        ## Now convert to border edges and then verts on border
        edgesOnShellBorder = lss()
        pm.mel.eval('ConvertSelectionToShellBorder;')
        edgesOnShellBorder = lss()
        pm.mel.eval('ConvertSelectionToVertices')
        verticiesOnShellBorder = lss()
        
        pm.select( verticiesOnShellBorder )
        
        ## At this point, we should have just the border verts selected
        
        ## Merge the selected vertices
        pm.polyMergeVertex( verticiesOnShellBorder, ch=1, distance=0.00001  )
            ##alwaysMergeTwoVerticies defaults to false
        
        
        ## Output a sensible selection, all polygons in the shell
        pm.select( shellSel )
        
        ## This should be sufficient
        

#MmmmShellThicken.shellThicken()ui = MmmmShellThickenUi()