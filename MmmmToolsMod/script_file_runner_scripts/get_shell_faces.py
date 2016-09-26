import maya.cmds as cmds
import maya.mel as mel
import traceback
def cmdslss():    return cmds.ls(selection=True)def getSelectionAsFaces(objs):    oSel = cmdslss()    cmds.select( objs )    mel.eval('ConvertSelectionToFaces;')    facesList = cmdslss()    cmds.select(objs)    cmds.select( facesList, add=True )    allFacesWithJunk = cmdslss()    allFacesFiltered = []    for entry in allFacesWithJunk:        if 'f[' in entry:            allFacesFiltered.append( entry )    return allFacesFiltered        cmds.select(oSel)

def getShells( objs ):    oSel = cmdslss()
    count = 0
    shells = []    objs = getSelectionAsFaces( objs )
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
        
        objs = cmds.ls(selection=True)        print( count )
        count+=1    cmds.select(oSel )
    return shellsdef getShellTest():    index = input()    inSel = cmdslss()    out = getShells( inSel )    print( out )    cmds.select( out[index] )getShellTest()