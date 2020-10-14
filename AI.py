import copy
import math as m
from HexNode import HexNode


class Ai:
    def __init__(self, board):
        self.__board = board
        self.__visited_b = set()
        self.__visited_r = set()
        self.__graph = [[HexNode for j in range(13)] for i in range(13)]
        self.__to_examine_red_d = set()
        self.__to_examine_blue_d = set()
        self.__destination_distance_b = list()
        self.__destination_distance_r = list()

    def __write_distance(self, tile, distance):
        if tile.text == "":
            tile.add_text(str(distance), self.__board.canvas, 'black')

    def __setup_dijkstra_blue(self):
        self.__visited_b.clear()
        self.__to_examine_blue_d.clear()
        for x in range(13):
            for y in range(13):
                if (x == 0 or x == 12) and (y == 0 or y == 12):
                    self.__graph[x][y] = HexNode("wall", x, y)
                elif x == 0:
                    self.__graph[x][y] = HexNode("source", x, y)
                    self.__to_examine_blue_d.add(HexNode("source", x, y))
                elif x == 12:
                    self.__graph[x][y] = HexNode("destination", x, y)
                elif y == 0 or y == 12:
                    self.__graph[x][y] = HexNode("wall", x, y)
                else:
                    x_tile = x - 1
                    y_tile = y - 1
                    if self.__board.tiles[x_tile][y_tile].fillColor == "blue":
                        self.__graph[x][y] = HexNode("friendly", x, y)
                    elif self.__board.tiles[x_tile][y_tile].fillColor == "red":
                        self.__graph[x][y] = HexNode("enemy", x, y)
                    else:
                        self.__graph[x][y] = HexNode("impartial", x, y)

    def hex_dijkstra_b(self):
        vertex_amount = self.__board.rowLength * self.__board.columnLength
        self.__setup_dijkstra_blue()

        while len(self.__visited_b) < vertex_amount:
            node = self.get_min_dist_node(self.__to_examine_blue_d)
            self.__to_examine_blue_d.remove(node)
            self.__visited_b.add(node)
            self.__update_dist_of_neighbour_b(node)

        min_distance = m.inf

        for distance in self.__destination_distance_b:
            if min_distance > distance:
                min_distance = distance

        return min_distance

    def __update_dist_of_neighbour_b(self, node):
        x = node.x
        y = node.y
        neighbour_positions = list()
        neighbour_positions.append((x, y - 1))
        neighbour_positions.append((x + 1, y - 1))
        neighbour_positions.append((x + 1, y))
        neighbour_positions.append((x, y + 1))
        for n_pos in neighbour_positions:
            row = n_pos[0]
            col = n_pos[1]
            neighbour_node = self.__graph[row][col]
            if row < 0 or row > 12:
                continue
            if col < 0 or col > 12:
                continue
            if ((neighbour_node.nodeType == "impartial" or neighbour_node.nodeType == "friendly")
                    and not (neighbour_node in self.__visited_b)
                    and neighbour_node.weight + node.distance < neighbour_node.distance):
                neighbour_node.distance = neighbour_node.weight + node.distance
                self.__to_examine_blue_d.add(neighbour_node)
                tile = self.__board.tiles[row - 1][col - 1]
                # self.__write_distance(tile, neighbour_node.distance)
            if neighbour_node.nodeType == "destination":
                self.__destination_distance_b.append(node.distance)

    def get_min_dist_node(self, to_examine):
        min_number = m.inf
        min_node = None
        for node in to_examine:
            if node.distance < min_number and node not in self.__visited_b:
                min_number = node.distance
                min_node = node
        return min_node

    def __setup_dijkstra_r(self):
        self.__visited_r.clear()
        self.__to_examine_red_d.clear()
        for x in range(13):
            for y in range(13):
                if (x == 0 or x == 12) and (y == 0 or y == 12):
                    self.__graph[x][y] = HexNode("wall", x, y)
                elif y == 0:
                    self.__graph[x][y] = HexNode("source", x, y)
                    self.__to_examine_red_d.add(HexNode("source", x, y))
                elif y == 12:
                    self.__graph[x][y] = HexNode("destination", x, y)
                elif x == 0 or x == 12:
                    self.__graph[x][y] = HexNode("wall", x, y)
                else:
                    x_tile = x - 1
                    y_tile = y - 1
                    if self.__board.tiles[x_tile][y_tile].fillColor == "red":
                        self.__graph[x][y] = HexNode("friendly", x, y)
                    elif self.__board.tiles[x_tile][y_tile].fillColor == "blue":
                        self.__graph[x][y] = HexNode("enemy", x, y)
                    else:
                        self.__graph[x][y] = HexNode("impartial", x, y)

    def hex_dijkstra_r(self):
        vertex_amount = self.__board.rowLength * self.__board.columnLength
        self.__setup_dijkstra_r()
        while len(self.__visited_r) < vertex_amount:
            node = self.get_min_dist_node(self.__to_examine_red_d)
            self.__to_examine_red_d.remove(node)
            self.__visited_r.add(node)
            self.__update_dist_of_neighbour_r(node)
        min_distance = m.inf

        for distance in self.__destination_distance_r:
            if min_distance > distance:
                min_distance = distance
        return min_distance

    def __update_dist_of_neighbour_r(self, node):
        x = node.x
        y = node.y
        neighbour_positions = list()
        neighbour_positions.append((x - 1, y))
        neighbour_positions.append((x + 1, y))
        neighbour_positions.append((x - 1, y + 1))
        neighbour_positions.append((x, y + 1))
        for n_pos in neighbour_positions:
            row = n_pos[0]
            col = n_pos[1]
            neighbour_node = self.__graph[row][col]
            if row < 0 or row > 12:
                continue
            if col < 0 or col > 12:
                continue
            if ((neighbour_node.nodeType == "impartial" or neighbour_node.nodeType == "friendly")
                    and not (neighbour_node in self.__visited_b)
                    and neighbour_node.weight + node.distance < neighbour_node.distance):
                neighbour_node.distance = neighbour_node.weight + node.distance
                self.__to_examine_red_d.add(neighbour_node)
                tile = self.__board.tiles[row - 1][col - 1]
                # self.__write_distance(tile, neighbour_node.distance)
            if neighbour_node.nodeType == "destination":
                self.__destination_distance_r.append(node.distance)

    def get_value_red(self):
        red = self.hex_dijkstra_r()
        blue = self.hex_dijkstra_b()
        return red - blue

    def get_value_blue(self):
        red = self.hex_dijkstra_r()
        blue = self.hex_dijkstra_b()
        return blue - red
