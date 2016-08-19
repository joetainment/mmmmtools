import pymel.all as pm

class HotBoxToggler(object):
    def __init__(self, parent):
        self.parent = parent
        self.toggleSwitch = 0
    def toggle( self ):
        if self.toggleSwitch == 0:
            pm.hotBox()
            self.toggleSwitch = 1
        else:
            pm.hotBox(release=True)
            self.toggleSwitch = 0