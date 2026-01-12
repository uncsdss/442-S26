#!/usr/bin/env python

# simple example of how to draw a cube using Panda's Geom Interface.

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *

from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import GeomNode, TextNode, LVector3
import sys
import os

base = ShowBase()
base.disableMouse()
base.camera.setPos(0, -10, 0)

title = OnscreenText(text="Lab1: Test of Panda3D",
                     style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.07,
                     parent=base.a2dBottomRight, align=TextNode.ARight)

spaceEvent = OnscreenText(text="Press a: Rotate Cube Right",
                          style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.14),
                          align=TextNode.ALeft, scale=.05,
                          parent=base.a2dTopLeft)
upDownEvent = OnscreenText(text="Press s: Rotate Cube Left",
                           style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.20),
                           align=TextNode.ALeft, scale=.05,
                           parent=base.a2dTopLeft)

spaceEvent = OnscreenText(text="Press w: Rotate Cube Up",
                          style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.26),
                          align=TextNode.ALeft, scale=.05,
                          parent=base.a2dTopLeft)
upDownEvent = OnscreenText(text="Press d: Rotate Cube Down",
                           style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.32),
                           align=TextNode.ALeft, scale=.05,
                           parent=base.a2dTopLeft)

# You can't normalize inline so this is a helper function
def normalized(*args):
    myVec = LVector3(*args)
    myVec.normalize()
    return myVec

# helper function to make a square given the Lower-Left-Hand and
# Upper-Right-Hand corners

def makeSquare(x1, y1, z1, x2, y2, z2, r, g, b):
    format = GeomVertexFormat.getV3n3cpt2()
    vdata = GeomVertexData('square', format, Geom.UHDynamic)

    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    color = GeomVertexWriter(vdata, 'color')

    # make sure we draw the sqaure in the right plane
    if x1 != x2:
        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y1, z1)
        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y2, z2)

        normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y1 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z2 - 1))
        normal.addData3(normalized(2 * x1 - 1, 2 * y2 - 1, 2 * z2 - 1))

    else:
        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y2, z1)
        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y1, z2)

        normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z2 - 1))
        normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z2 - 1))

    # adding different colors to the vertex for visibility
    color.addData4f(r, g, b, 1.0)
    color.addData4f(r, g, b, 1.0)
    color.addData4f(r, g, b, 1.0)
    color.addData4f(r, g, b, 1.0)

    # Quads aren't directly supported by the Geom interface
    tris = GeomTriangles(Geom.UHDynamic)
    tris.addVertices(0, 1, 3)
    tris.addVertices(1, 2, 3)

    square = Geom(vdata)
    square.addPrimitive(tris)
    return square

# Note: it isn't particularly efficient to make every face as a separate Geom.
# instead, it would be better to create one Geom holding all of the faces.
square0 = makeSquare(-1, -1, -1, 1, -1, 1, 1, 0, 0,)
square1 = makeSquare(-1, 1, -1, 1, 1, 1, 0, 1, 0)
square2 = makeSquare(-1, 1, 1, 1, -1, 1, 0, 0, 1)
square3 = makeSquare(-1, 1, -1, 1, -1, -1, 1, 1, 0)
square4 = makeSquare(-1, -1, -1, -1, 1, 1, 0,1,1)
square5 = makeSquare(1, -1, -1, 1, 1, 1, 1, 0, 1)
snode = GeomNode('square')
snode.addGeom(square0)
snode.addGeom(square1)
snode.addGeom(square2)
snode.addGeom(square3)
snode.addGeom(square4)
snode.addGeom(square5)

cube = render.attachNewNode(snode)
cube.setHpr(0.0, 0, 0)

# OpenGl by default only draws "front faces" (polygons whose vertices are
# specified CCW).
cube.setTwoSided(True)

class MyTapper(DirectObject):
    def __init__(self):
        self.accept("a", self.rotateCubeRight)
        self.accept("s", self.rotateCubeLeft)
        self.accept("w", self.rotateCubeUp)
        self.accept("d", self.rotateCubeDown)   
        self.Angle1 = 0.0
        self.Angle2 = 0.0

    def rotateCubeRight(self):
        global cube
        self.Angle1 -= 5.0
        cube.setHpr(self.Angle1, self.Angle2, 0)

    def rotateCubeLeft(self):
        global cube
        self.Angle1 += 5.0
        cube.setHpr(self.Angle1, self.Angle2, 0)

    def rotateCubeUp(self):
        global cube
        self.Angle2 -= 5.0
        cube.setHpr(self.Angle1, self.Angle2, 0)

    def rotateCubeDown(self):
        global cube
        self.Angle2 += 5.0
        cube.setHpr(self.Angle1, self.Angle2, 0)

t = MyTapper()
base.run()
