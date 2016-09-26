import sysimport pymel.all as pmimport maya.cmds as cmdsimport maya.OpenMaya as omimport MmmmToolsModimport MmmmToolsMod.Static
def info(msg):
    om.MGlobal.displayInfo(msg)

def warning(msg):
    om.MGlobal.displayWarning(msg)

def error(msg):
    om.MGlobal.displayError(msg)