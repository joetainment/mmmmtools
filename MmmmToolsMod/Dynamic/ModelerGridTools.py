import pymel
import pymel.all as pm
import maya
import maya.cmds

import MmmmToolsMod





class ModelerGridTools(object):
    def __init__(self, parent=None, makeUi=True):
        self.parent = parent
        self.modeler = self.parent
        self.mmmm = self.modeler.parent
        if makeUi:
            self.ui = ModelerGridToolsUi(self,self.mmmm)
        pass
    @classmethod    
    def grow(cls, setManip=True,log=True ):
        MmmmToolsMod.Static.Grid.grow(setManip=setManip,log=log)
    @classmethod
    def shrink(cls, setManip=True,log=True ):
        MmmmToolsMod.Static.Grid.shrink(setManip=setManip,log=log)

    @classmethod
    def putSelectedObjsOnGrid(cls):
        MmmmToolsMod.Static.Grid.putSelectedObjsOnGrid()

    @classmethod
    def putSelectedVertsOnGrid(cls):
        MmmmToolsMod.Static.Grid.putSelectedVertsOnGrid()

        
class ModelerGridToolsUi(object):

    def __init__(self,parent=None,mmmm=None):
        self.parent = parent
        self.mmmm = mmmm
        self.widgets = { }
        
        self.annotationAboutInteraction = (
            "The settings should also auto apply when you change them,\n "+
            "but due to a Maya bug, you may occasionally have to apply manually,\n "+
            "with the button."
        )
        
        aw = self.addWidget
        win = pm.Window( title="Grid Manager", width=100,height=200)
        
        try:
            initialMultiplier = pm.melGlobals['MmmmToolsModelerGridToolsMultiplier']
        except:
            initialMultiplier = 1.0
            pm.melGlobals.initVar( 'float', 'MmmmToolsModelerGridToolsMultiplier' )
            pm.melGlobals['MmmmToolsModelerGridToolsMultiplier'] = 1.0
        initialSpacing =(
            (    pm.grid( query=True, spacing=True ) / pm.grid( query=True, divisions=True )    )
            /
            initialMultiplier
        )
        initialWholeSize = pm.grid( query=True, size=True ) / initialMultiplier
        
        
        with aw( 'win', win):
          with aw( 'col', pm.ColumnLayout() ):
            aw('mayaOptionsButton',pm.Button(label="Maya Grid Options...",
                    command= lambda x: pm.mel.eval("GridOptions;")
                )
            )
            aw('resetButton', pm.Button(label="Reset (To Maya Defaults)",
                command= lambda x: self.resetToMayaDefault()  ) )
            #aw('resetText', pm.Text(label='  '))
            aw('reset2Button', pm.Button(
                    label="Apply These Settings",
                    annotation=self.annotationAboutInteraction,
                    command= lambda x: MmmmToolsMod.Static.Grid.reset_via_numbers(
                        multiplier=self.getMultiplierFromUi(),
                        spacing=self.getSpacingFromUi(),
                        wholeSize=self.getWholeSizeFromUi(),
                        setManip=True,
                    )
                )
            )
            
            
            ## note the "with" doesn't work with rows,
            ## so we manually specify parents
            priorParent=self.widgets['col']
            
            row1 = self.widgets["row1"] = pm.rowLayout( numberOfColumns=2 )
            aw( 'rowText1', pm.Text('Multiplier:', parent=row1)  )
            aw( 'multiplierFloatField', pm.floatField(value=initialMultiplier, parent=row1,
                    annotation="This will mutiply with both spacing and whole size \n " +
                        "to determine the final amount used. \n \n"+
                        self.annotationAboutInteraction,
                    changeCommand= lambda x: self.onChangedField(),
                    enterCommand= lambda x: self.onChangedField(),
                )
            )
            pm.setParent( priorParent )  
            
            row2 = self.widgets["row2"] = pm.rowLayout( numberOfColumns=2 )
            aw( 'rowText2', pm.Text('Spacing:', parent=row2)  )
            aw( 'spacingFloatField', pm.floatField(value=initialSpacing, parent=row2,
                    annotation="This will control grid point spacing,\n "+
                        "and will multiply with multiplier\n "+
                        "to determine the final amount used. \n \n"+
                        self.annotationAboutInteraction,
                    changeCommand= lambda x: self.onChangedField(),
                    enterCommand= lambda x: self.onChangedField(),
                )
            )
            pm.setParent( priorParent )  
            
            row3 = self.widgets["row3"] = pm.rowLayout( numberOfColumns=2 )            
            aw( 'rowText3', pm.Text('Whole:', parent=row3)  )
            aw( 'wholeSizeFloatField', pm.floatField(value=initialWholeSize, parent=row3,
                     annotation="This will control the extents of the whole grid,\n " +
                        "(width/height) and will multiply with multiplier \n "+
                        "to determine the final amount used. \n \n"+
                        "Note, Maya's grid width is like a radius, \n"+
                        "visible grid in Maya always looks twice as tall/wide, \n"+
                        "since the 'size' setting in Maya is distance from grid center, \n"+
                        "that's how Maya is intended to work. \n \n"+
                        self.annotationAboutInteraction,           
                    changeCommand= lambda x: self.onChangedField(),
                    enterCommand= lambda x: self.onChangedField(),
                )
            )
            pm.setParent( priorParent )
            
            row4 = self.widgets["row4"] = pm.rowLayout( numberOfColumns=2 )            
            aw( 'rowText4', pm.Text('Auto adjust discreet move:', parent=row4)  )
            aw( 'setManipCheckBox', pm.CheckBox(value=True, label=' ', parent=row4) )
                ## the checkbox has a built in label, but that shows on wrong side
            pm.setParent( priorParent )  
            
               
               
            aw('spacerBlankText', pm.Text(label='  '))

            aw('snapButton', pm.Button(label="Snap Selected Objs To Grid",
                command= lambda x: MmmmToolsMod.Static.Grid.putSelectedObjsOnGrid()  ) )
            aw('snapButton', pm.Button(label="Snap Selected Verts To Grid",
                command= lambda x: MmmmToolsMod.Static.Grid.snapVertsToGrid()  ) )
            aw('snapText', pm.Text(label='  '))
            
            aw('growButton', pm.Button(label="Grow",
                command= lambda x: self.growWithWarning(log=True)  ) )
            aw('shrinkButton', pm.Button(label="Shrink",
                command= lambda x: self.shrinkWithWarning(log=True)  ) )
            
        self.widgets['win'].show()
    
    
    def resetToMayaDefault(self):
        MmmmToolsMod.Static.Grid.reset(setManip=True)
        ## Maya default size is 5 with 5 divisions, results in one
        ## since this tool doesn't use divisions
        spacing = pm.grid( query=True, spacing=True ) / pm.grid( query=True, divisions=True )
        wholeSize = pm.grid( query=True, size=True )
        
        f = self.widgets['spacingFloatField']
        f.setValue(  spacing )
        f = self.widgets['multiplierFloatField']
        f.setValue(  1.0 )
        f = self.widgets['wholeSizeFloatField']
        f.setValue(  wholeSize )

    
    def getMultiplierFromUi(self):
        return self.widgets['multiplierFloatField'].getValue()
    
    def getSpacingFromUi(self):
        return self.widgets['spacingFloatField'].getValue()
    
    def getWholeSizeFromUi(self):
        return self.widgets['wholeSizeFloatField'].getValue()
    
    def getSetManipFromUi(self):
        return self.widgets['setManipCheckBox'].getValue()
    
    def growWithWarning(self, log=False):
        ## This grow function will increase total size if required.
        self.applyUiNumbers()
        
        ## Double the value of the UI field
        f = self.widgets['spacingFloatField']
        f.setValue(  2.0 * f.getValue()  )
        ## Double the actual grid spacing
        MmmmToolsMod.Static.Grid.grow(setManip=True,log=log)

        ## Check to make sure the spacing isn't too big
        ## if the grid spacing is too large, adjust the whole grid size to accomadate
        spacingOfActualGrid = pm.grid( query=True, spacing=True ) / pm.grid( query=True, divisions=True )
        wholeSizeOfActualGrid = pm.grid( query=True, size=True )
        multiplier=self.getMultiplierFromUi()
        w = self.widgets['wholeSizeFloatField']
        
        if spacingOfActualGrid>wholeSizeOfActualGrid:
            spacing = self.getSpacingFromUi()
            newWholeSizeNoMultiplier = spacing
            newWholeSizeWithMultiplier = newWholeSizeNoMultiplier * self.getMultiplierFromUi()
            pm.grid(    size=newWholeSizeWithMultiplier    )
            w.setValue( newWholeSizeNoMultiplier )
            
        
        if log:
            pm.warning( "(You can safely ignore this) Grid size set to: "+ str(MmmmToolsMod.Static.Grid.getSpacing() ) )
            
            
    def shrinkWithWarning(self, log=False):

        self.applyUiNumbers()
        ## Half the UI fields        
        f = self.widgets['spacingFloatField']
        f.setValue(  0.5 * f.getValue()  )    
        ## Half the actual Maya size
        MmmmToolsMod.Static.Grid.shrink(setManip=True,log=log)
        if log:
            pm.warning( "(You can safely ignore this) Grid size set to: "+ str(MmmmToolsMod.Static.Grid.getSpacing() ) )
    
    def onChangedField(self):
        self.applyUiNumbers()
        
    
    def applyUiNumbers(self):
            MmmmToolsMod.Static.Grid.reset_via_numbers(
                        multiplier=self.getMultiplierFromUi(),
                        spacing=self.getSpacingFromUi(),
                        wholeSize=self.getWholeSizeFromUi(),
                        setManip=self.getSetManipFromUi(),
            )
            pm.melGlobals['MmmmToolsModelerGridToolsMultiplier'] = self.getMultiplierFromUi()

    
    def addWidget(self, name, widget):
        #if name is None or name == '':
        #    name = widget
        #if name in widgets.keys():
        #    numDigits = 0
        #    
        #    white name
        #    name = name
        self.widgets[ name ] = widget
        return widget
                

pass