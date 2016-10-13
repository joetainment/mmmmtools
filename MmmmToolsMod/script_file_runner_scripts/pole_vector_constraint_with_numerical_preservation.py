## The ik handle has the information we need in it's
## pole vector attribute
import pymel.all as pm

## We can use ik


## get the ik by name
#ik = pm.PyNode('ik_heel')
## or get it by selection
selection = pm.ls(selection=True)
ik = selection[0]
 ## get the first things in 
 ## the list of selected objects


## get a locator by name
#loc = pm.PyNode('locator1')
loc = pm.spaceLocator()


## the locator first get's parented to
## the ik handle, just so it's in the right
## coordsys
## parenting order is (slave, master)
## or  (child, parent)
pm.parent( loc, ik )


## now we need to put the locator
## at the one exact "magic"
## place where the pole vector
## is for the ik handle
## it's magic, because it's the only
## place that won't "pop" out of the pose
##
## connect the ik's poleVector attribute
## to the locators translation
## which is a way of recording the data
ik.poleVector >> loc.translate
##
## now that's it is in the right
## world space location
## we can disconnect it, and unparent it
## as long as its world space location
## stays put, it works, and marks that
## location for later
##
## disconnect
loc.translate.disconnect()
## unparent (via parent to world)
## this is how you unparent in code
pm.parent( loc, world=True )

## now finally, we can constrain the
## the ik to the locator,
## using a pole vector constraint
#pm.poleVectorConstraint( targetGoal, thingBeingConstrained )
#pm.poleVectorConstraint( master, slave )
pm.poleVectorConstraint( loc, ik )