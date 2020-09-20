class Ai:
    def __init__(self, board):
        self.__board = board
        self.__visited = set()

    def distance_to_all(self, row, col, distance=0):
        self.__visited.add((row, col))
        if row >= self.__board.rowLength or col >= self.__board.columnLength or col < 0 or row < 0:
            return True
        tile = self.__board.tiles[row][col]
        if distance != 0:
            tile.add_text(str(distance), self.__board.canvas, 'black')
        """t_color = tile.get_fill_color(self.__canvas)
        if t_color != 'red':
            return False"""
        if not ((row, col - 1) in self.__visited):
            if self.distance_to_all(row, col - 1, distance + 1) and distance != 0:
                return True
        if not ((row + 1, col - 1) in self.__visited):
            if self.distance_to_all(row + 1, col - 1, distance + 1) and distance != 0:
                return True
        if not ((row + 1, col) in self.__visited):
            if self.distance_to_all(row + 1, col, distance + 1) and distance != 0:
                return True
        if not ((row - 1, col) in self.__visited):
            if self.distance_to_all(row - 1, col, distance + 1) and distance != 0:
                return True
        if not ((row - 1, col + 1) in self.__visited):
            if self.distance_to_all(row - 1, col + 1, distance + 1) and distance != 0:
                return True
        if not ((row, col + 1) in self.__visited):
            if self.distance_to_all(row, col + 1, distance + 1) and distance != 0:
                return True
        return False


