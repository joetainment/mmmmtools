import pymel.all as pm
import maya.cmds as cmds
import traceback

sourceUvSetName = 'map1'
destinationUvSetName = 'world'


oSel = pm.ls(selection=True)
objs = oSel[:]   ## shorthand for copy list

for obj in objs:
    try:
        pm.polyCopyUV( obj,
            uvSetNameInput=sourceUvSetName,
            uvSetName=destinationUvSetName,
            createNewMap=True,
            constructionHistory=True,
        )
        """
        pm.mel.eval(
            'polyCopyUV -uvSetNameInput "'
            + sourceUvSetName
            + '" -uvSetName "'
            + destinationUvSetName
            + '" -createNewMap 1 -ch 1 '
            + obj.name() 
            + ';'
        )
        """
    except:
        print( traceback.format_exc()  )
        
        
pm.select( oSel,  replace=True )