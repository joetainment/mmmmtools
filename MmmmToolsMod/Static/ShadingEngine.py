import pymel
import pymel.all as pm
import maya.cmds as cmds
import traceback


def getFaceShadingGroup(face):  ## assumes face is a string, faster vs to meshface?
    sg = cmds.listSets(extendToShape=True, type=1, object=face )
    ##sg = pm.listSets(extendToShape=True, type=1, object=face)
    if len(sg)>1:
        sg = cmds.ls(
            sg,
            type='shadingEngine'
        )
    return sg[0]
#MmmmToolsMod.Static.ShadingEngine.transferShadingSetsBySpaceForSel
def transferShadingSetsBySpaceForSel( ):
    objs = pm.ls(selection=True)
    srcObj = objs.pop(0)
    transferShadingSetsBySpace( srcObj, objs)
    
    
def transferShadingSetsBySpace(srcObj, dstObjs ):
    ## this function assumes sampling in local space and
    ## searchMethod of closest in space
    ## which are the only options that really make sense for
    ## such a "one to many" type situation
    for dstObj in dstObjs:
        pm.transferShadingSets( srcObj, dstObj, sampleSpace=1, searchMethod=3 )

        
# MmmmToolsMod.Static.ShadingEngine.transferShadingSetsByComponentForSel()    
def transferShadingSetsByComponentForSel( ownProgress=True ):
    objs = pm.ls(selection=True)
    srcObj = objs.pop(0)
    transferShadingSetsByComponent( srcObj, objs, ownProgress=ownProgress )
    
def transferShadingSetsByComponent( srcObj, dstObjs, ownProgress=True ):
    oSel = pm.ls(selection=True)
    
    pm.progressWindow(endProgress=True)    
    pm.progressWindow(isInterruptable=1,
        title="Esc Key - Press To Cancel",
        status="Please wait...",
    )
    try:
        breakAll = False
        
        sgMap = {}
        
        faces = pm.ls( str(srcObj) + '.f[*]' )
        #print( "faces len is:" )
        #print( len(faces) )
        
        ## faces at this point should be a list with one entry, a range of faces
        
        for faceRange in faces:                 
            faceRangeLen = len(faceRange)
            for i,face in enumerate(faceRange):
                if i%1000==0:
                    if ownProgress==True:
                        pm.progressWindow(edit=True,
                            progress= i*1.0/faceRangeLen*50
                        )
                    if pm.progressWindow(query=1, isCancelled=1):
                        breakAll=True
                        break           
                sgStr = str( getFaceShadingGroup( str(face) ) )
                ##faceInt = int( str(face).split('[')[1].split(']')[0]  )
                if sgStr in sgMap:
                    sgMap[sgStr].append( str(face) )
                else:
                    sgMap[sgStr] = [ str(face) ]
                    
        if ownProgress==True:
            pm.progressWindow(edit=True, progress=50) 
        
        ## now we have a list populated with faceInts
        sgMapKeys = sgMap.keys()
        lenKeys = len(sgMapKeys)
        newProgress = 0
        for iSgStr, sgStr in enumerate(sgMapKeys):
            if breakAll==True:
                break                 
            if pm.progressWindow(query=1, isCancelled=1):
                        breakAll=True
                        break              
                        
            pm.select( sgMap[sgStr] )
            compacted = pm.ls(selection=True)
            compactedLen = len(compacted)
            for i, faceRange in enumerate( compacted ):
                newProgress+=1
                pm.progressWindow(edit=True, progress=50+50*(1.0*newProgress/(compactedLen * lenKeys)) )
                if True==True:   ##i%1==0:
                    if pm.progressWindow(query=1, isCancelled=1):
                        breakAll=True
                        break
                for dstObj in dstObjs:
                    try:
                        srcShape = srcObj.getShape()
                    except:
                        srcShape = srcObj
                    try:
                        dstShape = dstObj.getShape()
                    except:
                        dstShape = dstObj
                    
                    dstFaceStr = str( faceRange ).replace(  str(srcShape), str(dstShape)  )
                    #print( dstFaceStr )
                    pm.select( dstFaceStr )
                    cmds.sets( forceElement=str(sgStr), e=1)
    except:
        print( traceback.format_exc()  )
    finally:
        if ownProgress==True:
            pm.progressWindow(endProgress=True)
        pm.select( oSel )