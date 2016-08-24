import pymel.all as pm
import maya.cmds as cmds
import traceback


textureName='checker1'
uvSetName='map1'

uvChannel=3


oSel = pm.ls(selection=True)
objs = oSel[:]   ## shorthand for copy list

for obj in objs:
    
    uvSetsList = cmds.polyUVSet( query=True, allUVSets=True )
    uvSetsNamesList = cmds.polyUVSet( query=True, allUVSetsWithCount=True )
    uvSetsIndiciesList = cmds.polyUVSet( query=True, allUVSetsIndices=True )
    
    print( uvSetsList )
    print( uvSetsNamesList )
    print( uvSetsIndiciesList )
    
    uvSetIndiciesByName = dict(  zip( uvSetsNamesList, uvSetsIndiciesList )  )
    
    print( uvSetIndiciesByName )

    uvIndex =  int(uvSetIndiciesByName[uvSetName])
    
    
    
    uvSetQualifiedName = obj.name() + '.uvSet[' + str(uvIndex) + '].uvSetName';


    try:
        print( uvSetQualifiedName )
        print( textureName )
        cmds.uvLink( uvSet=uvSetQualifiedName, texture=textureName )
        """
        uvCmd = (
            'uvLink -texture '
           + textureName
           + ' -uvSet '
           + uvSetQualifiedName
           + ';'
        )
        print( uvCmd )
        pm.mel.eval(
           uvCmd
        )
        """
    except:
        print( traceback.format_exc()  )
        
        
pm.select( oSel,  replace=True )