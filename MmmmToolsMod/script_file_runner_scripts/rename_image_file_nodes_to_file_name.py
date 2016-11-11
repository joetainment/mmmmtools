## this script based on an idea originally found at:
## magnus-olsson.se


import pymel.all as pm
import traceback
import os


fileNodes = pm.ls(textures=True)
## or alternatively, just selected file node
# fileNodes = pm.ls(textures=True, selection=True)
 
for f in fileNodes:
    try:
        fileNameFull = f.fileTextureName.get()
        fileNameBase = os.path.basename(fileNameFull)
        fileName, fileExt = os.path.splitext(fileNameBase)
        pm.rename(f, fileName )
    except:
        print( traceback.format_exc() )