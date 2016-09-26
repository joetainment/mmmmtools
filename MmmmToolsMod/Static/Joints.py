import pymel.all as pm
def createTwistJointToSelectedChild():
    objs = pm.ls(selection=True)

    ## Make an empty list to store joints in
    newJoints = []

    for obj in objs:
        pm.select( clear=True )
        child = obj
        parentJnt = obj.getParent()
        jnt = pm.joint(position=[0,0,0])


        pc = pm.pointConstraint( [parentJnt, child] , jnt )
        oc = pm.orientConstraint( parentJnt, jnt )
        pm.delete( pc )
        pm.delete( oc )
        pm.parent( jnt, parentJnt )
        ## Put out new joint in the list!
        newJoints.append( jnt )

    pm.select( newJoints )