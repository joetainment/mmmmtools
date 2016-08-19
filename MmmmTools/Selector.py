import pymel.all as pm
import maya.cmds as cmds
import MmmmTools
import SelectorVolumeSelect
import traceback
import random
import math


## Import Volume Select, but:
##  can't reload with Maya running, causes api error and crash
class Selector(object):
    def __init__(self, parentRef):
        self.parent = parentRef
        self.mmmm = self.parent
        self.slots = {}
        self.quickList = []
        self.activeSlot = 0
        #self.volumeSelect = SelectorVolumeSelect.SelectorVolumeSelect
        #self.volumeSelectApp = SelectorVolumeSelect.SelectorVolumeSelectApp

    def printActiveSlot(self):
        self.mmmm.u.printWarning( "Selector active slot is now: " + str(self.activeSlot)  )
        
    def nextSlot( self ):
        self.activeSlot = int(self.activeSlot) + 1
        self.printActiveSlot()

    def prevSlot( self ):
        self.activeSlot = int(self.activeSlot) - 1
        self.printActiveSlot()
         
    def getSlots(self, slotsCount=2, useStartSlot=False, startSlot=None):
        if useStartSlot:
            if startSlot is None:
                startSlot = self.activeSlot        
            else:
                sslot = startSlot
        else:
            sslot = 0
            
        #n=int(n)
        result = []
        for i in xrange(slotsCount):
            result.append( self.slots[i + sslot] )
                ## this should fail if we
                ## don't have enough slots
                ## in that case we want an
                ## exception
        return result
        
    def getSlot(self, n=None):
        if n is None:
            n = int( self.activeSlot )
        else:
            n = 0
            
        n=int(n)
        return self.slots[n]
    
    def nFixDefault(self,n):
        if n is None:
            n = int( self.activeSlot )
        else:
            n = 0        
        return n

        
    def setSlot(self, n=None, listToSet=None):
        n = self.nFixDefault(n)
                    
        n = int(n)
        if isinstance(listToSet, list ):
            l = listToSet
        else:
            l = pm.ls(selection=True)
        self.slots[n] = l
        
    def selSlot( self, n=None, add=False ):
        n = self.nFixDefault(n)
        l = self.slots[n]
        self.selList( l, add=add )
        
    def selList( self, l, add=False ):
        print( "sel list function:" )
        print( l )
        print( type(l) )
        try:
            pm.select( l , add=add )
        except:
            if add==False:
                pm.select(clear=True)
            for obj in l:
                try:
                    pm.select( obj, add=True )
                except:
                    self.mmmm.u.printWarning( "Could not select a node, most likely an"
                          " object that was in the selection slot has been deleted."
                    )
                
    def setNamedSlot( self, name, listToUse=None ):
        if listToUse is None:
            listToUse = pm.ls(selection=True)
        self.slots[name] = listToUse
    
    def selNamedSlot( self, name ):
        self.selList( self.slots[name] )
        
    def setNamedSlotByUi(self):
        name = self.mmmm.prompt( 'Set/Save selection to a named slot.  Enter the name of the slot to use:', )
        if not name is None:
            name = unicode( name )
            self.setNamedSlot( name )
        
    def selNamedSlotByUi(self):
        name = self.mmmm.prompt( 'Select nodes stored in named slot.  Enter the name of the slot to use:', )
        if not name is None:
            name = unicode( name )
            self.selNamedSlot( name )
            
    def showSlotsUi( self, maxToShow=10 ):
        m = []
        
        m.append( "The following named slots are being used:" )
        m.append( "\n\n\n" )
        keys = self.slots.keys()
        if len(keys) < maxToShow:
            for k in self.slots.keys():
                if isinstance( k, basestring ):
                    m.append( k )
            msg = "\n".join( m )
        else:
            msg = "Please see the script editor \n " \
            " history for a printout of \n" \
            " named slots, since it is \n" \
            " too long to show here."
        request = self.mmmm.prompt( msg=msg )
        print( msg )
        self.selNamedSlot( unicode(request) )
        
    
    def volumeSelect( self, faces=False ):
        result = SelectorVolumeSelect.SelectorVolumeSelect.volumeSelect(faces=faces)
        return result

    def volumeSelectApp( self, faces=False ):
        print( "Volume Select App/Tool/UI current disabled because of a Maya crash bug." )
        #SelectorVolumeSelect.SelectorVolumeSelectApp( make_default_ui=True )


        

#### Note, the Ui should probably have a slider, but it doesn't have one yet.
class RandomSelectorUi(object):
    def __init__(self, mmmmTools=None, randomSelector=None):
        if randomSelector==None:
            self.randomSelector = RandomSelector()
        self.win = pm.window( 'Random Selector' )
        with self.win:
            self.col = pm.columnLayout()
            with self.col:
                self.ratioText = pm.text( "Decimal number as ratio to select:" )
                self.ratioFloat = pm.floatField(  )
                self.ratioFloat.setValue( 0.5 )
                self.selectButton = pm.button(
                    "Select by Ratio",
                    command = lambda x:
                        self.randomSelector.go(
                            self.ratioFloat.getValue()
                        )
                )
        self.win.show()

class RandomSelector(object):

    def go(self, ratio=0.5):
        self.select_random_part_of_selection_by_ratio( ratio )

    def select_random_part_of_selection_by_ratio( self, ratio=0.5 ):
        ratio_to_select = ratio
        
        ## Bail early if the ratio is high
        ## or zero of negative
        if ratio_to_select <= 0.0:
                pm.select( clear=True )

        if ratio_to_select >= 1.0:
            if ratio_to_select <= 0.0:
                pm.select( clear=True )
            else:
                return



        original_selection = pm.ls(selection=True, flatten=True )
        objs = original_selection[:]


        ## Calculate what the target selection count is,
        ## don't let the result be more than selectionlength:
        sel_len = len(objs)
        target_sel_count = int(    round( sel_len * ratio_to_select )    )
        if target_sel_count > sel_len:
            target_sel_count = sel_len


        ## Make a list of valid indexes and shuffle it
        ## should be python3 future proof
        indexes = [  index for index in range(sel_len) ]

        random.shuffle( indexes )
        shuffled_indexes = indexes

        indexes_to_select = []

        for i in range(target_sel_count):
            indexes_to_select.append( shuffled_indexes.pop() )


        ## Now that we know what to select
        ## clear the selection and
        ## then select our targets!

        pm.select( clear=True )
        for i in indexes_to_select:
            pm.select( objs[i], add=True )


pass