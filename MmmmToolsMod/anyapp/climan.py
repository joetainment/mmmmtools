import subprocess as Subprocess

class Climan(object):
    def __init__(self):
        self.testvar = True

    def call(self):
        x = 1
        
        ## restart a running script
        #os.execl(sys.executable, *([sys.executable]+sys.argv))
        #sys.stdout.flush() or os.fsync()
        
        