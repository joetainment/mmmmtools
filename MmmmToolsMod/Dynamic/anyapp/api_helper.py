            
class Api_helper(object):
    def __init__(self, obj=None):
        self.obj = obj
        
    def setObj(self, obj):
        self.obj = obj
            
    def get_obj(self):
        return self.obj
            
        
    def getInfo(self, obj, spacing=10, collapse=1):

        """
        Print methods and doc strings of objects.
        Takes module, class, list, dictionary, or string.
        """
        
        methodList = [
          method for method in dir(object) \
          if callable( getattr(object, method) )
        ]
        processFunc = \
            collapse and ( lambda s: " ".join( s.split() )  ) or (lambda s: s)
            
        info = "\n".join([
            "%s %s" % (
              method.ljust(spacing),
              processFunc(    str(  getattr(object,method).__doc__  )    )
            )
            for method in methodList
        ])        

        return info
