import copy
import math as m
from HexNode import HexNode
import copy as c
import random as r
from yBoard import YBoard


class Ai:
    def __init__(self, board, canvas, occupied_tiles, y_board_red, y_board_blue):
        self.__board = board
        self.occupied_tiles = occupied_tiles
        self.graph_blue = [[HexNode for j in range(13)] for i in range(13)]
        self.graph_red = [[HexNode for j in range(13)] for i in range(13)]
        self.y_board_red = y_board_red
        self.y_board_blue = y_board_blue
        self.__destination_length = 10
        self.__visited = set()
        self.__to_examine_red_starting = set()
        self.__to_examine_blue_starting = set()
        self.__canvas = canvas
        self.setup_dijkstra_blue()
        self.setup_dijkstra_red()

    def f(self, p, q, r):
        return 0.5 * (p + q + r - p * q * r)

    def g(self, q, r):
        return 0.5 * (1 - q * r)

    def y_eval(self, y_board_pos):
        board_size = self.__board.rowLength + self.__board.rowLength - 1
        val = [YBoard(11, "i") for i in range(0, board_size)]
        val[board_size - 1] = c.copy(y_board_pos)
        # val[board_size -1].print_board()
        for b in range(board_size - 2, -1, -1):
            for x in range(0, b + 1):
                for y in range(0, x + 1):
                    p = val[b + 1].get_y(x, y)
                    q = val[b + 1].get_y(x + 1, y)
                    r = val[b + 1].get_y(x + 1, y + 1)
                    prob = self.f(p, q, r)
                    val[b].place_y_val(x, y, prob)
            # val[b].print_board()
        return val

    def get_y_move(self, y_board_pos):
        board_size = self.__board.rowLength + self.__board.rowLength - 1
        move = [YBoard(11, "i") for i in range(0, board_size)]
        val = c.copy(self.y_eval(y_board_pos))
        move[0].place_y_val(0, 0, 1)
        for b in range(1, board_size):
            for x in range(0, b + 1):
                for y in range(0, x + 1):
                    p = move[b - 1].get_y(x, y) * self.g(val[b].get_y(x + 1, y), val[b].get_y(x + 1, y + 1))
                    q = move[b - 1].get_y(x - 1, y) * self.g(val[b].get_y(x, y), val[b].get_y(x, y + 1))
                    r = move[b - 1].get_y(x - 1, y - 1) * self.g(val[b].get_y(x, y - 1), val[b].get_y(x, y))
                    prob = p + q + r
                    move[b].place_y_val(x, y, prob)
        move[board_size - 1].print_board()

    def __write_distance(self, tile, distance):
        if not tile.isText:
            tile.add_text(str(distance), self.__board.canvas, 'black')
        else:
            tile.change_text(self.__board.canvas, str(distance))

    def delete_all_writing(self):
        self.__board.clear_writing(self.__canvas)

    def setup_dijkstra_blue(self):
        for x in range(13):
            for y in range(13):
                if (x == 0 or x == 12) and (y == 0 or y == 12):
                    self.graph_blue[x][y] = HexNode("wall", x, y)
                elif x == 0:
                    self.graph_blue[x][y] = HexNode("source", x, y)
                    self.__to_examine_blue_starting.add(HexNode("source", x, y))
                elif x == 12:
                    self.graph_blue[x][y] = HexNode("destination", x, y)
                elif y == 0 or y == 12:
                    self.graph_blue[x][y] = HexNode("wall", x, y)
                else:
                    self.graph_blue[x][y] = HexNode("impartial", x, y)

    def hex_dijkstra_b(self, graph):
        destination_distance = list()
        visited = set()
        to_examine = c.copy(self.__to_examine_blue_starting)
        # self.delete_all_writing() #debugging

        while True:
            node = self.get_min_dist_node(to_examine, visited)
            if node is None:
                break
            """row = node.x - 1
            col = node.y - 1
            if self.__is_pos_on_board((row, col)):
                self.__write_distance(self.__board.tiles[row][col], node.distance) #debugging"""
            to_examine.remove(node)
            visited.add(node)
            self.__update_dist_of_neighbour_b(node, graph, destination_distance, to_examine, visited)
            if node.nodeType != "source":
                node.distance = m.inf
        if len(destination_distance) == 0:
            return 12
        return min(destination_distance)

    def __update_dist_of_neighbour_b(self, node, graph, destination_distance, to_examine, visited):
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
            neighbour_node = graph[row][col]
            if row < 0 or row > 12:
                continue
            if col < 0 or col > 12:
                continue
            if ((neighbour_node.nodeType == "impartial" or neighbour_node.nodeType == "friendly")
                    and not (neighbour_node in visited)
                    and neighbour_node.weight + node.distance < neighbour_node.distance):
                neighbour_node.distance = neighbour_node.weight + node.distance
                to_examine.add(neighbour_node)
                # neighbour_node.print()
            if neighbour_node.nodeType == "destination":
                destination_distance.append(node.distance)

    def get_min_dist_node(self, to_examine, visited):
        if len(to_examine) == 0:
            return None
        return min(to_examine)

    def setup_dijkstra_red(self):
        for x in range(13):
            for y in range(13):
                if (x == 0 or x == 12) and (y == 0 or y == 12):
                    self.graph_red[x][y] = HexNode("wall", x, y)
                elif y == 0:
                    self.graph_red[x][y] = HexNode("source", x, y)
                    self.__to_examine_red_starting.add(HexNode("source", x, y))
                elif y == 12:
                    self.graph_red[x][y] = HexNode("destination", x, y)
                elif x == 0 or x == 12:
                    self.graph_red[x][y] = HexNode("wall", x, y)
                else:
                    self.graph_red[x][y] = HexNode("impartial", x, y)

    def hex_dijkstra_r(self, graph):
        destination_distance = list()
        # self.delete_all_writing() #debugging
        visited = set()
        to_examine = c.copy(self.__to_examine_red_starting)

        while True:
            node = self.get_min_dist_node(to_examine, visited)
            if node is None:
                break
            row = node.x - 1
            col = node.y - 1
            """if self.__is_pos_on_board((row, col)):
                self.__write_distance(self.__board.tiles[row][col], node.distance) #debugging"""
            to_examine.remove(node)
            visited.add(node)
            self.__update_dist_of_neighbour_r(node, graph, destination_distance, to_examine, visited)
            if node.nodeType != "source":
                node.distance = m.inf
        if len(destination_distance) == 0:
            return 12
        return min(destination_distance)

    def __update_dist_of_neighbour_r(self, node, graph, destination_distance, to_examine, visited):
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
            neighbour_node = graph[row][col]
            if row < 0 or row > 12:
                continue
            if col < 0 or col > 12:
                continue
            if ((neighbour_node.nodeType == "impartial" or neighbour_node.nodeType == "friendly")
                    and not (neighbour_node in visited)
                    and neighbour_node.weight + node.distance < neighbour_node.distance):
                neighbour_node.distance = neighbour_node.weight + node.distance
                to_examine.add(neighbour_node)
            if neighbour_node.nodeType == "destination":
                destination_distance.append(node.distance)

    def get_value_red(self, graph_red, graph_blue):
        red = self.hex_dijkstra_r(graph_red)
        blue = self.hex_dijkstra_b(graph_blue)
        return blue - red

    def get_value_blue(self, graph_blue, graph_red):
        red = self.hex_dijkstra_r(graph_red)
        blue = self.hex_dijkstra_b(graph_blue)
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
                position[0] > 10 or position[1] > 10):
            return False
        return True

    def get_value_moves(self, start_color, moves):
        graph_blue = self.graph_blue
        graph_red = self.graph_red
        color = start_color
        for move in moves:
            if color == "red":
                g_pos = self.from_tile_to_graph(move)
                graph_blue[g_pos[0]][g_pos[1]].set_color("enemy", "red")
                graph_red[g_pos[0]][g_pos[1]].set_color("friendly", "red")
                color = "blue"
            else:
                g_pos = self.from_tile_to_graph(move)
                graph_blue[g_pos[0]][g_pos[1]].set_color("friendly", "blue")
                graph_red[g_pos[0]][g_pos[1]].set_color("enemy", "blue")
                color = "red"
        if start_color == "red":
            value = self.get_value_red(graph_red, graph_blue)
        else:
            value = self.get_value_blue(graph_blue, graph_red)
        self.clear_moves(moves)
        return value

    def clear_moves(self, moves):
        for move in moves:
            g_pos = self.from_tile_to_graph(move)
            self.graph_red[g_pos[0]][g_pos[1]].set_color("impartial", "white")
            self.graph_blue[g_pos[0]][g_pos[1]].set_color("impartial", "white")

    def from_graph_to_tile(self, graph_position):
        return graph_position[0] - 1, graph_position[1] - 1

    def from_tile_to_graph(self, tile_position):
        return tile_position[0] + 1, tile_position[1] + 1

    def get_region_moves(self, moves):
        moves_set = set(moves)
        tiles = moves_set | self.occupied_tiles
        return self.get_active_region(tiles)

    def is_game_over_moves(self, start_color, moves):
        if len(moves) + len(self.occupied_tiles) < 21:
            return "none"
        graph_red = self.graph_red
        graph_blue = self.graph_blue
        color = start_color
        for move in moves:
            if color == "red":
                graph_blue[move[0] + 1][move[1] + 1].set_color("enemy", "red")
                graph_red[move[0] + 1][move[1] + 1].set_color("friendly", "red")
                color = "blue"
            else:
                graph_blue[move[0] + 1][move[1] + 1].set_color("friendly", "blue")
                graph_red[move[0] + 1][move[1] + 1].set_color("enemy", "blue")
                color = "red"
        if self.is_red_winner(graph_red):
            self.clear_moves(moves)
            return "red"
        if self.is_blue_winner(graph_blue):
            self.clear_moves(moves)
            return "blue"
        self.clear_moves(moves)
        return "none"

    def make_move(self, board, color, row, col):
        board[row][col].color = color

    def monte_carlo(self, color):
        active_region = self.get_active_region(self.occupied_tiles)
        virtual_occupied = c.deepcopy(self.occupied_tiles)
        best_score = -m.inf
        for move in active_region:
            board = self.get_virtual_tiles()
            virtual_occupied.add((move[0], move[1]))
            self.make_move(board, color, move[0], move[1])
            value = self.get_monte_score(board, color, virtual_occupied, 2000)
            print(value)
            if best_score < value:
                best_score = value
                best_move = move
        return best_move

    def get_monte_score(self, board, color, virtual_occupied, amount=1000):
        score = 0
        for i in range(amount):
            score += self.play_game_randomly(board, color, virtual_occupied)
        return score

    def play_game_randomly(self, board, color, virtual_occupied, future=10):
        if color == "red":
            current_color = "blue"
        else:
            current_color = "red"
        occupied = c.deepcopy(virtual_occupied)
        temp_board = c.deepcopy(board)
        for i in range(future):
            while True:
                row = r.randint(0, 10)
                col = r.randint(0, 10)
                if (row, col) not in occupied:
                    occupied.add((row, col))
                    temp_board[row][col].color = current_color
                    if current_color == "blue":
                        current_color = "red"
                    else:
                        current_color = "blue"
                    break
            """if self.is_red_winner(temp_board):
                if color == "red":
                    return 10
                return -10
            elif self.is_blue_winner(temp_board):
                if color == "blue":
                    return 10
                return -10"""
        if color == "red":
            return self.get_value_red(temp_board)
        return self.get_value_blue(temp_board)

    def minimax(self, moves, color, depth, max_depth, alpha, beta, maximizing, winning_move):
        if len(winning_move) > 0:
            return winning_move[0]

        winner = self.is_game_over_moves(color, moves)
        if depth == 0 or winner != "none":

            val = self.get_value_moves(color, moves)
            if winner == color:
                for move in moves:
                    mov = list()
                    mov.append(move)
                    if self.is_game_over_moves(color, mov) == color:
                        winning_move.append(move)
                        return winning_move[0]
            moves.pop()
            return val
        best_move = None
        active_region = self.get_region_moves(moves)
        if maximizing:
            max_eval = -m.inf
            for to_examine in active_region:
                moves.append(to_examine)
                val = self.minimax(moves, color, depth - 1, max_depth, alpha, beta, False, winning_move)
                if len(winning_move) > 0:
                    return winning_move[0]
                if max_eval < val:
                    max_eval = val
                    if depth == max_depth:
                        best_move = to_examine
                alpha = max(alpha, max_eval)
                if depth == max_depth:
                    moves.clear()
                if beta <= alpha:
                    break

            if depth == max_depth:
                if best_move is not None:
                    return best_move
            moves.pop()
            return max_eval
        else:
            min_eval = +m.inf
            for to_examine in active_region:
                moves.append(to_examine)
                val = self.minimax(moves, color, depth - 1, max_depth, alpha, beta, True, winning_move)
                if len(winning_move) > 0:
                    return winning_move[0]
                if min_eval > val:
                    min_eval = val
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            moves.pop()
            return min_eval

    def is_red_winner(self, graph):
        for row in range(11):
            if self.__is_tile_connected_red(row, 0, graph, set()):
                return True
        return False

    def is_blue_winner(self, graph):
        for col in range(11):
            if self.__is_tile_connected_blue(0, col, graph, set()):
                return True
        return False

    def __is_tile_connected_red(self, row, col, graph, visited):
        visited.add((row, col))
        if col > self.__destination_length:
            return True
        if row > self.__destination_length or col < 0 or row < 0:
            return False
        g_pos = self.from_tile_to_graph((row, col))
        tile = graph[g_pos[0]][g_pos[1]]
        t_color = tile.color
        if t_color != 'red':
            return False
        if not ((row, col - 1) in visited):
            if self.__is_tile_connected_red(row, col - 1, graph, visited):
                return True
        if not ((row + 1, col - 1) in visited):
            if self.__is_tile_connected_red(row + 1, col - 1, graph, visited):
                return True
        if not ((row + 1, col) in visited):
            if self.__is_tile_connected_red(row + 1, col, graph, visited):
                return True
        if not ((row - 1, col) in visited):
            if self.__is_tile_connected_red(row - 1, col, graph, visited):
                return True
        if not ((row - 1, col + 1) in visited):
            if self.__is_tile_connected_red(row - 1, col + 1, graph, visited):
                return True
        if not ((row, col + 1) in visited):
            if self.__is_tile_connected_red(row, col + 1, graph, visited):
                return True
        return False

    def __is_tile_connected_blue(self, row, col, graph, visited):
        visited.add((row, col))
        if row > self.__destination_length:
            return True
        if col > self.__destination_length or row < 0 or col < 0:
            return False
        g_pos = self.from_tile_to_graph((row, col))
        tile = graph[g_pos[0]][g_pos[1]]
        t_color = tile.color
        if t_color != 'blue':
            return False
        if not ((row, col - 1) in visited):
            if self.__is_tile_connected_blue(row, col - 1, graph, visited):
                return True
        if not ((row + 1, col - 1) in visited):
            if self.__is_tile_connected_blue(row + 1, col - 1, graph, visited):
                return True
        if not ((row + 1, col) in visited):
            if self.__is_tile_connected_blue(row + 1, col, graph, visited):
                return True
        if not ((row - 1, col) in visited):
            if self.__is_tile_connected_blue(row - 1, col, graph, visited):
                return True
        if not ((row - 1, col + 1) in visited):
            if self.__is_tile_connected_blue(row - 1, col + 1, graph, visited):
                return True
        if not ((row, col + 1) in visited):
            if self.__is_tile_connected_blue(row, col + 1, graph, visited):
                return True
        return False

    def is_game_over(self):
        return self.is_red_winner(self.graph_red) or self.is_blue_winner(self.graph_blue)

    def get_debug_red_value(self):
        return self.hex_dijkstra_r(self.graph_red)

    def get_debug_blue_value(self):
        return self.hex_dijkstra_b(self.graph_blue)

    def get_current_val(self, color):
        if color == "red":
            value = self.get_value_red(self.graph_red, self.graph_blue)
        else:
            value = self.get_value_blue(self.graph_blue, self.graph_red)
        return value
