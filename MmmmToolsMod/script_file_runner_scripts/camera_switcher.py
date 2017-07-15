## Original idea by Marcel Gorri
## in future I would like to make a couple simple camera cycle button,
## one to cycle through all persp views and another to cycle through ortho views
#change to perspective cam
withFocus = mc.getPanel(wf=True)
mel.eval("lookThroughModelPanel persp %s;" %(withFocus))
#change to concept_cam
#withFocus = mc.getPanel(wf=True)
#mel.eval("lookThroughModelPanel concept_cam %s;" %(withFocus))