#Import Desired Libraries Here
import maya.OpenMaya as om
import maya.OpenMayaRender as omRender
import maya.OpenMayaMPx as omMPx
import pymel.all as pm
import random

#Set name and id
nodeName = "mmmmScripterNodeV001v"
nodeId = om.MTypeId(0x0011C240)  ## This is globally unique and was obtained from Autodesk


glRenderer = omRender.MHardwareRenderer.theRenderer()
glFT = glRenderer.glFunctionTable()
####  loadPlugin "D:/Dropbox/maya/2013-x64/scripts/MmmmTools/plugins/MmmmLocatorPlugin.py"; createNode mmmmJitter;

####  import random; random.seed( seedFloat); output = random.uniform( -1,1 ) * scaleFloat + offsetFloat


class MmmmScripterNodeV001(omMPx.MPxLocatorNode):
    ## attribute references (kinda sorta like pointers)
    ENABLED = om.MObject()
    DEPENDENCY = om.MObject()
    EXPRESSION = om.MObject()
    OUTPUT = om.MObject()

    def __init__(self):
        omMPx.MPxLocatorNode.__init__(self)
        
    def draw(self, view, path, style, status):
		view.beginGL()
 
		glFT.glBegin(omRender.MGL_LINES)
		glFT.glVertex3f(-1.0, 0.0, 0.0)
		glFT.glVertex3f(1.0, 0.0, 0.0)
		glFT.glVertex3f(0.0, -1.0, 0.0)
		glFT.glVertex3f(0.0, 1.0, 0.0)
		glFT.glVertex3f(0.0, 0.0, -1.0)
		glFT.glVertex3f(0.0, 0.0, 1.0)
		glFT.glEnd()
 
		view.endGL()

        
    def compute(self, plug, dataBlock):
        if (plug == MmmmScripterNodeV001.OUTPUT):
            enabledHandle = dataBlock.inputValue(MmmmScripterNodeV001.ENABLED)
            enabledBoolean = enabledHandle.asBool()
            
            if enabledBoolean:
            
                dependencyHandle = dataBlock.inputValue(MmmmScripterNodeV001.DEPENDENCY)
                dependencyFloat = dependencyHandle.asFloat()
            
                exprHandle = dataBlock.inputValue (MmmmScripterNodeV001.EXPRESSION)
                exprStData = om.MFnStringData( exprHandle.data() )
                exprSt = exprStData.string()            
            
                defaultCode = """
            
self_node = pm.PyNode(self_name)

"""
            
            
            
                exprSt = defaultCode + exprSt
            
                nodeName = self.name()
            
                ns = {}
                ns['pm'] = pm
                ns['self_name'] = str( nodeName )
                ns['dependency'] = dependencyFloat
            
                exec exprSt in ns
                result = ns.setdefault( 'output', 0.0 )
            
                outputHandle = dataBlock.outputValue(MmmmScripterNodeV001.OUTPUT )
                try:
                    outputHandle.setFloat(result)
                except:
                    outputHandle.setFloat(0.0)
                
                dataBlock.setClean(plug)


def nodeCreator():

    return omMPx.asMPxPtr( MmmmScripterNodeV001() )

 
def nodeInitializer():
	return om.MStatus.kSuccess    

def nodeInit():
    numAttr = om.MFnNumericAttribute()    
    MmmmScripterNodeV001.ENABLED = numAttr.create("enableScript","ens",om.MFnNumericData.kBoolean,1)
    numAttr.setStorable(1)

    exprSt = om.MFnStringData ()
    exprStCreator = exprSt.create ('output = 0.0  ## Your script code can set a variable (of type float) called output which will become the value of the actual output attribute. In your code, self_node is a variable automatically provided for you so that you can use it your code to refer to this node.  It is a pymel PyNode referring to this object.  To get values from this node, use self_node.yourAttributeName.get()  For multiline scripts, you can type your script into the notes attribute below, and then copy/paste it here. It might not look like the new line characters are being copied, but they are.   READ THIS ENTIRE LINE AND REPLACE IT WITH YOUR SCRIPT CODE')
    tAttr =om.MFnTypedAttribute()
    MmmmScripterNodeV001.EXPRESSION =tAttr.create ("notes", "nts", om.MFnStringData.kString,   exprStCreator)
    tAttr.setStorable (1)
    tAttr.setKeyable (False)


      
    
    numAttr = om.MFnNumericAttribute()    
    MmmmScripterNodeV001.DEPENDENCY = numAttr.create("dependency","dep",om.MFnNumericData.kFloat,0.0)
    numAttr.setStorable(1)  

    numAttr = om.MFnNumericAttribute()
    MmmmScripterNodeV001.OUTPUT = numAttr.create("output","out",om.MFnNumericData.kFloat,0.0)
    numAttr.setStorable(1)
    numAttr.setWritable(1)

    
    
    MmmmScripterNodeV001.addAttribute(MmmmScripterNodeV001.ENABLED)    
    MmmmScripterNodeV001.addAttribute(MmmmScripterNodeV001.DEPENDENCY)    
    MmmmScripterNodeV001.addAttribute(MmmmScripterNodeV001.EXPRESSION)
    
    MmmmScripterNodeV001.addAttribute(MmmmScripterNodeV001.OUTPUT)
    
    
    MmmmScripterNodeV001.attributeAffects(MmmmScripterNodeV001.ENABLED, MmmmScripterNodeV001.OUTPUT)
    MmmmScripterNodeV001.attributeAffects(MmmmScripterNodeV001.DEPENDENCY, MmmmScripterNodeV001.OUTPUT)
    MmmmScripterNodeV001.attributeAffects(MmmmScripterNodeV001.EXPRESSION, MmmmScripterNodeV001.OUTPUT)    
    
   
    

# On load plugin
def initializePlugin(mobject):
    mplugin = omMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode(nodeName, nodeId, nodeCreator, nodeInit, omMPx.MPxNode.kLocatorNode)
        ## note the last thing, where we use kLocatorNode
    except:
        sys.stderr.write("Error loading")
        raise

# On unload plugin
def uninitializePlugin(mobject):
    mplugin = omMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( nodeId )
    except:
        sys.stderr.write("Error removing")
        raise
