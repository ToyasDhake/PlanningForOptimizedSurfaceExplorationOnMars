from copy import deepcopy
from math import sqrt, cos, sin

img = []
with open("map.txt", "r") as file:
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
        yield from reversed(p)

class Environment:
    def __init__(self, stepSize, dimension, wheelClearance=250):
        self.stepSize= stepSize
        self.wheelClearance = wheelClearance
        self.dimension = dimension

    def checkPosition(self, start, angle):
        valid = True
        for i in range(1, self.stepSize):
            new = [int(start[0] + i * cos(angle)), int(start[1] + i * sin(angle))]
            old = [int(start[0] + (i-1) * cos(angle)), int(start[1] + (i-1) * sin(angle))]
            if new[0] < 0 or new[1] < 0 or new[0] > self.dimension[0] or new[1] > self.dimension[1]:
                return False
            if abs(img[new[0]][new[1]] - img [old[0]][old[1]]) > self.wheelClearance:
                valid = False
        return valid
