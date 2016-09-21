import maya.cmds as cmds
import maya.mel as mel
import traceback


def getShells( objs ):
    count = 0
    shells = []
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
        count+=1
    return shells