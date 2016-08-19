import maya.cmds as cmds
import pymel.all as pm
import pymel.tools.mel2py as Mel2py
import traceback


class MmmmLoftThroughCvs(object):
    def __init__(self):
        self.MmmmLoftThroughCvs()
        
    @classmethod
    def MmmmLoftThroughCvs( cls ):    	
    	## Create the bitmasks
    	##     melBitmaskGlobalVars could be name instead of bitmasks
    	##     and filter using them
    	bitmasks = [
    	    'gSelectNurbsCurvesBit', 'gSelectIsoparmsBit',
    	    'gSelectCurvesOnSurfacesBit', 'gSelectSurfaceEdgeBit'
    	]
    	for bitmask in bitmasks:
    	    #pm.mel.eval( "global int " + "$" + bitmask + ";" )
        	pm.melGlobals.initVar('int', bitmask)

        mg = pm.melGlobals
    	curves=pm.filterExpand(ex=True,
    	    sm=[
    	        mg[ bitmasks[0] ], mg[ bitmasks[1] ],
        	    mg[ bitmasks[2] ], mg[ bitmasks[3] ],
        	]
    	)
    	
    	print( curves )
    	print( type(curves) )

        newCurves = []
        for crv in curves:
            nList = pm.rebuildCurve(crv, rt=0, ch=True, kcp=True, rpo=False, degree=1)
            nX = nList[0]
            nS = nX.getShape()
            newCurves.append(  nX  )

        surface = pm.loft( newCurves, degree=1 )
        pm.rebuildSurface(surface, rt=0, ch=True, kcp=True, dv=3, du=3, rpo=True)

MmmmLoftThroughCvs.MmmmLoftThroughCvs()


        
"""        
class MmmmMelToPython(object):
    def __init__(self):
        self.MmmmMelToPython()
        
    @classmethod
    def MmmmMelToPython(cls, melStr=""):
        mel2py = Mel2py
        pyStr = mel2py.mel2pyStr( melStr )
        return pyStr
"""
        
        
melStr = """
        """