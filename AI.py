import copy
import math as m
from HexNode import HexNode


class Ai:
    def __init__(self, board):
        self.__board = board
        self.__shortest_path = set()
        self.__graph = [[HexNode for j in range(13)] for i in range(13)]
        self.__to_examine_blue_d = set()
        self.__blue_tiles_visited = set()
        self.__destination_distance_b = list()
        self.__visited = set()
        self.__to_examine = set()
        self.__own_color_visited = set()

    def __distance_to_all(self, row, col, color, enemy_color):
        self.__visited.add((row, col))
        self.__own_color_visited.add(row, col)
        self.__to_examine.add((row, col))
        distance = 1
        tiles_to_place = 0
        tiles_to_examine = True
        while tiles_to_examine:
            to_examine_count = len(self.__to_examine)
            tiles_to_examine = to_examine_count > 0
            examine = copy.deepcopy(self.__to_examine)
            self.__to_examine.clear()
            for tile_coordinates in examine:
                current_row = tile_coordinates[0]
                current_column = tile_coordinates[1]
                no_column_border = current_column < self.__board.columnLength - 1
                no_row_border = current_row < self.__board.rowLength - 1
                if (current_row >= self.__board.rowLength or current_column >= self.__board.columnLength
                        or current_column < 0 or current_row < 0):
                    continue
                if current_column > 0:
                    if not ((current_row, current_column - 1) in self.__visited):
                        temp_tile = self.__board.tiles[current_row][current_column - 1]
                        if temp_tile.fillColor != enemy_color:
                            self.__write_distance(temp_tile, distance)
                            self.__to_examine.add((current_row, current_column - 1))
                            self.__visited.add((current_row, current_column - 1))
                    if not ((current_row + 1, current_column - 1) in self.__visited) and no_row_border:
                        temp_tile = self.__board.tiles[current_row + 1][current_column - 1]
                        if temp_tile.fillColor != enemy_color:
                            self.__write_distance(temp_tile, distance)
                            self.__to_examine.add((current_row + 1, current_column - 1))
                            self.__visited.add((current_row + 1, current_column - 1))
                if current_row > 0:
                    if not ((current_row - 1, current_column) in self.__visited):
                        temp_tile = self.__board.tiles[current_row - 1][current_column]
                        if temp_tile.fillColor != enemy_color:
                            self.__write_distance(temp_tile, distance)
                            self.__to_examine.add((current_row - 1, current_column))
                            self.__visited.add((current_row - 1, current_column))
                    if not ((current_row - 1, current_column + 1) in self.__visited) and no_column_border:
                        temp_tile = self.__board.tiles[current_row - 1][current_column + 1]
                        if temp_tile.fillColor != enemy_color:
                            self.__write_distance(temp_tile, distance)
                            self.__to_examine.add((current_row - 1, current_column + 1))
                            self.__visited.add((current_row - 1, current_column + 1))
                if not ((current_row + 1, current_column) in self.__visited) and no_row_border:
                    temp_tile = self.__board.tiles[current_row + 1][current_column]
                    if temp_tile.fillColor != enemy_color:
                        self.__write_distance(temp_tile, distance)
                        self.__to_examine.add((current_row + 1, current_column))
                        self.__visited.add((current_row + 1, current_column))
                if not ((current_row, current_column + 1) in self.__visited) and no_column_border:
                    temp_tile = self.__board.tiles[current_row][current_column + 1]
                    if temp_tile.fillColor != enemy_color:
                        self.__write_distance(temp_tile, distance)
                        self.__to_examine.add((current_row, current_column + 1))
                        self.__visited.add((current_row, current_column + 1))
            distance += 1

    def __write_distance(self, tile, distance):
        if tile.text == "":
            tile.add_text(str(distance), self.__board.canvas, 'black')

    def __distance_from_to(self, row_from, column_from, row_to, column_to, enemy_color):
        self.__visited.add((row_from, column_from))
        self.__to_examine.add((row_from, column_from))
        distance = 1
        tiles_to_examine = True
        while tiles_to_examine:
            to_examine_count = len(self.__to_examine)
            tiles_to_examine = to_examine_count > 0
            examine = copy.deepcopy(self.__to_examine)
            self.__to_examine.clear()
            for tile_coordinates in examine:
                current_row = tile_coordinates[0]
                current_column = tile_coordinates[1]
                no_column_border = current_column < self.__board.columnLength - 1
                no_row_border = current_row < self.__board.rowLength - 1
                if (current_row >= self.__board.rowLength or current_column >= self.__board.columnLength
                        or current_column < 0 or current_row < 0):
                    continue
                if current_column > 0:
                    if not ((current_row, current_column - 1) in self.__visited):
                        if current_row == row_to and current_column - 1 == column_to:
                            return distance - 1
                        temp_tile = self.__board.tiles[current_row][current_column - 1]
                        if temp_tile.fillColor != enemy_color:
                            self.__write_distance(temp_tile, distance)
                            self.__to_examine.add((current_row, current_column - 1))
                            self.__visited.add((current_row, current_column - 1))
                    if not ((current_row + 1, current_column - 1) in self.__visited) and no_row_border:
                        if current_row + 1 == row_to and current_column - 1 == column_to:
                            return distance - 1
                        temp_tile = self.__board.tiles[current_row + 1][current_column - 1]
                        if temp_tile.fillColor != enemy_color:
                            self.__write_distance(temp_tile, distance)
                            self.__to_examine.add((current_row + 1, current_column - 1))
                            self.__visited.add((current_row + 1, current_column - 1))
                if current_row > 0:
                    if not ((current_row - 1, current_column) in self.__visited):
                        if current_row - 1 == row_to and current_column == column_to:
                            return distance - 1
                        temp_tile = self.__board.tiles[current_row - 1][current_column]
                        if temp_tile.fillColor != enemy_color:
                            self.__write_distance(temp_tile, distance)
                            self.__to_examine.add((current_row - 1, current_column))
                            self.__visited.add((current_row - 1, current_column))
                    if not ((current_row - 1, current_column + 1) in self.__visited) and no_column_border:
                        if current_row - 1 == row_to and current_column + 1 == column_to:
                            return distance - 1
                        temp_tile = self.__board.tiles[current_row - 1][current_column + 1]
                        if temp_tile.fillColor != enemy_color:
                            self.__write_distance(temp_tile, distance)
                            self.__to_examine.add((current_row - 1, current_column + 1))
                            self.__visited.add((current_row - 1, current_column + 1))
                if not ((current_row + 1, current_column) in self.__visited) and no_row_border:
                    if current_row + 1 == row_to and current_column == column_to:
                        return distance - 1
                    temp_tile = self.__board.tiles[current_row + 1][current_column]
                    if temp_tile.fillColor != enemy_color:
                        self.__write_distance(temp_tile, distance)
                        self.__to_examine.add((current_row + 1, current_column))
                        self.__visited.add((current_row + 1, current_column))
                if not ((current_row, current_column + 1) in self.__visited) and no_column_border:
                    if current_row == row_to and current_column + 1 == column_to:
                        return distance - 1
                    temp_tile = self.__board.tiles[current_row][current_column + 1]
                    if temp_tile.fillColor != enemy_color:
                        self.__write_distance(temp_tile, distance)
                        self.__to_examine.add((current_row, current_column + 1))
                        self.__visited.add((current_row, current_column + 1))
            distance += 1

    def __distance_to_next_tile_red(self, row, col, distance=1):
        to_examine = set()
        visited = set()
        visited.add((row, col))
        to_examine.add((row, col))
        distance = distance
        tiles_to_examine = True

        while tiles_to_examine:
            to_examine_count = len(to_examine)
            tiles_to_examine = to_examine_count > 0
            examine = copy.deepcopy(to_examine)
            to_examine.clear()

            for tile_coordinates in examine:
                current_row = tile_coordinates[0]
                current_column = tile_coordinates[1]
                no_column_border = current_column < self.__board.columnLength - 1
                no_row_border = current_row < self.__board.rowLength - 1

                if (current_row >= self.__board.rowLength or current_column >= self.__board.columnLength
                        or current_column < 0 or current_row < 0):
                    continue

                if current_column >= self.__board.columnLength - 1:
                    return distance - 1, (current_row, current_column)

                if not ((current_row, current_column + 1) in visited) and no_column_border:
                    temp_tile = self.__board.tiles[current_row][current_column + 1]
                    if temp_tile.fillColor == "red":
                        return distance - 1, (current_row, current_column + 1)
                    if temp_tile.fillColor != "blue":
                        to_examine.add((current_row, current_column + 1))
                        visited.add((current_row, current_column + 1))
                        self.__write_distance(temp_tile, distance)

                    if current_row > 0:
                        if not ((current_row - 1, current_column + 1) in visited) and no_column_border:
                            temp_tile = self.__board.tiles[current_row - 1][current_column + 1]
                            if temp_tile.fillColor == "red":
                                return distance - 1, (current_row - 1, current_column + 1)
                            if temp_tile.fillColor != "blue":
                                to_examine.add((current_row - 1, current_column + 1))
                                visited.add((current_row - 1, current_column + 1))
                                self.__write_distance(temp_tile, distance)

                        if not ((current_row - 1, current_column) in visited) and no_column_border:
                            temp_tile = self.__board.tiles[current_row - 1][current_column]
                            if temp_tile.fillColor == "red":
                                return distance - 1, (current_row - 1, current_column)
                            if temp_tile.fillColor != "blue":
                                to_examine.add((current_row - 1, current_column))
                                visited.add((current_row - 1, current_column))
                                # self.__write_distance(temp_tile, distance)

                    if not ((current_row + 1, current_column) in visited) and no_column_border and no_row_border:
                        temp_tile = self.__board.tiles[current_row + 1][current_column]
                        if temp_tile.fillColor == "red":
                            return distance - 1, (current_row + 1, current_column)
                        if temp_tile.fillColor != "blue":
                            to_examine.add((current_row + 1, current_column))
                            visited.add((current_row + 1, current_column))
                            self.__write_distance(temp_tile, distance)
            distance += 1

    def get_value_red(self):
        min_val = m.inf
        for row in range(11):
            val = self.__get_tiles_to_place_red(row)
            print(val)
            if val < min_val:
                min_val = val
        return min_val

    def __get_tiles_to_place_red(self, row):
        at_end = False
        distance_sum = 0
        current_row = row
        current_col = 0
        while not at_end:
            struct = self.__distance_to_next_tile_red(current_row, current_col)
            if struct is None:
                print("weird")
                break
            pos = struct[1]
            distance_sum += struct[0]
            current_row = pos[0]
            current_col = pos[1]
            at_end = pos[1] >= self.__board.columnLength - 1
        return distance_sum + 1

    def __distance_to_next_tile_blue(self, row, col, distance=1):
        to_examine = set()
        interesting_blue_tiles = list()
        visited = set()
        visited.add((row, col))
        to_examine.add((row, col))
        distance = distance
        tiles_to_examine = True
        blue_tile_found = False
        while tiles_to_examine:
            to_examine_count = len(to_examine)
            tiles_to_examine = to_examine_count > 0
            examine = copy.deepcopy(to_examine)
            to_examine.clear()

            for tile_coordinates in examine:
                current_row = tile_coordinates[0]
                current_column = tile_coordinates[1]
                no_column_border = current_column < self.__board.columnLength - 1
                no_row_border = current_row < self.__board.rowLength - 1
                temp_tile_curr = self.__board.tiles[current_row][current_column]

                if temp_tile_curr.fillColor == "blue" and current_row == 0:
                    interesting_blue_tiles.append((0, (current_row, current_column)))
                    return interesting_blue_tiles

                if (current_row >= self.__board.rowLength or current_column >= self.__board.columnLength
                        or current_column < 0 or current_row < 0):
                    continue

                if current_row >= self.__board.rowLength - 1:
                    interesting_blue_tiles.append((distance - 1, (current_row, current_column)))
                    return interesting_blue_tiles

                if not ((current_row + 1, current_column) in visited) and no_row_border:
                    temp_tile = self.__board.tiles[current_row + 1][current_column]
                    if (temp_tile.fillColor == "blue"
                            and not (current_row + 1, current_column) in visited in self.__blue_tiles_visited):
                        blue_tile_found = True
                        self.__blue_tiles_visited.add((current_row + 1, current_column))
                        interesting_blue_tiles.append((distance - 1, (current_row + 1, current_column)))
                    if temp_tile.fillColor != "red" and not blue_tile_found:
                        to_examine.add((current_row + 1, current_column))
                        visited.add((current_row + 1, current_column))
                        self.__write_distance(temp_tile, distance)

                if current_column > 0:
                    if not ((current_row, current_column - 1) in visited):
                        temp_tile = self.__board.tiles[current_row][current_column - 1]
                        if (temp_tile.fillColor == "blue"
                                and not (current_row, current_column - 1) in self.__blue_tiles_visited):
                            self.__blue_tiles_visited.add((current_row, current_column - 1))
                            blue_tile_found = True
                            interesting_blue_tiles.append((distance - 1, (current_row, current_column - 1)))
                        if temp_tile.fillColor != "red" and not blue_tile_found:
                            to_examine.add((current_row, current_column - 1))
                            visited.add((current_row, current_column - 1))
                            self.__write_distance(temp_tile, distance)

                    if not ((current_row + 1, current_column - 1) in visited) and no_row_border:
                        temp_tile = self.__board.tiles[current_row + 1][current_column - 1]
                        if (temp_tile.fillColor == "blue"
                                and not (current_row + 1, current_column - 1) in self.__blue_tiles_visited):
                            self.__blue_tiles_visited.add((current_row + 1, current_column - 1))
                            blue_tile_found = True
                            interesting_blue_tiles.append((distance - 1, (current_row + 1, current_column - 1)))
                        if temp_tile.fillColor != "red" and not blue_tile_found:
                            to_examine.add((current_row + 1, current_column - 1))
                            visited.add((current_row + 1, current_column - 1))
                            self.__write_distance(temp_tile, distance)

                if not ((current_row, current_column + 1) in visited) and no_column_border:
                    temp_tile = self.__board.tiles[current_row][current_column + 1]
                    if (temp_tile.fillColor == "blue"
                            and not (current_row, current_column + 1) in self.__blue_tiles_visited):
                        self.__blue_tiles_visited.add((current_row, current_column + 1))
                        blue_tile_found = True
                        interesting_blue_tiles.append((distance - 1, (current_row, current_column + 1)))
                    if temp_tile.fillColor != "red" and not blue_tile_found:
                        to_examine.add((current_row, current_column + 1))
                        visited.add((current_row, current_column + 1))
                        self.__write_distance(temp_tile, distance)

                if blue_tile_found:
                    return interesting_blue_tiles
            distance += 1

    def __get_tiles_to_place_blue(self, col):
        self.__blue_tiles_visited.clear()
        at_end = False
        current_row = 0
        current_col = col
        min_distance = m.inf
        path_array = list()
        path_visited = set()
        current_distance = 1
        while not at_end:  # todo buggy

            # todo buggy + nochmal was überprüfen wenn distance gleich bei zwei paths,
            # wenn es mehr als 1 path gibt wird immer der erste genommen und die anderen mit curr distance
            # gespeichert und später alle anderen paths nochmal durchgegangen wenn nötig nochaml wiederholen bis
            # kein path mehr übrig ist
            temp_path_array = self.__distance_to_next_tile_blue(current_row, current_col, current_distance)
            if temp_path_array is None:
                print("weird")
                break
            path = temp_path_array[0]
            if len(temp_path_array) > 1:
                for i in range(1, len(temp_path_array)):
                    path_array.append(temp_path_array[i])
            current_distance = path[0]
            temp_current_pos = path[1]
            current_row = temp_current_pos[0]
            current_col = temp_current_pos[1]
            print(temp_path_array)
            at_end = current_row >= self.__board.rowLength - 1

        return current_distance + 1

    def get_value_blue(self):  # TODO: Buggy as fuck
        min_val = m.inf
        for col in range(11):
            val = self.__get_tiles_to_place_blue(col)
            if val < min_val:
                min_val = val
            print(val)
        return min_val

    def __setup_dijkstra_blue(self):
        self.__shortest_path.clear()
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

        while len(self.__shortest_path) < vertex_amount:
            node = self.get_min_dist_node(self.__to_examine_blue_d)
            self.__to_examine_blue_d.remove(node)
            self.__shortest_path.add(node)
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
                    and not (neighbour_node in self.__shortest_path)
                    and neighbour_node.weight + node.distance < neighbour_node.distance):
                neighbour_node.distance = neighbour_node.weight + node.distance
                self.__to_examine_blue_d.add(neighbour_node)
                tile = self.__board.tiles[row - 1][col - 1]
                self.__write_distance(tile, neighbour_node.distance)
            if neighbour_node.nodeType == "destination":
                self.__destination_distance_b.append(node.distance)

    def get_min_dist_node(self, to_examine):
        min_number = m.inf
        min_node = None
        for node in to_examine:
            if node.distance < min_number and node not in self.__shortest_path:
                min_number = node.distance
                min_node = node
        return min_node
