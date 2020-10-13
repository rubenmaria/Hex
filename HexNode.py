import math as m


class HexNode:

    def __init__(self, node_type, x, y):
        self.nodeType = node_type
        self.x = x
        self.y = y
        self.weight = 0
        self.distance = m.inf
        if node_type == "source":
            self.weight = 0
            self.distance = 0
        elif node_type == "friendly" or node_type == "destination":
            self.weight = 0
        elif node_type == "enemy" or node_type == "wall":
            self.weight = m.inf
        elif node_type == "impartial":
            self.weight = 1
        else:
            raise ValueError("not a valid node Type!")

    def print(self):
        print("nodeType = ", self.nodeType, "\n")
        print("position =  x= ", self.x, " y= ", self.y, "\n")
        print("weight = ", self.weight, "\n")
        print("distance = ", self.distance, "\n")
