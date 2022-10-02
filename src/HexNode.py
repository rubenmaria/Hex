import math as m
import copy as c

class HexNode:

    def __init__(self, node_type, x, y, color="white"):
        self.nodeType = node_type
        self.color = color
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

    def set_color(self, node_type, color):
        self.color = color
        self.nodeType = node_type
        if node_type == "enemy":
            self.weight = m.inf
        elif node_type == "friendly":
            self.weight = 0
        elif node_type == "impartial":
            self.weight = 1

    def __lt__(self, other):
        return self.distance < other.distance

    def __gt__(self, other):
        return self.distance > other.distance

    def __le__(self, other):
        return self.distance <= other.distance

    def __ge__(self, other):
        return self.distance >= other.distance

    def copy(self):
        copy = c.copy(self)
        copy.weight = c.deepcopy(self.weight)
        copy.nodeType = c.deepcopy(self.nodeType)
        copy.distance = c.deepcopy(self.distance)
        copy.color = c.deepcopy(self.color)
        return copy

    def print(self):
        print("nodeType = ", self.nodeType, "\n")
        print("position =  x= ", self.x, " y= ", self.y, "\n")
        print("weight = ", self.weight, "\n")
        print("distance = ", self.distance, "\n")
