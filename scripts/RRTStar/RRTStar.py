#!/usr/bin/env python
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from random import randint
from math import sqrt, sin, cos, atan2
from Environment import Node, Environment


class RRTStar:
    def __init__(self, start, goal, xDimension, yDimension, numberOfPoints, stepSize, neighbourhoodScale=2):
        self.xDimension = xDimension
        self.yDimension = yDimension
        self.numberOfPoints = numberOfPoints
        self.start = start
        self.goal = goal
        self.stepSize = stepSize
        self.neighbourhoodScale = neighbourhoodScale

    def solve(self):
        environment = Environment(self.stepSize, [self.xDimension, self.yDimension])
        nodes = []
        nodes.append(Node(self.start, self.stepSize))
        goalReached = False
        while not goalReached:
            for _ in range(self.numberOfPoints):
                x = randint(0, self.xDimension - 1)
                y = randint(0, self.yDimension - 1)
                for i in range(len(nodes)):
                    nodes[i].updateDistance(x, y)
                nodes.sort(key=lambda x: x.distance)
                possible = False
                temp = 0
                while not possible and temp < len(nodes):
                    angle = atan2(y - nodes[temp].env[1], x - nodes[temp].env[0])
                    newX = nodes[temp].env[0] + self.stepSize * cos(angle)
                    newY = nodes[temp].env[1] + self.stepSize * sin(angle)
                    possible = environment.checkPosition(nodes[temp].env, angle)
                    temp += 1
                if possible:
                    neighbourhood = []
                    for i in range(len(nodes)):
                        if (newX - nodes[i].env[0]) ** 2 + (newY - nodes[i].env[1]) ** 2 < (
                                self.stepSize * self.neighbourhoodScale) ** 2:
                            neighbourhood.append(nodes[i])
                    neighbourhood.sort(key=lambda x: x.costToCome)
                    nodes.append(Node([newX, newY],
                                      sqrt((newX - neighbourhood[0].env[0]) ** 2 + (newY - neighbourhood[0].env[1]) ** 2),
                                      neighbourhood[0]))

                    for i in range(len(neighbourhood)):
                        for j in range(len(neighbourhood)):
                            if neighbourhood[i].parent is not None:
                                if i != j:
                                    if neighbourhood[i].parent.costToCome + sqrt(
                                            (neighbourhood[i].parent.env[0] - neighbourhood[i].env[0]) ** 2 + (
                                                    neighbourhood[i].parent.env[1] - neighbourhood[i].env[1]) ** 2) > \
                                            neighbourhood[j].costToCome + sqrt(
                                            (neighbourhood[j].env[0] - neighbourhood[i].env[0]) ** 2 + (
                                                    neighbourhood[j].env[1] - neighbourhood[i].env[1]) ** 2):
                                        if environment.checkConnection(neighbourhood[i].parent.env, neighbourhood[j].env):
                                            if environment.checkParent(neighbourhood[i].parent, neighbourhood[j]):
                                                neighbourhood[i].parent = neighbourhood[j]

            for i in range(len(nodes)):
                nodes[i].updateDistance(self.goal[0], self.goal[1])
            nodes.sort(key=lambda x: x.distance)
            if sqrt((nodes[0].env[0]-self.goal[0])**2 + (nodes[0].env[1]-self.goal[1]) ** 2) < 15:
                goalReached = True
            print("Computing...")
        for k in range(len(nodes)):
            neighbourhood = []
            for l in range(len(nodes)):
                if (nodes[l].env[0] - nodes[k].env[0]) ** 2 + (nodes[l].env[1] - nodes[k].env[1]) ** 2 < (
                        self.stepSize * self.neighbourhoodScale) ** 2:
                    neighbourhood.append(nodes[l])
            for i in range(len(neighbourhood)):
                for j in range(len(neighbourhood)):
                    if neighbourhood[i].parent is not None:
                        if i != j:
                            if neighbourhood[i].parent.costToCome + sqrt(
                                    (neighbourhood[i].parent.env[0] - neighbourhood[i].env[0]) ** 2 + (
                                            neighbourhood[i].parent.env[1] - neighbourhood[i].env[1]) ** 2) > \
                                    neighbourhood[
                                        j].costToCome + sqrt(
                                (neighbourhood[j].env[0] - neighbourhood[i].env[0]) ** 2 + (
                                        neighbourhood[j].env[1] - neighbourhood[i].env[1]) ** 2):
                                if environment.checkConnection(neighbourhood[i].parent.env, neighbourhood[j].env):
                                    if environment.checkParent(neighbourhood[i].parent, neighbourhood[j]):
                                        neighbourhood[i].parent = neighbourhood[j]
        return nodes[0].path()
