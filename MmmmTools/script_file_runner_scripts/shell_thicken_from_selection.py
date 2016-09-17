import pymel.all as pm
import maya.cmds as cmds
import maya.mel as melimport traceback



"""
Shell Tool for Maya

Part of MmmmTools
http://mmmmtools.celestinestudios.com
http://github.com/joetainment/mmmmtools

Written By Joe Crawford  (username Joetainment)
## Rules for how/when Maya makes backfaces when ## extruding, as I can best figure out## (if this is documented somewhere, I can't find it)
## Note that development of this tool ends up a bit "lucky"
## because the components on the border edge selection
## aren't really changed by the history, even
## when changing topo in history using
## controls like "divisions".
## Thus, we can easily set those after the fact
## without rerunning any script code.
"""
import maya.cmds as cmds
import maya.mel as mel
import traceback

def cmdslss():
    return cmds.ls(selection=True)

def getSelectionAsFaces(objs):
    oSel = cmdslss()

    cmds.select( objs )
    mel.eval('ConvertSelectionToFaces;')
    facesList = cmdslss()

    cmds.select(objs)
    cmds.select( facesList, add=True )

    allFacesWithJunk = cmdslss()
    allFacesFiltered = []
    for entry in allFacesWithJunk:
        if 'f[' in entry:
            allFacesFiltered.append( entry )

    return allFacesFiltered
    
    cmds.select(oSel)


def getShells( objs ):
    oSel = cmdslss()
    count = 0
    shells = []

    objs = getSelectionAsFaces( objs )

    while len(objs)>0 and count < 9999:
        chunk = objs[-1]
        
        objPart = chunk[:chunk.find('.')]
        firstFace = chunk.split( '[' )[1]
        firstFace = firstFace.split( ']' )[0]
        firstFace = firstFace.split( ':' )[0]
        
        toSel = objPart + ".f[" + firstFace + ']'
        cmds.select( toSel )
        mel.eval( 'ConvertSelectionToShell;')
        shell = cmds.ls(selection=True)
        shells.append( shell )
        ## see what remains in sel after
        ## shell is substracted
        cmds.select( objs )
        cmds.select( shell, deselect=True )
        
        objs = cmds.ls(selection=True)
        print( count )
        count+=1

    cmds.select(oSel )
    return shells

def getShellTest():
    index = input()
    inSel = cmdslss()
    out = getShells( inSel )
    print( out )
    cmds.select( out[index] )



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
                self.thicknessLabel = pm.text( "Thickness:             " )
                self.thicknessFloatField = pm.floatField( value=1.0, precision=9, width=200 )
                self.divisionsLabel = pm.text( "Divisions:             " )
                self.divisionsIntField = pm.intField( value=1, width=200 )
                self.mergeLabel = pm.text( "Distance (tolerance) for verts merge:" )
                self.mergeFloatField = pm.floatField( value=0.00001, precision=9, width=200 )

                self.btn1 = pm.button(label="Divisions", 
                    command=lambda x: self.shellThicken.shellThicken(
                        thickness=self.thicknessFloatField.getValue(),                        divisions=self.divisionsIntField.getValue(),                        distanceForMerge=self.mergeFloatField.getValue()
                    )
                )
        

class MmmmShellThicken(object):
    @classmethod    
    def shellThicken( cls, thickness=1.0, divisions=1, distanceForMerge=0.00001 ):
        ## Make a shorthand for listing selection
        lss = lambda: pm.ls(selection=True)
        cmdslss = lambda: cmds.ls(selection=True)
        ## Get the original selection
        oSel = cmdslss()
        
        ## Copy it so we have a list that's safe to modify
        ## without loosing the original selection
        facesSelAtStart = oSel[:]        facesSelAtStart = getSelectionAsFaces(facesSelAtStart)        shells = getShells( facesSelAtStart )
                outputSelection = []        ## use pm in the next section        ## because cmds gives a weird api error        simpleCount = 0        complexCount = 0        for shell in shells:            print( "handling shell..." )            print( shell )            doComplex = False            if len(shell)==1:                subShell=shell[0]                if not ':' in subShell:
                    print( "simple shell is:" )
                    print( shell )
                    simpleCount += 1
                    ## can extrude directly
                    pm.polyExtrudeFacet( shell, ch=1, keepFacesTogether=1, smoothingAngle=180, divisions=divisions, thickness=thickness )
                    pm.mel.eval('ConvertSelectionToShell;')
                    shellAfterExtrude = lss()
                    outputSelection += shellAfterExtrude                else:                    doComplex=True            else:                doComplex=True                        if doComplex:                complexCount+=1                print( "complex shell selected is:" )                print( shell )                pm.select( shell )                pm.polyChipOff( shell, ch=1, keepFacesTogether=1, dup=1, off=0 )                facesDup = lss()                print( facesDup )
                pm.polyExtrudeFacet( facesDup, ch=1, keepFacesTogether=1, smoothingAngle=180, divisions=divisions,  thickness=thickness )
        
                pm.polyNormal( shell, normalMode=0, userNormalMode=0 )
        
                ## Select the faces we started with, and the new faces
                pm.select(shell)
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
                shellAfterExtrude = cmdslss()
                
                ## Now convert to border edges and then verts on border
                edgesOnShellBorder = lss()
                pm.mel.eval('ConvertSelectionToShellBorder;')
                edgesOnShellBorder = lss()
                pm.mel.eval('ConvertSelectionToVertices')
                verticiesOnShellBorder = lss()
                
                pm.select( verticiesOnShellBorder )
                
                ## At this point, we should have just the border verts selected
                
                ## Merge the selected vertices                if len(verticiesOnShellBorder)!=0:
                    pm.polyMergeVertex( verticiesOnShellBorder, ch=1, distance=0.00001  )
                ##alwaysMergeTwoVerticies defaults to false
                
                outputSelection += shellAfterExtrude
                ## Output a sensible selection, all polygons in the shell
        pm.select( outputSelection )
        print( "simple shells: " + str(simpleCount) )
        print( "complex shells: " + str(complexCount) )
        """
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
        
"""
#MmmmShellThicken.shellThicken()ui = MmmmShellThickenUi()