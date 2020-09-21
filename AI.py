import copy


class Ai:
    def __init__(self, board):
        self.__board = board
        self.__visited = set()
        self.__to_examine = set()

    def distance_to_all(self, row, col):
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
                no_row_border = current_row < self.__board.rowLength - 1
                if (current_row >= self.__board.rowLength or current_column >= self.__board.columnLength
                        or current_column < 0 or current_row < 0):
                    continue
                if current_column > 0:
                    if not ((current_row, current_column - 1) in self.__visited):
                        temp_tile = self.__board.tiles[current_row][current_column - 1]
                        self.__write_distance(temp_tile, distance)
                        self.__to_examine.add((current_row, current_column - 1))
                        self.__visited.add((current_row, current_column - 1))
                    if not ((current_row + 1, current_column - 1) in self.__visited) and no_row_border:
                        temp_tile = self.__board.tiles[current_row + 1][current_column - 1]
                        self.__write_distance(temp_tile, distance)
                        self.__to_examine.add((current_row + 1, current_column - 1))
                        self.__visited.add((current_row + 1, current_column - 1))
                if not ((current_row + 1, current_column) in self.__visited) and no_row_border:
                    temp_tile = self.__board.tiles[current_row + 1][current_column]
                    self.__write_distance(temp_tile, distance)
                    self.__to_examine.add((current_row + 1, current_column))
                    self.__visited.add((current_row + 1, current_column))
                if current_row > 0:
                    if not ((current_row - 1, current_column) in self.__visited):
                        temp_tile = self.__board.tiles[current_row - 1][current_column]
                        self.__write_distance(temp_tile, distance)
                        self.__to_examine.add((current_row - 1, current_column))
                        self.__visited.add((current_row - 1, current_column))
                    if not ((current_row - 1, current_column + 1) in self.__visited) and no_column_border:
                        temp_tile = self.__board.tiles[current_row - 1][current_column + 1]
                        self.__write_distance(temp_tile, distance)
                        self.__to_examine.add((current_row - 1, current_column + 1))
                        self.__visited.add((current_row - 1, current_column + 1))
                if not ((current_row, current_column + 1) in self.__visited) and no_column_border:
                    temp_tile = self.__board.tiles[current_row][current_column + 1]
                    self.__write_distance(temp_tile, distance)
                    self.__to_examine.add((current_row, current_column + 1))
                    self.__visited.add((current_row, current_column + 1))
            distance += 1

    def __write_distance(self, tile, distance):
        if tile.text == "":
            tile.add_text(str(distance), self.__board.canvas, 'black')
