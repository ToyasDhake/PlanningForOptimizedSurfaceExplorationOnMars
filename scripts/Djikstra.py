
from Environment import Node
from Environment import Environment

# Dijkstra class is called to solve for path using Dijkstra
class Dijkstra:

    # Initiation method
    def __init__(self, start, goal, clearance):
        self.start = start
        self.goal = goal
        self.clearance = clearance

    # Method to solve a Dijkstra object
    def solve(self):
        search = []

        # Set current node to start and add start node to the node list and node search dictionary
        CurrentNode = Node(self.start)
        NodeList = [CurrentNode]
        NodeDict = {tuple(CurrentNode.env)}

        # Check if the current node is the goal node
        while CurrentNode.env != self.goal:
            # Keep checking if there are nodes in list
            if len(NodeList) > 0:
                # Set current node to the first node in the list and then delete from list
                CurrentNode = NodeList.pop()
                search.append(CurrentNode.env)
                Course = Environment(CurrentNode.env, self.clearance)
                # Check all of the possible actions
                for action in Course.possibleMoves():
                    temp = Course.move(action)
                    tempNode = Node(temp.currentPosition, CurrentNode, action)
                    # Search dictonary and add node to list and dictionary if it hasn't been explored yet
                    if tuple(tempNode.env) not in NodeDict:
                        NodeList.append(tempNode)
                        NodeDict.add(tuple(tempNode.env))
                # Sort list of nodes based on cost
                NodeList.sort(key=lambda x: x.weight, reverse=True)
            else:
                return -1, CurrentNode.path(), search

        # solve for path
        x = CurrentNode.path()
        path = []
        for node in x:
            path.append(node.env)
        return path, search