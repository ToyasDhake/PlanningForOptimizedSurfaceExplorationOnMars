#!/usr/bin/env python
from copy import deepcopy
from math import sqrt, cos, sin, atan2

img = []
with open("/home/toyas/catkin_ws/src/PlanningForOptimizedSurfaceExplorationOnMars/scripts/RRTStar/map.txt", "r") as file:
    for line in file:
        line = line
        row = line.split(",")
        row = list(map(int, row))
        img.append(row)

class Node:
    # Initialize
    def __init__(self, env, stepSize,  parent=None):
        self.env = env
        self.parent = parent
        self.distance = 0
        if parent != None:
            self.costToCome = parent.costToCome + stepSize
        else:
            self.costToCome = 0
    def updateDistance(self, x, y):
        self.distance = sqrt((self.env[0] - x) ** 2 + (self.env[1] - y) ** 2)

    def path(self):
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        return reversed(p)

class Environment:

    def __init__(self, stepSize, dimension, wheelClearance=2):
        self.stepSize= stepSize
        self.wheelClearance = wheelClearance
        self.dimension = dimension

    def checkPosition(self, start, angle):
        valid = True
        for i in range(1, self.stepSize*3):


            new = [int(start[0] + i * cos(angle)), int(start[1] + i * sin(angle))]
            old = [int(start[0] + (i-1) * cos(angle)), int(start[1] + (i-1) * sin(angle))]
            if old[0] < 0 or old[1] < 0 or old[0] >= self.dimension[0] or old[1] >= self.dimension[1]:
                return False
            if new[0] < 0 or new[1] < 0 or new[0] >= self.dimension[0] or new[1] >= self.dimension[1]:
                return False
            if abs(img[new[1]][new[0]] - img [old[1]][old[0]]) > self.wheelClearance:
                valid = False
        return valid

    def checkConnection(self, start, end):
        angle = atan2(end[1] - start[1], end[0] - start[0])
        return  self.checkPosition(start, angle)

    def checkParent(self, parent, child):
        if parent.parent is not None and child.parent is not None:
            angle = abs(abs(atan2(parent.env[0]-parent.parent.env[0], parent.env[1]-parent.parent.env[1]))-abs(atan2(child.env[0] - child.parent.env[0], child.env[1] - child.parent.env[1])))
            if angle > 60:
                return False
            else:
                return True
        else:
            return True

