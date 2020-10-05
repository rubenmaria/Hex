import tkinter as tk
from AI import Ai
from tkinter import messagebox

class Game:
    def __init__(self, board, canvas):
        self.playersTurn = "red"
        self.playerBegins = "red"
        self.isSwapRule = False
        self.redComputerLevel = 1
        self.blueComputerLevel = 1
        self.isRedComputer = False
        self.isBlueComputer = False
        self.board = board
        self.occupiedByBlue = list()
        self.occupiedByRed = list()
        self.__canvas = canvas
        self.__destination_length = 10
        self.__visited = set()
        self.__ai = Ai(board)

    def draw(self):
        self.board.draw(self.__canvas)

    def mouse_input_config(self):
        self.__canvas.bind("<Button-1>", self.__button1_callback)

    def __button1_callback(self, event):
        if (self.__canvas.find_withtag(tk.CURRENT)
                and self.__canvas.itemcget(tk.CURRENT, 'fill') == 'white'):
            cur_tag = self.__canvas.itemcget(tk.CURRENT, 'tag')
            if self.playersTurn == "red":
                if self.isRedComputer:
                    return
                self.__canvas.itemconfig(tk.CURRENT, fill="blue")
                self.__canvas.update_idletasks()
                self.__canvas.after(200)
                self.__canvas.itemconfig(tk.CURRENT, fill="red")
                self.playersTurn = "blue"
                if self.is_red_winner():
                    messagebox.showinfo("Game Over", "Red has won!")
                    self.apply()
                index_dash = cur_tag.find('-')
                index_space = cur_tag.find(' ')
                row = int(cur_tag[0:index_dash])
                col = int(cur_tag[index_dash + 1:index_space])
                self.board.tiles[row][col].fillColor = "red"
                self.occupiedByRed.append((row, col))
                print(self.occupiedByRed)
                """if len(self.occupiedByRed) == 3:
                    tile_from = self.occupiedByRed[0]
                    tile_to = self.occupiedByRed[1]
                    print("distance : ", self.__ai.get_tiles_to_place_red(0))"""
            else:
                if self.isBlueComputer:
                    return
                self.__canvas.itemconfig(tk.CURRENT, fill="red")
                self.__canvas.update_idletasks()
                self.__canvas.after(200)
                self.__canvas.itemconfig(tk.CURRENT, fill="blue")
                self.playersTurn = "red"
                if self.is_blue_winner():
                    messagebox.showinfo("Game Over", "Red has won!")
                    self.apply()
                index_dash = cur_tag.find('-')
                index_space = cur_tag.find(' ')
                row = int(cur_tag[0:index_dash])
                col = int(cur_tag[index_dash + 1:index_space])
                self.board.tiles[row][col].fillColor = "blue"
                self.occupiedByBlue.append((row, col))
                # self.__ai.distance_to_all(row, col, "red")
                print(self.occupiedByBlue)

    def is_red_winner(self):
        for row in range(11):
            self.__visited.clear()
            if self.__is_tile_connected_red(row, 0):
                self.__visited.clear()
                return True
        self.__visited.clear()
        return False

    def is_blue_winner(self):
        for col in range(11):
            self.__visited.clear()
            if self.__is_tile_connected_blue(0, col):
                self.__visited.clear()
                return True
        self.__visited.clear()
        return False

    def __is_tile_connected_red(self, row, col):
        self.__visited.add((row, col))
        if col > self.__destination_length:
            return True
        if row > self.__destination_length or col < 0 or row < 0:
            return False
        tile = self.board.tiles[row][col]
        t_color = tile.get_fill_color(self.__canvas)
        if t_color != 'red':
            return False
        if not ((row, col - 1) in self.__visited):
            if self.__is_tile_connected_red(row, col - 1):
                return True
        if not ((row + 1, col - 1) in self.__visited):
            if self.__is_tile_connected_red(row + 1, col - 1):
                return True
        if not ((row + 1, col) in self.__visited):
            if self.__is_tile_connected_red(row + 1, col):
                return True
        if not ((row - 1, col) in self.__visited):
            if self.__is_tile_connected_red(row - 1, col):
                return True
        if not ((row - 1, col + 1) in self.__visited):
            if self.__is_tile_connected_red(row - 1, col + 1):
                return True
        if not ((row, col + 1) in self.__visited):
            if self.__is_tile_connected_red(row, col + 1):
                return True
        return False

    def __is_tile_connected_blue(self, row, col):
        self.__visited.add((row, col))
        if row > self.__destination_length:
            return True
        if col > self.__destination_length or row < 0 or col < 0:
            return False
        tile = self.board.tiles[row][col]
        t_color = tile.get_fill_color(self.__canvas)
        if t_color != 'blue':
            return False
        if not ((row, col - 1) in self.__visited):
            if self.__is_tile_connected_blue(row, col - 1):
                return True
        if not ((row + 1, col - 1) in self.__visited):
            if self.__is_tile_connected_blue(row + 1, col - 1):
                return True
        if not ((row + 1, col) in self.__visited):
            if self.__is_tile_connected_blue(row + 1, col):
                return True
        if not ((row - 1, col) in self.__visited):
            if self.__is_tile_connected_blue(row - 1, col):
                return True
        if not ((row - 1, col + 1) in self.__visited):
            if self.__is_tile_connected_blue(row - 1, col + 1):
                return True
        if not ((row, col + 1) in self.__visited):
            if self.__is_tile_connected_blue(row, col + 1):
                return True
        return False

    def __clear_board(self):
        self.board.clear_board(self.__canvas)

    def apply(self):
        self.__clear_board()
        self.playersTurn = self.playerBegins

    def change_transformable(self, canvas, x, y, width):
        self.board.change_transformable(canvas, x, y, width)
