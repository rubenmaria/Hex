import copy
import math as m
from HexNode import HexNode
import copy as c


class VirtualTile:
    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color


class Ai:
    def __init__(self, board, canvas, occupied_tiles):
        self.__board = board
        self.occupied_tiles = occupied_tiles
        self.__visited_b = set()
        self.__visited_r = set()
        self.__graph = [[HexNode for j in range(13)] for i in range(13)]
        self.__destination_length = 10
        self.__visited = set()
        self.__to_examine_red_d = set()
        self.__to_examine_blue_d = set()
        self.__destination_distance_b = list()
        self.__destination_distance_r = list()
        self.moves = list()
        self.moves_score = list()
        self.__canvas = canvas

    def __write_distance(self, tile, distance):
        if tile.text == "":
            tile.add_text(str(distance), self.__board.canvas, 'black')

    def __setup_dijkstra_blue(self, tiles):
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
                    if tiles[x_tile][y_tile].color == "blue":
                        self.__graph[x][y] = HexNode("friendly", x, y)
                    elif tiles[x_tile][y_tile].color == "red":
                        self.__graph[x][y] = HexNode("enemy", x, y)
                    else:
                        self.__graph[x][y] = HexNode("impartial", x, y)

    def hex_dijkstra_b(self, tiles):
        vertex_amount = self.__board.rowLength * self.__board.columnLength
        self.__setup_dijkstra_blue(tiles)

        while len(self.__visited_b) < vertex_amount:
            node = self.get_min_dist_node(self.__to_examine_blue_d)
            if node is None:
                break
            self.__to_examine_blue_d.remove(node)
            self.__visited_b.add(node)
            self.__update_dist_of_neighbour_b(node, tiles)

        min_distance = m.inf

        for distance in self.__destination_distance_b:
            if min_distance > distance:
                min_distance = distance

        return min_distance

    def __update_dist_of_neighbour_b(self, node, tiles):
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

    def __setup_dijkstra_r(self, tiles):
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
                    if tiles[x_tile][y_tile].color == "red":
                        self.__graph[x][y] = HexNode("friendly", x, y)
                    elif tiles[x_tile][y_tile].color == "blue":
                        self.__graph[x][y] = HexNode("enemy", x, y)
                    else:
                        self.__graph[x][y] = HexNode("impartial", x, y)

    def hex_dijkstra_r(self, tiles):
        vertex_amount = self.__board.rowLength * self.__board.columnLength
        self.__setup_dijkstra_r(tiles)
        while len(self.__visited_r) < vertex_amount:
            node = self.get_min_dist_node(self.__to_examine_red_d)
            if node is None:
                break
            self.__to_examine_red_d.remove(node)
            self.__visited_r.add(node)
            self.__update_dist_of_neighbour_r(node, tiles)

        min_distance = m.inf

        for distance in self.__destination_distance_r:
            if min_distance > distance:
                min_distance = distance
        return min_distance

    def __update_dist_of_neighbour_r(self, node, tiles):
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
                tile = tiles[row - 1][col - 1]
                # self.__write_distance(tile, neighbour_node.distance)
            if neighbour_node.nodeType == "destination":
                self.__destination_distance_r.append(node.distance)

    def get_value_red(self, tiles):
        red = self.hex_dijkstra_r(tiles)
        blue = self.hex_dijkstra_b(tiles)
        return blue - red

    def get_value_blue(self, tiles):
        red = self.hex_dijkstra_r(tiles)
        blue = self.hex_dijkstra_b(tiles)
        return red - blue

    def get_active_region(self, occupied_tiles):
        active_region = set()
        neighbour_positions = list()

        for tile in occupied_tiles:
            neighbour_positions.clear()
            x = tile[0]
            y = tile[1]
            neighbour_positions.append((x - 1, y))
            neighbour_positions.append((x + 1, y))
            neighbour_positions.append((x - 1, y + 1))
            neighbour_positions.append((x, y + 1))
            neighbour_positions.append((x - 1, y))
            neighbour_positions.append((x + 1, y - 1))
            neighbour_positions.append((x, y - 1))
            neighbour_positions.append((x, y - 2))
            neighbour_positions.append((x + 1, y - 2))
            neighbour_positions.append((x + 2, y - 2))
            neighbour_positions.append((x + 2, y - 1))
            neighbour_positions.append((x + 2, y))
            neighbour_positions.append((x + 1, y + 1))
            neighbour_positions.append((x, y + 2))
            neighbour_positions.append((x - 1, y + 2))
            neighbour_positions.append((x - 2, y + 2))
            neighbour_positions.append((x - 2, y + 1))
            neighbour_positions.append((x - 2, y))
            neighbour_positions.append((x - 1, y - 1))
            for pos in neighbour_positions:
                if (self.__is_pos_on_board(pos) and pos not in active_region
                        and pos not in occupied_tiles):
                    active_region.add(pos)
        # for t in active_region:
        # tile = self.__board.tiles[t[0]][t[1]]
        # self.__write_distance(tile, 1)
        return active_region

    def __is_pos_on_board(self, position):
        if (position[0] < 0 or position[1] < 0 or
                position[0] > self.__board.rowLength - 1 or
                position[1] > self.__board.columnLength - 1):
            return False
        return True

    def get_value_moves(self, start_color, maximizing):
        tiles = self.get_virtual_tiles()
        color = start_color
        for move in self.moves:
            if color == "red":
                tiles[move[0]][move[1]].color = "red"
                color = "blue"
            else:
                tiles[move[0]][move[1]].color = "blue"
                color = "red"
        if start_color == "red":
            value = self.get_value_red(tiles)
        else:
            value = self.get_value_blue(tiles)
        return value

    def get_region_moves(self):
        moves_set = set(self.moves)
        tiles = moves_set | self.occupied_tiles
        return self.get_active_region(tiles)

    def is_game_over_moves(self, start_color):
        if len(self.moves) + len(self.occupied_tiles) < 21:
            return
        tiles = self.get_virtual_tiles()
        color = start_color
        for move in self.moves:
            if color == "red":
                tiles[move[0]][move[1]].color = "red"
                color = "blue"
            else:
                tiles[move[0]][move[1]].color = "blue"
                color = "red"
        return self.is_red_winner(tiles) or self.is_blue_winner(tiles)

    def minimax(self, color, depth, alpha, beta, maximizing):
        if depth == 0 or self.is_game_over_moves(color):
            val = self.get_value_moves(color, maximizing)
            self.moves.pop()
            if len(self.moves_score) > 1:
                self.moves_score.pop()
            return val

        active_region = self.get_region_moves()
        #print(len(active_region))
        if maximizing:
            max_eval = -m.inf
            for to_examine in active_region:
                self.moves.append(to_examine)
                val = self.minimax(color, depth - 1, alpha, beta, False)
                self.moves_score.append((to_examine, val))
                if depth == 3:
                    print(to_examine, "score= ", val)
                max_eval = max(max_eval, val)
                alpha = max(alpha, val)

                if beta <= alpha:
                    break
            print(self.moves)
            if len(self.moves) > 1:
                self.moves.pop()
            if len(self.moves_score) > 1:
                self.moves_score.pop()
            print("max= ", max_eval)
            return max_eval
        else:
            min_eval = +m.inf
            for to_examine in active_region:
                self.moves.append(to_examine)
                val = self.minimax(color, depth - 1, alpha, beta, True)
                self.moves_score.append((to_examine, val))
                min_eval = min(min_eval, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break
            if len(self.moves) > 1:
                self.moves.pop()
            if len(self.moves_score) > 1:
                self.moves_score.pop()
            print("min= ", min_eval)
            return min_eval

    def is_red_winner(self, tiles):
        for row in range(11):
            self.__visited.clear()
            if self.__is_tile_connected_red(row, 0, tiles):
                self.__visited.clear()
                return True
        self.__visited.clear()
        return False

    def is_blue_winner(self, tiles):
        for col in range(11):
            self.__visited.clear()
            if self.__is_tile_connected_blue(0, col, tiles):
                self.__visited.clear()
                return True
        self.__visited.clear()
        return False

    def __is_tile_connected_red(self, row, col, tiles):
        self.__visited.add((row, col))
        if col > self.__destination_length:
            return True
        if row > self.__destination_length or col < 0 or row < 0:
            return False
        tile = tiles[row][col]
        t_color = tile.color
        if t_color != 'red':
            return False
        if not ((row, col - 1) in self.__visited):
            if self.__is_tile_connected_red(row, col - 1, tiles):
                return True
        if not ((row + 1, col - 1) in self.__visited):
            if self.__is_tile_connected_red(row + 1, col - 1, tiles):
                return True
        if not ((row + 1, col) in self.__visited):
            if self.__is_tile_connected_red(row + 1, col, tiles):
                return True
        if not ((row - 1, col) in self.__visited):
            if self.__is_tile_connected_red(row - 1, col, tiles):
                return True
        if not ((row - 1, col + 1) in self.__visited):
            if self.__is_tile_connected_red(row - 1, col + 1, tiles):
                return True
        if not ((row, col + 1) in self.__visited):
            if self.__is_tile_connected_red(row, col + 1, tiles):
                return True
        return False

    def __is_tile_connected_blue(self, row, col, tiles):
        self.__visited.add((row, col))
        if row > self.__destination_length:
            return True
        if col > self.__destination_length or row < 0 or col < 0:
            return False
        tile = tiles[row][col]
        t_color = tile.color
        if t_color != 'blue':
            return False
        if not ((row, col - 1) in self.__visited):
            if self.__is_tile_connected_blue(row, col - 1, tiles):
                return True
        if not ((row + 1, col - 1) in self.__visited):
            if self.__is_tile_connected_blue(row + 1, col - 1, tiles):
                return True
        if not ((row + 1, col) in self.__visited):
            if self.__is_tile_connected_blue(row + 1, col, tiles):
                return True
        if not ((row - 1, col) in self.__visited):
            if self.__is_tile_connected_blue(row - 1, col, tiles):
                return True
        if not ((row - 1, col + 1) in self.__visited):
            if self.__is_tile_connected_blue(row - 1, col + 1, tiles):
                return True
        if not ((row, col + 1) in self.__visited):
            if self.__is_tile_connected_blue(row, col + 1, tiles):
                return True
        return False

    def get_virtual_tiles(self):
        virtual_tiles = [[VirtualTile for j in range(11)] for k in range(11)]
        for row in range(11):
            for column in range(11):
                color = self.__board.tiles[row][column].fillColor
                virtual_tiles[row][column] = VirtualTile(row, column, color)
        return virtual_tiles
