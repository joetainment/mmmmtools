import pymel.all as pm

## Get selected objects

total = int( input() )

oSel = pm.ls(selection=True)

toothOrig = oSel[0]
path = oSel[1]

new_teeth = []
for n in range(total):
    new_tooth_list = pm.duplicate( toothOrig )
    new_tooth = new_tooth_list[0]
    new_tooth_name = new_tooth.name()
    new_teeth.append( new_tooth )
    mPathName = pm.pathAnimation(
        new_tooth,
        curve=path,
        follow=True,
        followAxis='x',
        upAxis='y',
        inverseUp=True,
        worldUpObject='inverse_up_ref_xform',
        worldUpType='object'
    )
    mPath = pm.PyNode(mPathName)
    mPath.rename(
        new_tooth_name + '_mpath'
    )
    mPathName = mPath.name()
    mPath.uValue.disconnect()
    exprName = new_tooth_name + '_expr'
    
    exprCode = ( mPathName
        + '.uValue='
        + '(driver_y.translateY/100 + '
        + str( n/float(total) ) + ')%1.0'
    )

    
    
    exp = pm.expression(
        name= exprName,
        s = exprCode
        ##s is short for string
    )
    
    