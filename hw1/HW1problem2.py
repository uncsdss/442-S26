#!/usr/bin/env python

from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *

from panda3d.core import TextNode, LVector3
from direct.task.Task import Task
from panda3d.core import WindowProperties

import util442


class HW1problem2(ShowBase):
    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)
        self.disableMouse()

        # Get current window properties
        props = WindowProperties()
        # Set new size (e.g., 1024x768)
        props.setSize(1024, 768)
        # Apply the properties to the window
        base.win.requestProperties(props)
        
        self.camera.setPos(0, -60, 12)
        # This code puts the standard title and instruction text on screen
        self.title = OnscreenText(text=__class__.__name__,
                     style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.07,
                     parent=base.a2dBottomRight, align=TextNode.ARight)

        self.cube = render.attachNewNode(util442.make_cube(2))
        self.cube.setTwoSided(True)  

        self.mainLoop = taskMgr.add(self.simulationLoop, "simulationLoop")

    def simulationLoop(self, task):
        # Standard technique for finding the amount of time since the last frame
        dt = globalClock.getDt()
        simulationIteration(self.cube, dt)
        return Task.cont


heading = 0.0
pitch = 0.0
roll = 0.0

pos=25.0
vel=0.0

def simulationIteration(cube, dt):
    global heading, pitch, roll
    heading += 20.0*dt # just for fun, make the cube spin
    cube.setHpr(heading, pitch, roll)

    global pos, vel
    # add code here to implement a bouncing cube
    # hint: you will need to use dt (the delta time)
    cube.setPos(0,0,pos)    

simulation=HW1problem2()
simulation.run()