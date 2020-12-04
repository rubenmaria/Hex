from array import array
import pprint


class YBoard:

    def __init__(self, hex_board_size, color):
        self.color = color
        self.character = color[0]
        self.hex_board_size = hex_board_size
        self.y_board = [array('f') for i in range(self.hex_board_size + self.hex_board_size - 1)]
        self.__init_y_array()

    def __init_y_array(self):
        y_board_size = self.hex_board_size + self.hex_board_size - 1
        column_length = y_board_size
        for row in range(0, y_board_size):
            for col in range(0, column_length):
                if self.color == 'i':
                    self.y_board[row].append(0)
                else:
                    if self.hex_board_size - 1 < col:  # Filled with Red pieces to get a Hex-board
                        if self.color == "red":
                            self.y_board[row].append(1)
                        else:
                            self.y_board[row].append(-1)
                    elif self.hex_board_size - 1 < row:
                        if self.color == "blue":
                            self.y_board[row].append(1)
                        else:
                            self.y_board[row].append(-1)
                    else:
                        self.y_board[row].append(0)
            column_length -= 1

    def print_board(self):
        b = self.hex_board_size + self.hex_board_size - 1
        for x in range(0, b):
            for y in range(0, x + 1):
                print(self.get_y(x, y), end=" ")
            print("\n")

    def place_hex(self, x, y, color):
        self.__is_hex_bounds(x, y)
        x_yboard = self.hex_board_size - 1 - x
        y_yboard = self.hex_board_size - 1 - y
        if color == self.color:
            self.y_board[x_yboard][y_yboard] = 1
        elif color == "white":
            self.y_board[x_yboard][y_yboard] = 0
        else:
            self.y_board[x_yboard][y_yboard] = -1

    def get_hex(self, x, y):
        self.__is_hex_bounds(x, y)
        x_yboard = self.hex_board_size - 1 - x
        y_yboard = self.hex_board_size - 1 - y
        return self.y_board[x_yboard][y_yboard]

    def __is_hex_bounds(self, x, y):
        if (x >= self.hex_board_size or y >= self.hex_board_size
                or x < 0 or y < 0):
            raise IndexError

    def place_y_val(self, x, y, val):
        self.__is_y_bounds(x, y)
        y_board_size = self.hex_board_size + self.hex_board_size - 1
        y_max = y_board_size - 1
        x_yboard = x - y
        y_yboard = y_max - x  # idk
        self.y_board[x_yboard][y_yboard] = val

    def place_y(self, x, y, color):
        self.__is_y_bounds(x, y)
        y_board_size = self.hex_board_size + self.hex_board_size - 1
        y_max = y_board_size - 1
        x_yboard = x - y
        y_yboard = y_max - x
        if color == self.color:
            self.y_board[x_yboard][y_yboard] = 1
        else:
            self.y_board[x_yboard][y_yboard] = -1

    def get_y(self, x, y):
        if not self.__is_y_bounds(x, y):
            return 0
        y_board_size = self.hex_board_size + self.hex_board_size - 1
        y_max = y_board_size - 1
        x_yboard = x - y
        y_yboard = y_max - x
        return self.y_board[x_yboard][y_yboard]

    def __is_y_bounds(self, x, y):
        y_board_size = self.hex_board_size + self.hex_board_size - 1
        if x < 0 or y < 0 or y > x or x >= y_board_size or y >= y_board_size:
            return False
        return True
