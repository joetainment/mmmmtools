import pymel.all as pm

class Duck(object):
    pass

class DrivenKeyMaker( object ):
    ## Static and class methods
    @classmethod
    def makeDrivenKeysForPairs( cls, driverAttr, drivenAttr, drivenDrivenPairs ):
        for pair in driverDrivenPairs:
            driverValue = pair[0]
            drivenValue = pair[1]
            sphereTy.set( drivenValue )
            cubeTy.set( driverValue )
            pm.setDrivenKeyframe( drivenAttr, cd=driverAttr )


    ## Instance Methods
    def __init__(self, autoRunTestCaseA=None):
        if autoRunTestCaseA:
            self.testCaseA()
        
    def testCaseA(self):
        testCaseA_ctx = Duck()
        ## this changes the ctx a lot!  populates it with objects etc
        testCaseA_makeGeo( testCaseA_ctx )
        
        testCaseA_ctx.driverDrivenPairs = [
            [0,0]
            [1,2]
        ]
        self.makeDrivenKeysForPairs(
            testCaseA_ctx.driverAttr,
            testCaseA_ctx.drivenAttr,
            testCaseA_ctx.driverDrivenPairs
        )
        
        
        
        ## Here a list of driven pairs
        
        
         
    def testCaseA_makeGeo(self, ctx):
        ## Make geo objects and get the nodes for their xforms (transforms)
        ctx.sphereList = polySphere()  ## creating gives list, not one object
        ctx.cubeList = polyCube()
        ctx.sphere = ctx.sphereList[0]  ## xform is first in list
        ctx.cube = ctx.cubeList[0]

        ## Move the objects apart to be side by side on x
        ## to change an attribute directly,
        ## we use the set method
        ctx.sphere.tx.set(-2)  
        ctx.cube.tx.set(2)


        ## Get the attributes
        ##   note that this isn't getting the value
        ##   of the attribute, this is getting
        ##   the attribute itself, as an object,
        ##   which will have it's own useful methods
        ##   Remember, getattr is a python built-in function
        ctx.driverAttr = getattr( ctx.sphere, 'translateY' )
        ctx.drivenAttr = getattr( ctx.cube, 'translateY' )

