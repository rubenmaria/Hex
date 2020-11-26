from array import array


class Y_Board:
    def __init__(self, hex_board_size):
        self.hex_board_size = hex_board_size
        self.y_board = [array('i') for i in range(self.hex_board_size + self.hex_board_size -1)]
        self.__init_y_array()

    def __init_y_array(self):
        y_board_size = self.hex_board_size + self.hex_board_size - 1
        column_length = y_board_size
        for row in range(0, y_board_size):
            for col in range(column_length, 0, -1):
                self.y_board[row].append(1)
            column_length -= 1

        print(self.y_board)

