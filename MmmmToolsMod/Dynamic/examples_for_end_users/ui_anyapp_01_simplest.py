from collections import OrderedDict
from PySide import QtGui
import pymel.all as pm
import MmmmTools



app = MmmmTools.MmmmAnyapp(
    make_default_ui=True,
    ui_title='Your Window Title',
    ui_widgets = {
        'cubeButton':QtGui.QPushButton(
            'Make a cube!',
            clicked=lambda: pm.polyCube(),
        ),
        'sphereButton':QtGui.QPushButton(
            'Make a sphere!',
            clicked=lambda: pm.polySphere(),
        ),
    } ,
    ui_width = 300,
)

pass

"""
from collections import OrderedDict
from PySide import QtGui
import pymel.all as pm
import MmmmTools


your_ui_widgets = OrderedDict()
your_ui_widgets['cubeButton'] = QtGui.QPushButton( 'Make a cube!' )
your_ui_widgets['cubeButton'].clicked.connect(
    lambda: pm.polyCube()
)
your_ui_widgets['sphereButton'] = QtGui.QPushButton( 'Make a sphere!' )
your_ui_widgets['sphereButton'].clicked.connect(
    lambda: pm.polySphere()
)

app = MmmmTools.MmmmAnyapp(
    make_default_ui=True,
    ui_title='Your Window Title',
    ui_widgets = your_ui_widgets,
    ui_width = 300,
)

pass
"""