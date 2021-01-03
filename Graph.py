import math as m
import operator
import collections


class Vertex:
    def __init__(self, node_id):
        self.id = node_id
        self.adjacent = {}
        self.distance = m.inf

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_weight(self, neighbor, weight):
        self.adjacent[neighbor] = weight

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def remove_neighbor(self, neighbour):
        del self.adjacent[neighbour]

    def __gt__(self, other):
        return self.distance > other.distance

    def __lt__(self, other):
        return not self.__gt__(other)

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node_id):
        if node_id in self.vert_dict:
            return
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node_id)
        self.vert_dict[node_id] = new_vertex
        return new_vertex

    def get_vertex(self, node_id):
        if node_id in self.vert_dict:
            return self.vert_dict[node_id]
        else:
            return None

    def add_edge(self, frm, to, cost=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        # self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost) undirected

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_connection_weight(self, to_id, weight):
        #print(to_id)
        vert = self.get_vertex(to_id)
        connects = vert.get_connections()
        for con in connects:
            con.set_weight(vert, weight)

    def delete_vertex(self, node_id):
        vert = self.get_vertex(node_id)
        conns = vert.get_connections()
        for con in conns:
            con.remove_neighbor(node_id)
        del self.vert_dict[node_id]

    def add_enemy(self, node_id):
        self.set_connection_weight(node_id, m.inf)

    def add_friendly(self, node_id):
        self.set_connection_weight(node_id, 0)

    def add_neutral(self, node_id, weight=1):
        self.set_connection_weight(node_id, weight)

    def sort_vertices(self):
        self.vert_dict = collections.OrderedDict(sorted(self.vert_dict.items()))
