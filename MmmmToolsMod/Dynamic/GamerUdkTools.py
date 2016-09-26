import pymel.all as pm
from copy import copy as Copy
import sys


class GamerFbxExport(object):
    def __init__(self):
        self.mesh_suffix = '__mesh'
        self.ref_suffix = '__ref_mesh'

    def go(self):
        user_path = str(  raw_input()  )
        sel = pm.ls(selection=True)
        sel_orig = Copy(sel)

        for obj in sel:
            #print( type(obj)  )
            
            ## Bail early if it's not a transform node
            if not isinstance(obj, pm.core.nodetypes.Transform):
                continue
                
                
            pm.select(obj, replace=True, hierarchy=True)
            
            suf = self.mesh_suffix
            dir = user_path.replace('\\', '/' )
            dest = dir + '/' + obj.name() + suf + '.fbx'
            fmt = 'FBX export'
            pm.exportSelected( dest, type=fmt, es=True )
            
            pm.select( clear=True )
            
            
class GamerUcxRenameAndParent(object):
    def __init__(self):
        pass
    def go(self):            
        ## Get a list of the selected objects in maya
        sel = pm.ls(selection=True)
            ## in mel:   ls -sl

        ## Get the last object selected by
        ## popping it out of the list
        target = sel.pop(-1)

        for obj in sel:
            obj.rename(  'UCX_' + target.name() + '_00'  )  ## rename based on the target's name
            pm.parent( obj, target ) ## parent this object to the target


        ## Freeze transforms
        pm.makeIdentity( target, apply=True  )
        ## Select target and all its children
        pm.select( target, hierarchy=True )
        ## Delete history
        pm.delete( constructionHistory=True )


            

            
            
            
            
            
            
            
            
            
            
            
            
            
pass