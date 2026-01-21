#!/usr/bin/env python

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

MAX_TREES = 2000

class Lab2(ShowBase):
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
        self.camLens.setFilmSize( 44, 33) # Or whatever size you want
        self.cam.node().setLens(self.camLens)
        # This code puts the standard title and instruction text on screen
        self.title = OnscreenText(text=__class__.__name__,
                     style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.07,
                     parent=base.a2dBottomRight, align=TextNode.ARight)

        self.trees = []
        self.x=[]
        self.y=[]
        self.time = 0.0
        for i in range(0,MAX_TREES):
                self.trees.append(render.attachNewNode(util442.make_redgreentree(0.4)))
                self.trees[-1].setTwoSided(True)
                self.x.append(random.uniform(-15,15))
                self.y.append(random.uniform(-15,15))

        self.mainLoop = taskMgr.add(self.simulationLoop, "simulationLoop")
    def simulationLoop(self, task):
        # Standard technique for finding the amount of time since the last frame
        dt = globalClock.getDt()
        self.time += dt
        if self.time >= 0.1: # run simulation 10 frames per second
            self.time = 0.0
            simulationIteration(self.trees, self.x, self.y)
        return Task.cont





saplings = 500
mature_trees = 500

def simulationIteration(trees, x, y):
    global saplings
    global mature_trees

    #############################################################
    #     
    # Write code to update the number of saplings and mature trees.
    #
    # Note that saplings and mature_trees are already defined and 
    # initialized but you'll need to update them.
    #
    # Define variables for the remaining 4 elements from Step 1.
    #
    # Assume this code gets run once for each year in the forest.
    #
    # your code here
    #
    #############################################################

    number_of_trees = saplings + mature_trees
    # loop to draw the trees 
    for i in range(0,MAX_TREES):
            if i < saplings:
                trees[i].setHpr(180,0,0) # for saplings, green side forward
                trees[i].setPos(x[i],0,y[i])
            elif i < number_of_trees:
                trees[i].setHpr(0,0,0) # for mature trees, red side forward
                trees[i].setPos(x[i],0,y[i])
            else:
                trees[i].setPos(0,1000,0) # hide any extra tree objects offscreen


simulation=Lab2()
simulation.run()