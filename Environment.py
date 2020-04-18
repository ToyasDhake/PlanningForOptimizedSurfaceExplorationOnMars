from copy import deepcopy

img = []
with open("map.txt", "r") as file:
    for line in file:
        line = line
        row = line.split(",")
        row = list(map(int, row))
        img.append(row)

class Node:
    # Initialize
    def __init__(self, env, parent=None, action=None):
        self.env = env
        self.parent = parent
        self.action = action

    def path(self):
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        yield from reversed(p)

class Environment:
    def __init__(self, currentPosition, wheelClearance=5):
        self.currentPosition = currentPosition
        self.wheelClearance = wheelClearance

    def checkPosition(self, val):
        global img
        temp = deepcopy(self)
        if val == 'U':
            temp.currentPosition[1] += 1
        elif val == 'D':
            temp.currentPosition[1] -= 1
        elif val == 'R':
            temp.currentPosition[0] += 1
        elif val == 'L':
            temp.currentPosition[0] -= 1
        elif val == 'UL':
            temp.currentPosition[0] -= 1
            temp.currentPosition[1] += 1
        elif val == 'UR':
            temp.currentPosition[0] += 1
            temp.currentPosition[1] += 1
        elif val == 'DL':
            temp.currentPosition[0] -= 1
            temp.currentPosition[1] -= 1
        elif val == 'DR':
            temp.currentPosition[0] += 1
            temp.currentPosition[1] -= 1
        if abs(img[temp.currentPosition[0]][temp.currentPosition[1]] - img[self.currentPosition[0]][self.currentPosition[1]]) > self.wheelClearance:
            return True
        else:
            return False

    def possibleMoves(self):
        moves = []
        if self.currentPosition[2] == "U":
            moves += ["DL","D","DR"]
        elif self.currentPosition[2] == "D":
            moves += ["UL","U","UR"]
        elif self.currentPosition[2] == "R":
            moves += ["UL","L","DL"]
        elif self.currentPosition[2] == "L":
            moves += ["UR","R","DR"]
        elif self.currentPosition[2] == "UR":
            moves += ["L","DL","D"]
        elif self.currentPosition[2] == "UL":
            moves += ["D","DR","R"]
        elif self.currentPosition[2] == "DR":
            moves += ["U","UL","L"]
        elif self.currentPosition[2] == "DL":
            moves += ["U","UR","R"]
        for i in moves:
            if self.checkPosition(i):
                moves.remove(i)

    def move(self, val):
        temp = deepcopy(self)
        if val == 'U':
            temp.currentPosition[1] += 1
        if val == 'D':
            temp.currentPosition[1] -= 1
        if val == 'R':
            temp.currentPosition[0] += 1
        if val == 'L':
            temp.currentPosition[0] -= 1
        if val == 'UL':
            temp.currentPosition[0] -= 1
            temp.currentPosition[1] += 1
        if val == 'UR':
            temp.currentPosition[0] += 1
            temp.currentPosition[1] += 1
        if val == 'DL':
            temp.currentPosition[0] -= 1
            temp.currentPosition[1] -= 1
        if val == 'DR':
            temp.currentPosition[0] += 1
            temp.currentPosition[1] -= 1
        return temp