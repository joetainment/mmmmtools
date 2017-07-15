#### This document is
## https://drive.google.com/file/d/0Bw4JsMD2wNo2OXhwcWt2T01XWnc/view?usp=sharing
######  additional notes available here:
## https://drive.google.com/file/d/0Bw4JsMD2wNo2ejFsdnZPeXU1N2c/view?usp=sharing


##########  
## todo
## - constraints with and without offsets
## - no compensation parent
## - add parents to selection
## - deselect selection but select its children
## ## todo discovered with Deepti
## - auto name tip joints
## - 
## - cut and paste joint orient in world space
## - name with incrementing letter of alphabet instead of number
## - flip/spin180 joint orient around x

############## thinking behind quad/beauty fill ##########
## get original
## get count of original
## /2 for one side count

## get entire border of hole
## convert selection from

## get "other" by booleaning selection
## get count of that side by other/2
## bridge amount is one less than that side

## convert selection of bridge edges



#divide edges

#store original


#def splitSelectionIntoContinuous():
#    lists = []
    
#    return listOfLists
#############################




import traceback
import maya.cmds as cmds
import pymel.all as pm
import pymel
import datetime
import maya.OpenMaya as om


class Gad29Tools(object):

    @classmethod    
    def getAttrsByChannelForObj(cls, obj, channels):
        attrs = [ ]
        for channel in channels:
            attr = obj.name() + '.' + channel
            try:
                ## if attribute doesn't exist, this line will fail
                pyAttr = pm.Attribute( attr ) 
                attrs.append( pyAttr )
            except:
                print(   traceback.format_exc()  )
        return attrs
        
    @classmethod
    def getChannelBoxChannels(cls):
        mainChannels = pm.channelBox(
            'mainChannelBox', q=True,
            selectedMainAttributes=True
        )
        
        if mainChannels==None:  mainChannels = []

        return mainChannels
    
    @classmethod
    def checkJointsForRotZeroAndScaleAsOne( cls ):
        allOk = True
        oSel = pm.ls(selection=True)
        pm.select(hierarchy=True)
        objs = pm.ls(selection=True)
        pm.select( oSel )
        
        ##objs = objs + objs.listRelatives(children=True)
        for obj in objs:
            try:
                if type(obj) == pm.core.nodetypes.Joint:
                    testGood = (    obj.rotateX.get()==0
                            and obj.rotateY.get()==0
                            and obj.rotateZ.get()==0
                            and obj.scaleX.get()==1
                            and obj.scaleY.get()==1
                            and obj.scaleZ.get()==1
                    )
                    if not testGood:
                        allOk = False
            except:
                allOk = False
                print( traceback.format_exc() )
        return allOk
                            
                    
    def __init__(self):
        self.winTitle = "Gad29Tools"
        #try:
        #    pm.deleteUI( self.winTitle )
        #except:
        #    print( traceback.format_exc() )
        if pm.window( self.winTitle, query=True, exists=True ):
            pm.deleteUI( self.winTitle )
        self.win = pm.window( "Gad29Tools" )
        #self.win = pm.window( "Gad29Tools" + '_' +  str( datetime.datetime.today().strftime('y%Ym%md%dh%Hn%Ms%S') )    )
        self.scroll = pm.scrollLayout(parent=self.win)
        self.col = pm.columnLayout(parent=self.scroll)
        with self.col:

            self.jointsSectionLabel = pm.text( "Joints:" )
            self.autoOrientXKeepZBtn = pm.button( "auto orient x while keeping z",
                command = lambda x: self.autoOrientXKeepZForSelected()
            )
            self.autoOrientTipJointsBtn = pm.button( "auto orient tip joints",
                command = lambda x: self.autoOrientTipJointsForSelected()
            )
            self.autoOrientTipJointsBtn = pm.button( "fix joint complex xforms",
                command = lambda x: self.fixJointComplexXformsForSelected()
            )
            
            self.checkJointsBtn = pm.button( "check joints (currently only rot and scale)",
                command = lambda x: self.checkJoints()
            )  


            self.ctrlSectionLabel = pm.text( "\n" + "Controls:" )            
            self.ctrlSizeFloatField = pm.floatField(
                value=8.0
            )
            self.makeAnimCtrlAndZeroBtn = pm.button(
                "Make Anim Ctrl And Zero (at size given above)",
                command = lambda x: self.makeAnimCtrlAndZero()
            )
            self.clearSelectedCtrlsPosSlaveBtn = pm.button(
                "Clear Selected Ctrls Pos Slave",
                command = lambda x: self.clearSelectedCtrlsPosSlave()
            )
            self.clearSelectedCtrlsRotSlaveBtn = pm.button(
                "Clear Selted Ctrls Rot Slave",
                command = lambda x: self.clearSelectedCtrlsRotSlave()
            )
            self.constrainSlavesToSelectedBtn = pm.button(
                "Constrain Slaves To Selected",
                command = lambda x: self.constrainSlavesToSelected()
            )
            

            self.parentingSectionLabel = pm.text( "\n" + "Parenting:" )
            self.chainParentBtn = pm.button( "chain parent",
                command = lambda x: self.chainParent()
            )                                    
            self.chainParentWithZeroesBtn = pm.button( "chain parent with zeroes",
                command = lambda x: self.chainParentWithZeroes()
            )
            self.parentWithZeroesBtn = pm.button( "parent with zeroes",
                command = lambda x: self.parentWithZeroes()
            )
            
            #self.fromBtn = pm.button( "parent without compensation",
            #    command = lambda x: self.parentWithoutCompensation()
            #)

            self.connectionsSectionLabel = pm.text( "\n" + "Connections:" )
            
            self.fromBtn = pm.button( "from",
                command = lambda x: self.setFromAttrsViaChannelBoxAndSelection()
            )
            self.toBtn = pm.button( "to (connect)",
                command = lambda x: self.connectToAttrsViaChannelBoxAndSelection()
            )
            self.toBtn = pm.button( "to (drive)",
                command = lambda x: self.driveToAttrsViaChannelBoxAndSelectionOneToOne()
            )
            self.linearizeBtn = pm.button( "linearize",
                command = lambda x: self.linearizeViaChannelBoxAndSelection()
            )
            self.linearizeBtn = pm.button( "cycle",
                command = lambda x: self.cycleViaChannelBoxAndSelection()
            )
            

            self.parentingSectionLabel = pm.text( "\n" + "Misc:" )            
            self.fromBtn = pm.button( "makeCamPlaneForDrawing",
                command = lambda x: self.makeCamPlaneForDrawing()
            )
          
            self.checkForUnfoldNodesBtn = pm.button( "check for unfold nodes",
                command = lambda x: self.checkForUnfoldNodes()
            )            
                        
            
            
            
        self.win.show()
        
    def setFromAttrsViaChannelBoxAndSelection(self):
        channels = self.getChannelBoxChannels()
        objs = pm.ls(selection=True)
        if len(objs)==1:
            obj = objs[0]
            attrs = self.getAttrsByChannelForObj( obj, channels )
            self.fromAttrs = attrs
        else:
            om.MGlobal.displayInfo( "Please only one selected node when gathering 'from' channels.")
        
    def connectToAttrsViaChannelBoxAndSelection(self):
        channels = self.getChannelBoxChannels()
        objs = pm.ls(selection=True)
        for obj in objs:
            try:
                toAttrs = self.getAttrsByChannelForObj(obj, channels )
            
                for i,fromAttr in enumerate( self.fromAttrs ):
                    try:
                        fromAttr >> toAttrs[i]
                    except:
                        print( traceback.format_exc() )
            except:
                print( traceback.format_exc() ) 
                
    def driveToAttrsViaChannelBoxAndSelectionOneToOne(self,objs=None):
        channels = self.getChannelBoxChannels()
        if objs==None: objs = pm.ls(selection=True)
        for obj in objs:
            try:
                toAttrs = self.getAttrsByChannelForObj(obj, channels )
            
                for i,fromAttr in enumerate( self.fromAttrs ):
                    try:
                        pm.setDrivenKeyframe( at=toAttrs[i], cd=fromAttr[i] )
                        
                    except:
                        print( traceback.format_exc() )
            except:
                print( traceback.format_exc() )         
        
    def driveWithAutoSlopeToAttrsViaChannelBoxAndSelectionOneToOne(self,objs=None):
        channels = self.getChannelBoxChannels()
        if objs==None: objs = pm.ls(selection=True)
        for obj in objs:
            try:
                toAttrs = self.getAttrsByChannelForObj(obj, channels )
            
                for i,fromAttr in enumerate( self.fromAttrs ):
                    try:
                        toAttr = toAttrs[i]
                        pm.setDrivenKeyframe( at=toAttr, cd=fromAttr[i] )
                        inputs = toAttr.input()
                        
                    except:
                        print( traceback.format_exc() )
            except:
                print( traceback.format_exc() )
                
    def linearizeViaChannelBoxAndSelection(self):
        objs = pm.ls(selection=True)
        for obj in objs:
            channels = self.getChannelBoxChannels()
            for channel in channels:
                try:
                    pm.keyTangent( obj, at=channel, itt='linear', ott='linear', time=':' )
                except:
                    print( traceback.format_exc()   )
    def cycleViaChannelBoxAndSelection(self):
        objs = pm.ls(selection=True)
        for obj in objs:
            channels = self.getChannelBoxChannels()
            for channel in channels:
                try:
                    pm.setInfinity( obj, at=channel, pri='cycleRelative',poi='cycleRelative' )
                except:
                    print( traceback.format_exc()   )
                    
    def chainParent(self):
        objs = pm.ls(selection=True)
        for i,obj in enumerate(objs):
            try:
                if i==0:
                    continue
                child = objs[i-1]
                pm.parent( child, obj )
            except:
                print(traceback.format_exc() )

              
    def chainParentWithZeroes(self):
        objs = pm.ls(selection=True)
        for i,obj in enumerate(objs):
            try:
                if i==0:
                    continue
                ## if this current obj is to be parent
                ## the zero to be child is the parent of last in list
                child = objs[i-1].getParent( )
                pm.parent( child, obj )
            except:
                print(traceback.format_exc() )
      
      
    def parentWithZeroes(self):
        oSel = pm.ls(sl=True)
        objs = oSel[:] ## copy list oSel so I can change objs list but leave oSel alone
        par = objs.pop(-1)
        for child in objs:
            childZero = child.getParent()
            pm.parent( childZero, par )
         
    def makeCamPlaneForDrawing(self):
        drawPlaneGroup = pm.createNode( "transform" );
    
        size = 1024
        planeList = pm.polyPlane( w=size,h=size, sx=1,sy=1, n="drawPlane", axis=[0,0,1] )  #print( planeList )
        planeXform = planeList[0]

        planeShape = planeXform.getShape()
        planeShape.overrideEnabled.set(1)
        planeShape.overrideShading.set(0)
        
        locatorXform = pm.spaceLocator(n="drawPlaneLocator")
        locatorShape = locatorXform.getShape()
        locatorShape.localScale.set( [128,128,128] )

        camList = pm.camera( name="drawPlaneCam" )  #print( camList )
        camXform = camList[0]
        camXform.tz.set(256)        
        
        pm.parent( planeXform, locatorXform )
        pm.parent( locatorXform, drawPlaneGroup )
        pm.parent( camXform, drawPlaneGroup )
        
        pm.orientConstraint( camXform, planeXform, ) ##aimVector=[0,1,0], upVector=[0,0,1] )
        
        ## Look through cam
        pm.select( camXform )
        panel = pm.getPanel( withFocus=True )        
        pm.mel.eval( "lookThroughSelected 0 " + panel +";")
        
        pm.makeLive( planeXform )
        
    def checkJoints(self):
        result = self.checkJointsForRotZeroAndScaleAsOne()
        if result:
            msg = "Joints ok"
            om.MGlobal.displayInfo( msg ) 
        else:
            msg = "Joints not okay"
            om.MGlobal.displayInfo( msg )            
        
    def checkForUnfoldNodes(self):
        objs = pm.ls()
        
        unfold_nodes = [ ]
        
        for obj in objs:
            if type(obj) == pymel.core.nodetypes.Unfold3DUnfold:
                unfold_nodes.append( obj )
                
        pm.select( unfold_nodes )
        
        if len(unfold_nodes)>0:
            msg = "Unforld nodes were found and selected"
            om.MGlobal.displayInfo( msg )
        else:
            pm.select(clear=True)
            msg = "No Unfold nodes found, selected nothing."
            om.MGlobal.displayInfo( msg )
            ##print( msg )        
        
    #def parentWithoutCompensation
    def autoOrientTipJointsForSelected(self):
        for obj in pm.ls(sl=True):
            self.autoOrientTipJoint( obj )
        
    def autoOrientTipJoint(self,obj):
        ## this currently assumes that tip has no children
        par = obj.getParent()
        pm.parent( obj )
        obj.rotate.set( [0,0,0] )
        obj.jointOrient.set( [0,0,0] )
        obj.rotateAxis.set( [0,0,0] )
        con = pm.orientConstraint( par, obj )
        pm.delete( con )
        
        
    def fixCamsClipAndPos(self):
        ## Camera Python script to fix clipping and default positioning
        
        ## We can get maya objects by name
        persp = pm.PyNode( 'persp' )
        perspShape = pm.PyNode( 'perspShape' )
        ## We can set attributes like this
        perspShape.nearClipPlane.set( 1.0 )
        perspShape.farClipPlane.set( 99999 )
        
        
        
        top = pm.PyNode( 'top' )
        topShape = pm.PyNode( 'topShape' )
        ## We can set attributes like this
        top.translateY.set( 44444 )
        topShape.nearClipPlane.set( 1.0 )
        topShape.farClipPlane.set( 99999 )
        
        
        front = pm.PyNode( 'front' )
        frontShape = pm.PyNode( 'frontShape' )
        ## We can set attributes like this
        front.translateZ.set( 44444 )
        frontShape.nearClipPlane.set( 1.0 )
        frontShape.farClipPlane.set( 99999 )
        
        
        side = pm.PyNode( 'side' )
        sideShape = pm.PyNode( 'sideShape' )
        ## We can set attributes like this
        side.translateX.set( 44444 )
        sideShape.nearClipPlane.set( 1.0 )
        sideShape.farClipPlane.set( 99999 )        

    def constrainSlavesToSelected(self):
        oSel = pm.ls(sl=True)
        objs = oSel[:]
        for ctrl in objs:
            try:
                posSlaveAttr = ctrl.posSlave
                connectedAttrOfPosSlave = posSlaveAttr.inputs()[0]
                posSlave = connectedAttrOfPosSlave.node()
                pm.pointConstraint( ctrl, posSlave )
            except:
                print( traceback.format_exc()  )
                
            try:
                rotSlaveAttr = ctrl.rotSlave
                connectedAttrOfRotSlave = rotSlaveAttr.inputs()[0]
                rotSlave = connectedAttrOfRotSlave.node()
                pm.orientConstraint( ctrl, rotSlave )
            except:
                print( traceback.format_exc()  )
                
    def clearSelectedCtrlsPosSlave(self):
        objs = pm.ls(sl=True)
        for obj in objs:
            try:
                obj.posSlave.disconnect()
            except:
                print( traceback.format_exc()  )
                
    def clearSelectedCtrlsRotSlave(self):
            try:
                obj.rotSlave.disconnect()
            except:
                print( traceback.format_exc()  )

    def shrinkCtrlCurveHull(self):
        oSel = pm.ls(sl=True)
        for obj in oSel:
            pm.select(  obj + ".cv" )
        
    #def enlargeCtrlCurveHull(self):

    def makeAnimCtrlAndZero(self, doConnectPosSlave=True, doConnectRotSlave=True):
        ctrls = []
        objs = pm.ls(selection=True)
        for obj in objs:
            
            ## really, you have to find the first occurance of the numbered name
            ## that didn't exist in the scene as either a zero or a control
            goodNumber = None
            iter = 0
            while goodNumber == None   and   iter < 99:
                iter+=1
                if iter==0:
                    foundZ = pm.ls( obj.name() + "_zero" )
                    foundC = pm.ls( obj.name() + "_ctrl" )
                    if len(foundZ)==0  and  len( foundC )==0:
                        goodNumber = 0
                else:
                    foundZ = pm.ls( obj.name() + str(iter) + "_zero" )  ## could use .zfill(2)
                    foundC = pm.ls( obj.name() + str(iter) + "_ctrl" )
                    if len(foundZ)==0  and  len( foundC )==0:
                        goodNumber = iter
        
            if goodNumber == 0:
                basename = obj.name()
            else:
                basename = obj.name() + str(goodNumber)
            
            
            try:
                jointRadius=obj.radius.get()
            except:
                print( traceback.format_exc()  )
                jointRadius=16
            
            radiusToUse = self.ctrlSizeFloatField.getValue()
            if radiusToUse <= 0.0:
                radiusToUse = 8*jointRadius
            ctrlList = pm.circle(normal=[1,0,0], radius=radiusToUse, ch=False)
            #ctrlCircle = ctrlList[1]
            ctrl = ctrlList[0]
            pm.rename( ctrl, basename + "_ctrl" )
            pCon = pm.pointConstraint(
               obj, ctrl
            )
            oCon = pm.orientConstraint(
               obj, ctrl
            )
            ## beware, pymel returns constraints back directly, not in list
            pm.delete( [pCon, oCon] ) ## delte constraints  
        
            zeroList = pm.duplicate( ctrl )
            zero = zeroList[0]
            
            pm.rename( zero, basename + "_zero")
        
        
                
                
        
            pm.delete( zero.getShape() )
            
            pm.parent( ctrl, zero )
            #pCon = pm.pointConstraint( ctrl, obj )
            #oCon = pm.orientConstraint( ctrl, obj ) 

            pm.addAttr( ctrl, ln='posSlave', at='message' )
            pm.addAttr( ctrl, ln='rotSlave', at='message' )
            if doConnectPosSlave==True:
                obj.message >> ctrl.posSlave
            if doConnectRotSlave==True:
                obj.message >> ctrl.rotSlave
                
            ctrls.append( ctrl )
            
        pm.select( ctrls )
            




    def getParentAttr(self, obj, createOnMissing=False, useCurrentIfCreating=False):
        assert isinstance(obj, pymel.core.nodetypes.Transform)
        parAttr = None
        try:
            parAttr = obj.mmmmRiggerIntendedParent
        except:
            ## don't actually create the attribute unless
            if createOnMissing:
                pm.addAttr( obj,
                    ln='mmmmRiggerIntendedParent',
                    at='message'
                )
                parAttr = obj.mmmmRiggerIntendedParent
                if useCurrentIfCreating:
                    parObject = obj.getParent()
                    if not parObject is None:
                        parObj.message >> parAttr
        return parAttr

    def getIntendedParent(self, obj):
        parAttr = self.getParentAttr( obj )
        connectedAttr = parAttr.inputs()[0]
        parObj = connectedAtr.node()
        return parObj
        
    def setIntendedParentToCurrentParent(obj):
        assert isinstance(obj, pymel.core.nodetypes.Transform)
        parAttr = self.getParentAttr(obj, createOnMissing=True)
        parObject = obj.getParent()
        if not parObject is None:
            parObj.message >> parAttr
        else:
            parAttr.disconnect()
            
    def clearIntendedParent(self, obj):
        assert isinstance(obj, pymel.core.nodetypes.Transform)
        parAttr = self.getOrCreateParentAttr(obj)
        parAttr.disconnect()

    def clearIntendedParentOfSelected(self):
        oSel = pm.ls(sl=True)
        objs=oSel[:]
        for obj in objs:
            try:
                self.clearIntendedParent( obj )
            except:
                print( traceback.format_exc() )
                
    def setIntendedParentToCurrentParentOfSelected(self):
        oSel = pm.ls(sl=True)
        objs=oSel[:]
        for obj in objs:
            try:
                self.setIntendedParentToCurrentParent( obj )
            except:
                print( traceback.format_exc() )
                
    def parentToIntendedParent( self, obj, doUnparenting=True ):
        parAttr = self.getParentAttr() ## returns None if doesn't exists
        ## only continue if has intended parent attr
        if not parAttr is None:
            par = self.getIntendedParent( obj )
            if not par is None:
                pm.parent( obj, par )
            ## only unparent because of clear intended
            # parent if doUnparenting is True
            elif doUnparenting:
                pm.parent( obj, w=True)
                

    def rotateOnXToMatchZForSelected(self):
        oSel = pm.ls(sl=True)
        objs=oSel[:]
        for obj in objs:
            try:
                self.rotateOnXToMatchZ( obj )
            except:
                print( traceback.format_exc() )

    def autoOrientXKeepZForSelected(self ):
        oSel = pm.ls(sl=True)
        objs=oSel[:]
        for obj in objs:
            try:
                self.autoOrientXKeepZ( obj )
            except:
                print( traceback.format_exc() )
        pm.select(oSel)
                
    def autoOrientXKeepZ(self, obj ):
        assert isinstance(obj, pymel.core.nodetypes.Transform)
        
        unrepar = Unreparenter( obj )
        pm.makeIdentity( obj, apply=True, t=1, r=1, s=1, n=0, pn=1 )
        target = pm.createNode('joint')
        cons = [
            pm.pointConstraint( obj, target ),
            pm.orientConstraint( obj, target ),
            pm.scaleConstraint( obj, target )
        ]
        pm.delete( cons )
        
        
        unrepar.reparent()
        pm.joint( obj, edit=True,
            oj='xzy', secondaryAxisOrient='yup',
            zeroScaleOrient=True, children=False
        )
        unrepar.unparent( )
        pm.makeIdentity( obj, apply=True, t=1, r=1, s=1, n=0, pn=1 )
        
        
        self.rotateOnXToMatchZ(obj,target)

        pm.delete( target )
        
        pm.makeIdentity( obj, apply=True, t=1, r=1, s=1, n=0, pn=1 )
        unrepar.reparent(clean=True)

            
    def rotateOnXToMatchZ( self, obj, target ):
        assert isinstance(obj, pymel.core.nodetypes.Transform)
    
        helperZ = pm.createNode('transform')
        helperX = pm.createNode('transform')

        ## get helperZ,
        ## parent helperZ to target
        pm.parent( helperZ, target)    
        ##  zero helperZ, except +tz
        helperZ.translate.set( [0,0,16] )
        ######################### pm.duplicate( helperZ )  ## just to visualize debug
        ## parent helperZ to obj
        pm.parent( helperZ, obj )
        ## zero helperZ tx
        helperZ.tx.set( 0 )    
        ## make another helperX
        ## parent helperX to obj
        pm.parent( helperX, obj )
        ## move helperX only +tz, zero all else
        helperX.translate.set( [1,0,0] )
        ## unparent helper and helperX
        pm.parent( helperX, world=True )
        pm.parent( helperZ, world=True )
        ## should probably zero everything out that we can here
        obj.jointOrient.set( 0,0,0 )
        obj.rotateAxis.set( 0,0,0 )
        con = pm.aimConstraint( helperX, obj,
            worldUpType='object',
            worldUpObject=helperZ,
            aimVector=[1,0,0],
            upVector=[0,0,1],
        )
        pm.delete( con )   
        pm.delete( [helperX, helperZ] )
    
    def fixJointComplexXformsForSelected(self):
        oSel = pm.ls(sl=True)
        objs=oSel[:]
        for obj in objs:
            try:
                self.fixJointComplexXforms( obj )
            except:
                print( traceback.format_exc() )
        pm.select(oSel)        
        
    def fixJointComplexXforms( self, obj ):
        assert isinstance(obj, pymel.core.nodetypes.Transform)
        
        unrepar = Unreparenter( obj )
        
        pm.makeIdentity( obj, apply=True, t=1, r=1, s=1, n=0, pn=1 )
        tmp = pm.createNode('joint')
        cons = [
            pm.pointConstraint( obj, tmp ),
            pm.orientConstraint( obj, tmp ),
            pm.scaleConstraint( obj, tmp )
        ]
        pm.delete( cons )
        
        helperZ = pm.createNode('transform')
        helperX = pm.createNode('transform')
        pm.parent( helperX, tmp )
        pm.parent( helperZ, tmp )
        
        helperX.translate.set( [1,0,0] )    
        helperZ.translate.set( [0,0,1] )    

        obj.jointOrient.set( 0,0,0 )
        obj.rotateAxis.set( 0,0,0 )
        con = pm.aimConstraint( helperX, obj,
            worldUpType='object',
            worldUpObject=helperZ,
            aimVector=[1,0,0],
            upVector=[0,0,1],
        )
        pm.delete( con )   
        pm.delete( [helperX, helperZ] )
        
        pm.delete( tmp )
        
        pm.makeIdentity( obj, apply=True, t=1, r=1, s=1, n=0, pn=1 )
        unrepar.reparent( )
        





