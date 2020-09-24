import copy


class Ai:
    def __init__(self, board):
        self.__board = board
        self.__visited = set()
        self.__to_examine = set()
        self.__own_color_visited = set()

    def distance_to_all(self, row, col, color, enemy_color):
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

    def distance_from_to(self, row_from, column_from, row_to, column_to, enemy_color):
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

    def distance_to_next_tile_red(self, row, col):
        self.__visited.add((row, col))
        self.__to_examine.add((row, col))
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
                if (current_row >= self.__board.rowLength or current_column >= self.__board.columnLength
                        or current_column < 0 or current_row < 0):
                    continue
                if current_column >= self.__board.columnLength - 1:
                    return distance - 1, (row, col)
                if not ((current_row, current_column + 1) in self.__visited) and no_column_border:
                    temp_tile = self.__board.tiles[current_row][current_column + 1]
                    if temp_tile.fillColor == "red":
                        return distance - 1, (current_row, current_column + 1)
                    if temp_tile.fillColor != "blue":
                        self.__to_examine.add((current_row, current_column + 1))
                        self.__visited.add((current_row, current_column + 1))
                        self.__write_distance(temp_tile, distance)
                    if current_row > 0:
                        if not ((current_row - 1, current_column + 1) in self.__visited) and no_column_border:
                            temp_tile = self.__board.tiles[current_row - 1][current_column + 1]
                            if temp_tile.fillColor == "red":
                                return distance - 1, (current_row - 1, current_column + 1)
                            if temp_tile.fillColor != "blue":
                                self.__to_examine.add((current_row - 1, current_column + 1))
                                self.__visited.add((current_row - 1, current_column + 1))
                                self.__write_distance(temp_tile, distance)
                        if not ((current_row - 1, current_column) in self.__visited) and no_column_border:
                            temp_tile = self.__board.tiles[current_row - 1][current_column]
                            if temp_tile.fillColor == "red":
                                return distance - 1, (current_row - 1, current_column)
                            if temp_tile.fillColor != "blue":
                                self.__to_examine.add((current_row - 1, current_column))
                                self.__visited.add((current_row - 1, current_column))
                                self.__write_distance(temp_tile, distance)
                    if not ((current_row + 1, current_column) in self.__visited) and no_column_border:
                        temp_tile = self.__board.tiles[current_row + 1][current_column]
                        if temp_tile.fillColor == "red":
                            return distance - 1, (current_row + 1, current_column)
                        if temp_tile.fillColor != "blue":
                            self.__to_examine.add((current_row + 1, current_column))
                            self.__visited.add((current_row + 1, current_column))
                            self.__write_distance(temp_tile, distance)
            distance += 1

    def get_tiles_to_place_red(self, row):  # TODO: BUGGY AS FUCK
        at_end = False
        distance_sum = 0
        current_row = row
        current_col = 0
        while not at_end:
            struct = self.distance_to_next_tile_red(current_row, current_col)
            if struct is None:
                print("weird")
                break
            pos = struct[1]
            distance_sum += struct[0]
            current_row = pos[0]
            current_col = pos[1]
            at_end = pos[1] >= self.__board.columnLength - 1
        return distance_sum
