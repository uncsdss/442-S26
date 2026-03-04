#!/usr/bin/env python

from math import cos, sin, sqrt
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


# pendulum initial conditions 
L = 1.0
mass = 1
theta_zero = 0.0
thetadot_zero = 0.3

SAMPLE_TIME = 0.01

class Lab7_4(ShowBase):
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


        self.accept('a', self.leftTorque)
        self.accept('d', self.rightTorque)
        self.accept('0', self.setMode0)
        self.accept('1', self.setMode1)
        self.accept('r', self.reset)

        self.pendulum=render.attachNewNode(util442.make_pendulum(1,L*10))
        self.floor=render.attachNewNode(util442.make_floor(20.0))
        self.timeText = OnscreenText(text="Time:" + str(globalClock.getFrameTime()), pos=(-0.8, -0.77), scale=0.17)
        self.errorText = OnscreenText(text="Total Error: " + str(0.0), pos=(0.6, -0.77), scale=0.17)
        self.scoreText = OnscreenText(text="Score: " + str(0.0), pos=(0.0, -0.95), scale=0.12)
        self.reset()
        self.mainLoop = taskMgr.add(self.simulationLoop, "simulationLoop")
    def leftTorque(self):
        self.thetadot = self.thetadot + 5.0*0.1
    def rightTorque(self):
        self.thetadot = self.thetadot - 5.0*0.1
    def setMode0(self):
        self.mode=0
        globalClock.reset()
    def setMode1(self):
        self.mode=1
        globalClock.reset()
    def sense_theta(self):
        # add some noise to the measurement to make it more realistic
        noise =  random.gauss(0.0, 0.01)
        return self.theta + noise

    def reset(self):
        self.theta=theta_zero
        self.thetadot=thetadot_zero
        self.mode=0
        self.error_score=0.0
        self.error_previous=0.0
        globalClock.reset()
        self.timeText.setText("Time: " + str(0.0))
        self.errorText.setText("Total Error: " + str(0.0))
        self.scoreText.setText("Score: " + str(0.0))
        self.dt=0.0

    def simulationLoop(self, task):
        # Standard technique for finding the amount of time since the last frame
        dt = globalClock.getDt()
        if dt > 1.0: dt = 0.0
        self.dt = self.dt + dt
        if (self.dt>SAMPLE_TIME):
            simulationIteration(self,self.dt)
            self.dt=0.0
        return Task.cont


def simulationIteration(self, dt):
    if (self.mode!=0):

        # simulation

        # simulate a reference signal that changes every 5 seconds between -0.4, 0, and 0.4 radians
        theta_reference = (((int(globalClock.getFrameTime()/5.0)+1)%3)-1)*0.4

        #################################
        # compute control input
        # You may use self.theta and self.thetadot as needed
        # 
        theta = self.sense_theta()
        error = 0.0
          
        Kp = 100.0
        Kd = 20.0

        u = 0.0 # compute control input using a simple proportional and derivative controller
        ###############################

        # limit the control input to be within some bounds like in a real system
        umax = 10.0*mass*L*L
        if (u>umax): 
            u=umax
        elif (u<-umax): 
            u=-umax

        # simulate the pendulum forward in time by dt using semi-implicit Euler integration
        accel =  9.81/L * (self.theta) + u / (mass * L * L) # compute acceleration at the beginning of the time step

        # semi-implicit Euler integration
        self.thetadot = self.thetadot +  accel* dt # update velocity using the current acceleration
        self.theta = self.theta + self.thetadot*dt # update position using the new velocity

    
        # if the pendulum goes beyond horizontal stop the simulation
        if self.theta>3.14159/2:
            self.mode=0
        elif self.theta<-3.14159/2:
            self.mode=0
        elif self.mode!=0:
            # update the time and total error text
            self.error_score += abs(error)*dt
            t=globalClock.getFrameTime()
            self.timeText.setText("Time: " + str(round(t, 1)))
            self.errorText.setText("Total Error: " + str(round(self.error_score*180.0/3.14159, 1)))
            self.scoreText.setText("Kp=" + str(Kp) + "  Kd=" + str(Kd) + "  Score:" + str(round(self.error_score*180.0/3.14159/t, 1)))

    # draw the pendulum and floor
    self.pendulum.setHpr(0.0, 0.0, 180+ -self.theta*180.0/3.14159 )
    self.pendulum.setPos(L * 10.0 * sin(-self.theta), 0.0, -10.0 + L * 10.0 * cos(self.theta))
    self.floor.setPos(0.0, 0.0, -10.0)
 
simulation=Lab7_4()
simulation.run()