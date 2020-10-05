import math as m
from Hexagon import Hexagon


class Board:

    def __init__(self, offset_x, offset_y, width, canvas):
        self.tiles = [[]]
        self.canvas = canvas
        self.tiles = [[Hexagon for j in range(11)] for i in range(11)]
        self.rowLength = 11
        self.columnLength = 11
        self.__edges = []
        self.__offset_x = offset_x
        self.__offset_y = offset_y
        self.width = width
        self.__init_drawable_board(canvas)
        self.__hexagonWidth = width / 13
        self.__radiusHexagon = (self.__hexagonWidth / 2) / m.cos(m.radians(30))
        self.__lineEdgeWidth = 19 * self.__hexagonWidth
        delta_y = self.__radiusHexagon
        self.lineEdgeHeight = 20 * delta_y
        self.width = self.__lineEdgeWidth + 10
        self.offsetYRect = self.__offset_y - (delta_y + 4)

    def __init_drawable_board(self, canvas):
        w = self.width / 13
        offset_x = self.__offset_x
        offset_y = self.__offset_y
        r = (w / 2) / m.cos(m.radians(30))
        delta_y = r * m.cos(m.radians(60)) + r
        for col in range(-1, 12):
            y = offset_y + col * delta_y
            for row in range(-1, 12):
                x = offset_x + row * w
                if row == -1 and col == -1 or row == 11 and col == -1:
                    self.__edges.append(Hexagon(w, x, y, 'black', 'black', 3, "edge"))
                elif row == -1 and col == 11 or row == 11 and col == 11:
                    self.__edges.append(Hexagon(w, x, y, 'black', 'black', 3, "edge"))
                elif row == -1 or row == 11:
                    h = Hexagon(w, x, y, 'black', 'blue', 3, "edgeRed")
                    h.add_text("{}".format(col + 1), canvas)
                    self.__edges.append(h)
                elif col == -1 or col == 11:
                    h = Hexagon(w, x, y, 'black', 'red', 3, "edgeBlue")
                    h.add_text(chr(65 + row), canvas)
                    self.__edges.append(h)
                else:
                    self.tiles[row][col] = Hexagon(w, x, y, 'black', 'white', 3, "{}-{}".format(row, col))
            offset_x += w / 2

    def draw(self, canvas):
        for tile_arrays in self.tiles:
            for tiles in tile_arrays:
                tiles.draw(canvas)
        for el in self.__edges:
            el.draw(canvas)

    def clear_board(self, canvas):
        for tile_arrays in self.tiles:
            for tile in tile_arrays:
                tile.set_color(canvas, "white")
                tile.change_text(canvas, '')

    def change_transformable(self, canvas, offset_x, offset_y, width):
        self.width = width
        self.__offset_x = offset_x
        self.__offset_y = offset_y
        w = width / 13
        offset_x = offset_x
        offset_y = offset_y
        r = (w / 2) / m.cos(m.radians(30))
        self.__radiusHexagon = r
        delta_y = r * m.cos(m.radians(60)) + r
        edge_index = 0
        for col in range(-1, 12):
            y = offset_y + col * delta_y
            for row in range(-1, 12):
                x = offset_x + row * w
                if row == -1 and col == -1 or row == 11 and col == -1:
                    self.__edges[edge_index].change_transformable(canvas, w, x, y)
                    edge_index += 1
                elif row == -1 and col == 11 or row == 11 and col == 11:
                    self.__edges[edge_index].change_transformable(canvas, w, x, y)
                    edge_index += 1
                elif row == -1 or row == 11:
                    self.__edges[edge_index].change_transformable(canvas, w, x, y)
                    edge_index += 1
                elif col == -1 or col == 11:
                    self.__edges[edge_index].change_transformable(canvas, w, x, y)
                    edge_index += 1
                else:
                    self.tiles[row][col].change_transformable(canvas, w, x, y)
            offset_x += w / 2