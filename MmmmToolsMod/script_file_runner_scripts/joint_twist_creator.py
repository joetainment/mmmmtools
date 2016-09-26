import pymel.all as pm

objs = pm.ls(selection=True)

## Make an empty list to store joints in
newJoints = []

for obj in objs:
    pm.select( clear=True )
    jnt = pm.joint(position=[0,0,0])
    children = obj.getChildren()
    child = children[0]

    pc = pm.pointConstraint( [obj, child] , jnt )
    oc = pm.orientConstraint( obj, jnt )
    pm.delete( pc )
    pm.delete( oc )
    pm.parent( jnt, obj )
    ## Put out new joint in the list!
    newJoints.append( jnt )

pm.select( newJoints )