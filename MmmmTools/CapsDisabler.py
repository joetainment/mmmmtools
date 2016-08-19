import subprocess as Subprocess

import pymel.all as pm


class CapsDisabler(object):
    def __init__(self, parentRef, go=False):
        self.parentRef = parentRef
        self.ini = self.parentRef.ini
        self.conf = self.ini.conf        
        self.enabled = False
        
        self.autohotkeyProcess = None
        
        if go==True:
            self.go()
            
            
    
    def go(self):
        try:
            if int(  self.ini.getItem("disable_capslock")  ) == 1:
                self.enabled = True
            else:
                #print("Hotkeys not enabled.")
                pass
        except:
            print("\n  Could not start CapsLock disabling system or could "
            "not find info on it's configuration, perhaps because of "
            "missing info in the ini file. \n")
            
        if self.enabled:
            self.disableCapslock()
    def killAutohotkeyProcess(self):
        if isinstance( self.autohotkeyProcess, Subprocess.Popen ):
            try:
                self.autohotkeyProcess.kill()
            except:
                u.log( "Autohotkey process not stopped. Perhaps it had "
                        "not been started.")
            
            self.autohotkeyProcess = None
        else:
            self.autohotkeyProcess = None
            
                        
    def disableCapslock(self):
        self.killAutohotkeyProcess()
        self.autohotkeyProcess = None
        self.autohotkeyProcess = Subprocess.Popen( self.parentRef.env.conf.autohotkey_command )
    
    def startDisablingCapslock(self):
        self.disableCapslock()
    
    def stopDisablingCapslock(self):
        self.killAutohotkeyProcess()
        
    def setDisableCaplockOn(self):
        print( "pretending to set disable_capslock to ON" )
        #self.ini.setItem( disable_capslock, 1 )  ##untested code
        pass
    def setDisableCapslockOff(self):
        print( "pretending to set disable_capslock to OFF" )
        #self.ini.setItem( disable_capslock, 0 )
        pass