## a "class" define our own new kind of things
class RenamerUi(object):
    def __init__(self):
        self.window = pm.window( "Rename UI" )
        self.window.show()
        with self.window:
            self.col = pm.columnLayout()
            with self.col:
                pm.text( "Prefix Field" )
                self.prefixField = pm.textField( text="", width=300 )
                pm.text( "Search Field" )
                self.searchField = pm.textField( text="", width=300 )
                pm.text( "Replace Field" )
                self.replaceField = pm.textField( text="",width=300 )
                pm.text( "Suffix Field" )                
                self.suffixField = pm.textField( text="",width=300 )
                self.button = pm.button(
                    "Rename Selected",
                    command = lambda x: self.renameSelected()
                )
                self.button.setBackgroundColor( [0,0.5,0] )
                self.window.setWidth( 380 )
                self.window.setHeight( 180 )
    def renameSelected(self):
        prefix = self.prefixField.getText()
        search = self.searchField.getText()
        replace = self.replaceField.getText()
        suffix = self.suffixField.getText()
        objs = pm.ls(selection=True)
        for obj in objs:
            replacedName = obj.name().replace( search, replace )
            newName = prefix + replacedName + suffix
            obj.rename(  newName  )

class Unreparenter(object):
    def __init__(self, obj):
        self.gather(obj)
        
    def gather(self, obj, doUnparent=True):
        self.obj = obj
        if doUnparent:
            self.unparent( )
            
    def unparent( self ):
        obj=self.obj
        try:
            oParent = obj.getParent()
        except:
            oParent = None
            
        oChildren = obj.getChildren()
        oXformChildren = []
        
        for i,c in enumerate(oChildren):
            tcheck = pymel.core.nodetypes.Transform
            jcheck = pymel.core.nodetypes.Joint
            if type(c)==tcheck or type(c)==jcheck:
                oXformChildren.append( c )
                
        for c in oXformChildren:
            pm.parent( c, world=True )
        if oParent!=None:
            pm.parent( obj, world=True )
            
        self.oParent = oParent
        self.oXformChildren = oXformChildren

    def reparent(self, clean=False):
        for c in self.oXformChildren:
            pm.parent( c, self.obj )
        if self.oParent!=None:
            pm.parent( self.obj, self.oParent )
        if clean==True:
            self.clean()
        
    def clean(self):
        self.oParent = None
        self.oXformChildren = None
        self.obj = None   


               
## Runs the blueprint to create one, and make it a variable
#myRenamerUi = RenamerUi( ) 


gad29Tools = Gad29Tools()


