#!/usr/bin/env python
from math import sqrt, cos, sin, radians, atan2, floor

# Read map
img = []
with open("/home/toyas/catkin_ws/src/PlanningForOptimizedSurfaceExplorationOnMars/scripts/Dijkstra/map.txt", "r") as file:
    for line in file:
        line = line
        row = line.split(",")
        row = list(map(int, row))
        img.append(row)

class Node:
    # Initialize
    def __init__(self,start,  env, goal, stepSize, parent=None):
        self.env = env
        self.parent = parent
        self.goal = goal
        if parent is not None:
            self.g = parent.g + stepSize
        else:
            self.g = 0
        # Heuristic function
        self.weight = self.g 

    # Solve for path from goal to start node
    def path(self):
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        return reversed(p)

    # Get possible actions
    def actions(self):
        if self.action is None:
            return self.env.possibleMoves()
        else:
            return self.env.possibleMoves(self.action)


class Environment:
    # Initialize
    def __init__(self, currentPosition, clearance):
        self.currentPosition = currentPosition
        self.clearance = clearance

    def possiblePostion(self, new, old):
        global img
        if old[0] < 0 or old[1] < 0 or old[0] >= 511 or old[1] >= 511:
            return False
        if new[0] < 0 or new[1] < 0 or new[0] >= 511 or new[1] >= 511:
            return False
        if abs(img[int(new[1])][int(new[0])] - img[int(old[1])][int(old[0])]) > self.clearance:
            return False
        else:
            return True
    # Check if each action is possible
    def possibleMoves(self, start, node, stepSize):
        actions = []
        temp = self.move(start, '1', stepSize, node)
        if temp is not None:
            actions.append(temp)
        temp = self.move(start, '2', stepSize, node)
        if temp is not None:
            actions.append(temp)
        temp = self.move(start, '3', stepSize, node)
        if temp is not None:
            actions.append(temp)
        temp = self.move(start, '4', stepSize, node)
        if temp is not None:
            actions.append(temp)
        temp = self.move(start, '5', stepSize, node)
        if temp is not None:
            actions.append(temp)
        return actions

    # Move robot position according to action
    def move(self, start, val, stepSize, node):
        temp = None
        if val == '1':
            angle = self.currentPosition[2] + 60
            angle = self.angleCheck(angle)
            tempBoolean = True
            for i in range(1, stepSize):
                xOld = self.currentPosition[0] + (i - 1) * cos(radians(angle))
                yOld = self.currentPosition[1] + (i - 1) * sin(radians(angle))
                x = self.currentPosition[0] + i * cos(radians(angle))
                y = self.currentPosition[1] + i * sin(radians(angle))
                if not self.possiblePostion([x, y], [xOld, yOld]):
                    tempBoolean = False
            if tempBoolean:
                x = self.currentPosition[0] + stepSize * cos(radians(angle))
                y = self.currentPosition[1] + stepSize * sin(radians(angle))
                temp = Node(start, [x, y, angle], node.goal, stepSize, node)
        if val == '2':
            angle = self.currentPosition[2] + 30
            angle = self.angleCheck(angle)
            tempBoolean = True
            for i in range(1, stepSize):
                xOld = self.currentPosition[0] + (i-1) * cos(radians(angle))
                yOld = self.currentPosition[1] + (i-1) * sin(radians(angle))
                x = self.currentPosition[0] + i * cos(radians(angle))
                y = self.currentPosition[1] + i * sin(radians(angle))
                if not self.possiblePostion([x, y], [xOld, yOld]):
                    tempBoolean = False
            if tempBoolean:
                x = self.currentPosition[0] + stepSize * cos(radians(angle))
                y = self.currentPosition[1] + stepSize * sin(radians(angle))
                temp = Node(start, [x, y, angle], node.goal, stepSize, node)
        if val == '3':
            angle = self.currentPosition[2]
            angle = self.angleCheck(angle)
            tempBoolean = True
            for i in range(1, stepSize):
                xOld = self.currentPosition[0] + (i - 1) * cos(radians(angle))
                yOld = self.currentPosition[1] + (i - 1) * sin(radians(angle))
                x = self.currentPosition[0] + i * cos(radians(angle))
                y = self.currentPosition[1] + i * sin(radians(angle))
                if not self.possiblePostion([x, y], [xOld, yOld]):
                    tempBoolean = False
            if tempBoolean:
                x = self.currentPosition[0] + stepSize * cos(radians(angle))
                y = self.currentPosition[1] + stepSize * sin(radians(angle))
                temp = Node(start, [x, y, angle], node.goal, stepSize, node)
        if val == '4':
            angle = self.currentPosition[2] - 30
            angle = self.angleCheck(angle)
            tempBoolean = True
            for i in range(1, stepSize):
                xOld = self.currentPosition[0] + (i - 1) * cos(radians(angle))
                yOld = self.currentPosition[1] + (i - 1) * sin(radians(angle))
                x = self.currentPosition[0] + i * cos(radians(angle))
                y = self.currentPosition[1] + i * sin(radians(angle))
                if not self.possiblePostion([x, y], [xOld, yOld]):
                    tempBoolean = False
            if tempBoolean:
                x = self.currentPosition[0] + stepSize * cos(radians(angle))
                y = self.currentPosition[1] + stepSize * sin(radians(angle))
                temp = Node(start, [x, y, angle], node.goal, stepSize, node)
        if val == '5':
            angle = self.currentPosition[2] - 60
            angle = self.angleCheck(angle)
            tempBoolean = True
            for i in range(1, stepSize):
                xOld = self.currentPosition[0] + (i - 1) * cos(radians(angle))
                yOld = self.currentPosition[1] + (i - 1) * sin(radians(angle))
                x = self.currentPosition[0] + i * cos(radians(angle))
                y = self.currentPosition[1] + i * sin(radians(angle))
                if not self.possiblePostion([x, y], [xOld, yOld]):
                    tempBoolean = False
            if tempBoolean:
                x = self.currentPosition[0] + stepSize * cos(radians(angle))
                y = self.currentPosition[1] + stepSize * sin(radians(angle))
                temp = Node(start, [x, y, angle], node.goal, stepSize, node)
        return temp

    # Keep angle value from 0 to 360
    def angleCheck(self, angle):
        if angle >= 360:
            angle -= 360
        if angle < 0:
            angle = 360 + angle
        return angle
