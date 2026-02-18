#!/usr/bin/env python

from math import cos, sin
import random
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *

from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import TextNode, LVector3
from direct.task.Task import Task
from panda3d.core import WindowProperties
from panda3d.core import OrthographicLens

import util442

# adjust pendulum initial conditions 
#############################################################
L = 1
theta_zero = 0.0
thetadot_zero = 0.0
#############################################################


class Lab5(ShowBase):
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
        
        self.camera.setPos(0, -10, 0)
        self.camLens=OrthographicLens()
        self.camLens.setFilmSize( 44,33) # Or whatever size you want
        self.cam.node().setLens(self.camLens)
        # This code puts the standard title and instruction text on screen
        self.title = OnscreenText(text=__class__.__name__,
                     style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.07,
                     parent=base.a2dBottomRight, align=TextNode.ARight)


        self.theta=theta_zero
        self.thetadot=thetadot_zero

        self.accept('a', self.leftForce)
        self.accept('d', self.rightForce)


        self.pendulum=render.attachNewNode(util442.make_pendulum(1,L*10))
        self.mainLoop = taskMgr.add(self.simulationLoop, "simulationLoop")
        
    def leftForce(self):
        self.thetadot = self.thetadot - 5.0*0.1
    def rightForce(self):
        self.thetadot = self.thetadot + 5.0*0.1

    def simulationLoop(self, task):
        # Standard technique for finding the amount of time since the last frame
        dt = globalClock.getDt()
        if dt > 1.0: dt = 0.0
        simulationIteration(self,dt)
        return Task.cont


def simulationIteration(self, dt):
 

    # write code to implment the pendulum initial conditions 
    #############################################################

    self.theta = 0.0
    self.thetadot = 0.0


    #############################################################

    self.pendulum.setHpr(0.0, 0.0, -self.theta*180.0/3.14159 )
    self.pendulum.setPos(L * 10.0 * sin(self.theta), 0.0, 15.0 - L * 10.0 * cos(self.theta))



simulation=Lab5()
simulation.run()