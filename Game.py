import tkinter as tk
from AI import Ai
from tkinter import messagebox
import random as r
import math as m


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
        self.__canvas = canvas
        self.__destination_length = 10
        self.__visited = set()
        self.occupiedTiles = set()
        self.__ai = Ai(board, canvas, self.occupiedTiles)
        self.__update_ai()
        self.__undo_stack = []
        self.__redo_stack = []

    def draw(self):
        self.board.draw(self.__canvas)

    def __update_ai(self):

        first_move = len(self.occupiedTiles) == 0
        if self.playersTurn == "red" and self.isRedComputer and not first_move:
            self.__ai.moves.clear()
            self.__ai.minimax("red", 3, -m.inf, +m.inf, True)
            tile = self.__ai.moves[0]
            row = tile[0]
            col = tile[1]
            self.board.tiles[row][col].set_color(self.__canvas, "red")
            self.playersTurn = "blue"
            self.__redo_stack.clear()
            self.occupiedTiles.add((row, col))
            self.__undo_stack.append((row, col, "red"))
            if self.is_red_winner(self.board.tiles):
                messagebox.showinfo("Game Over", "Red has won!")
                self.apply()
                print("blue")

        elif self.playersTurn == "blue" and self.isBlueComputer and not first_move:
            self.__ai.moves.clear()
            self.__ai.minimax("blue", 3, -m.inf, +m.inf, True)
            tile = self.__ai.moves[0]
            print(tile)
            row = tile[0]
            col = tile[1]
            self.board.tiles[row][col].set_color(self.__canvas, "blue")
            self.playersTurn = "red"
            self.__redo_stack.clear()
            self.occupiedTiles.add((row, col))
            self.__undo_stack.append((row, col, "blue"))
            if self.is_blue_winner(self.board.tiles):
                messagebox.showinfo("Game Over", "Blue has won!")
                self.apply()
                print("blue")
        elif self.playersTurn == "blue" and self.isBlueComputer and first_move:
            row = 5
            col = 6
            self.board.tiles[row][col].set_color(self.__canvas, "blue")
            self.playersTurn = "red"
            self.__redo_stack.clear()
            self.occupiedTiles.add((row, col))
            self.__undo_stack.append((row, col, "blue"))
        elif self.playersTurn == "red" and self.isBlueComputer and first_move:
            row = 5
            col = 6
            self.board.tiles[row][col].set_color(self.__canvas, "red")
            self.playersTurn = "blue"
            self.__redo_stack.clear()
            self.occupiedTiles.add((row, col))
            self.__undo_stack.append((row, col, "red"))
        self.__canvas.after(1, self.__update_ai)

    def mouse_input_config(self):
        self.__canvas.bind("<Button-1>", self.__button1_callback)

    def undo(self, event):
        if len(self.__undo_stack) <= 0:
            return
        to_remove = self.__undo_stack.pop()
        if to_remove[2] == "red":
            self.playersTurn = "blue"
        else:
            self.playersTurn = "red"
        self.occupiedTiles.remove((to_remove[0], to_remove[1]))
        self.board.tiles[to_remove[0]][to_remove[1]].set_color(self.__canvas, "white")
        self.__redo_stack.append(to_remove)

    def redo(self, event):
        if len(self.__redo_stack) <= 0:
            return
        to_add = self.__redo_stack.pop()
        if to_add[2] == "red":
            self.board.tiles[to_add[0]][to_add[1]].set_color(self.__canvas, "red")
            self.playersTurn = "blue"
        else:
            self.board.tiles[to_add[0]][to_add[1]].set_color(self.__canvas, "blue")
            self.playersTurn = "red"
        self.occupiedTiles.add((to_add[0], to_add[1]))
        self.__undo_stack.append(to_add)

    def __button1_callback(self, event):
        if (self.__canvas.find_withtag(tk.CURRENT)
                and self.__canvas.itemcget(tk.CURRENT, 'fill') == 'white'):
            cur_tag = self.__canvas.itemcget(tk.CURRENT, 'tag')
            if self.playersTurn == "red":
                if self.isRedComputer or cur_tag.find('-') == -1:
                    return
                self.__redo_stack.clear()
                self.__canvas.itemconfig(tk.CURRENT, fill="red")
                self.playersTurn = "blue"
                if self.is_red_winner(self.board.tiles):
                    print("Farbe = ", self.__canvas.itemcget(tk.CURRENT, 'fill'))
                    messagebox.showinfo("Game Over", "Red has won!")
                    self.apply()
                index_dash = cur_tag.find('-')
                index_space = cur_tag.find(' ')
                row = int(cur_tag[0:index_dash])
                col = int(cur_tag[index_dash + 1:index_space])
                self.board.tiles[row][col].fillColor = "red"
                self.occupiedTiles.add((row, col))
                self.__undo_stack.append((row, col, "red"))
            else:
                if self.isBlueComputer or cur_tag.find('-') == -1:
                    return
                self.__canvas.itemconfig(tk.CURRENT, fill="blue")
                self.playersTurn = "red"
                self.__redo_stack.clear()
                if self.is_blue_winner(self.board.tiles):
                    messagebox.showinfo("Game Over", "Blue has won!")
                    self.apply()
                    print("blue")
                index_dash = cur_tag.find('-')
                index_space = cur_tag.find(' ')
                row = int(cur_tag[0:index_dash])
                col = int(cur_tag[index_dash + 1:index_space])
                self.board.tiles[row][col].fillColor = "blue"
                self.occupiedTiles.add((row, col))
                self.__undo_stack.append((row, col, "blue"))

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
        t_color = tile.get_fill_color(self.__canvas)
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
        t_color = tile.get_fill_color(self.__canvas)
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

    def __clear_board(self):
        self.board.clear_board(self.__canvas)

    def apply(self):
        self.occupiedTiles.clear()
        self.__clear_board()
        self.playersTurn = self.playerBegins

    def change_transformable(self, canvas, x, y, width):
        self.board.change_transformable(canvas, x, y, width)
