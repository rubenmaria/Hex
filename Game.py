import tkinter as tk
from GUI import Gui
from AI import Ai
from tkinter import messagebox
import random as r
from GUI import Gui
import math as m
from yBoard import YBoard


class Game:
    def __init__(self, root, board, canvas):
        self.__playersTurn = "red"
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
        self.y_board_red = YBoard(11, "red")
        self.y_board_blue = YBoard(11, "blue")
        self.__ai = Ai(board, canvas, self.occupiedTiles, self.y_board_red, self.y_board_blue)
        self.isSwapRuleDone = False
        self.__undo_stack = []
        self.__redo_stack = []
        self.gui = Gui(canvas, root, self.apply)
        self.__update_ai()

    def draw(self):
        self.board.draw(self.__canvas)

    def make_move(self, row, col, color):
        is_color_red = color == "red"
        is_color_blue = color == "blue"
        prev_color = self.board.tiles[row][col].fillColor
        self.board.tiles[row][col].set_color(self.__canvas, color)
        if is_color_red:
            self.__place_hex_on_y(row, col, "red")
            self.__ai.graph_blue[row + 1][col + 1].set_color("enemy", "red")
            self.__ai.graph_red[row + 1][col + 1].set_color("friendly", "red")
            self.__playersTurn = "blue"
            self.occupiedTiles.add((row, col))
            self.__undo_stack.append((row, col, "red"))
            self.is_red_winner(self.board.tiles)
        elif is_color_blue:
            self.__place_hex_on_y(row, col, "blue")
            self.__ai.graph_blue[row + 1][col + 1].set_color("friendly", "blue")
            self.__ai.graph_red[row + 1][col + 1].set_color("enemy", "blue")
            self.__playersTurn = "red"
            self.occupiedTiles.add((row, col))
            self.__undo_stack.append((row, col, "blue"))
            self.is_blue_winner(self.board.tiles)
        else:
            self.occupiedTiles.remove((row, col))
            self.board.tiles[row][col].set_color(self.__canvas, "white")
            self.__ai.graph_blue[row + 1][col + 1].set_color("impartial", "white")
            self.__ai.graph_red[row + 1][col + 1].set_color("impartial", "white")
            self.__redo_stack.append((row, col, prev_color))

    def game_over(self, color):
        if color == "red":
            messagebox.showinfo("Game Over", "Red has won!")
        else:
            messagebox.showinfo("Game Over", "Blue has won!")
        self.restart_game()

    def __update_ai(self):
        #print(self.__ai.y_eval(self.y_board_red)[0].get_y(0, 0))

        if not self.isRedComputer and not self.isBlueComputer:
            self.__canvas.after(1, self.__update_ai)
            return
        self.is_red_winner(self.board.tiles)
        self.is_blue_winner(self.board.tiles)
        second_move = len(self.occupiedTiles) == 1
        first_move = len(self.occupiedTiles) == 0
        swap_rule = (second_move and self.isSwapRule) and not self.isSwapRuleDone
        if swap_rule and self.__playersTurn == "red" and self.isBlueComputer and not self.isRedComputer:
            msg = messagebox.askyesno("Swap Rule", "Do you want to Swap?")
            if msg:
                move = next(iter(self.occupiedTiles))
                row = move[0]
                col = move[1]
                self.__undo_stack.pop()
                self.make_move(row, col, "red")
            self.isSwapRuleDone = True
        elif swap_rule and self.__playersTurn == "blue" and not self.isBlueComputer and self.isRedComputer:
            msg = messagebox.askyesno("Swap Rule", "Do you want to Swap?")
            if msg:
                move = next(iter(self.occupiedTiles))
                row = move[0]
                col = move[1]
                self.__undo_stack.pop()
                self.make_move(row, col, "blue")
            self.isSwapRuleDone = True
        elif (self.__playersTurn == "red" and self.isRedComputer and not first_move
              and not swap_rule):
            level = self.redComputerLevel
            tile = self.__ai.minimax(list(), "red", level, level, -m.inf, +m.inf, True, list())
            #tile = self.__ai.monte_carlo("red")
            row = tile[0]
            col = tile[1]
            self.make_move(row, col, "red")
        elif (self.__playersTurn == "blue" and self.isBlueComputer and not first_move
              and not swap_rule):
            # tile = self.__ai.monte_carlo("blue")
            level = self.blueComputerLevel
            tile = self.__ai.minimax(list(), "blue", level, level, -m.inf, +m.inf, True, list())
            row = tile[0]
            col = tile[1]
            self.make_move(row, col, "blue")
        elif self.__playersTurn == "blue" and self.isBlueComputer and first_move and not self.isSwapRule:
            self.make_move(5, 6, "blue")
        elif self.__playersTurn == "red" and self.isRedComputer and first_move and not self.isSwapRule:
            self.make_move(5, 6, "red")
        elif self.__playersTurn == "blue" and self.isBlueComputer and first_move and self.isSwapRule:
            row = 9
            col = 9
            self.make_move(row, col, "blue")
        elif self.__playersTurn == "red" and self.isRedComputer and first_move and self.isSwapRule:
            row = 9
            col = 9
            self.make_move(row, col, "red")
        elif self.__playersTurn == "red" and self.isRedComputer and swap_rule:
            move = next(iter(self.occupiedTiles))
            row = move[0]
            col = move[1]
            if row in range(3, 8) and col in range(3, 8):
                messagebox.showinfo("Swap Rule", "Red Swapped your move!")
                self.board.tiles[row][col].set_color(self.__canvas, "red")
                self.__playersTurn = "blue" #TODO: maybe bugy
            else:
                level = self.redComputerLevel
                tile = self.__ai.minimax(list(), "red", level, level, -m.inf, +m.inf, True, list())
                # tile = self.__ai.monte_carlo("red")
                row = tile[0]
                col = tile[1]
                self.make_move(row, col, "red")
            self.isSwapRuleDone = True
        elif self.__playersTurn == "blue" and self.isBlueComputer and swap_rule:
            move = next(iter(self.occupiedTiles))
            row = move[0]
            col = move[1]
            if row in range(3, 8) and col in range(3, 8):
                messagebox.showinfo("Swap Rule", "Blue Swapped your move!")
                self.board.tiles[row][col].set_color(self.__canvas, "blue")
                self.__playersTurn = "red"
            else:
                level = self.blueComputerLevel
                tile = self.__ai.minimax(list(), "blue", level, level, -m.inf, +m.inf, True, list())
                row = tile[0]
                col = tile[1]
                self.make_move(row, col, "blue")
            self.isSwapRuleDone = True
        self.__canvas.after(1, self.__update_ai)

    def mouse_input_config(self):
        self.__canvas.bind("<Button-1>", self.__button1_callback)

    def undo(self, event):
        if len(self.__undo_stack) <= 0:
            return
        to_remove = self.__undo_stack.pop()
        if to_remove[2] == "red":
            self.__playersTurn = "blue"
        else:
            self.__playersTurn = "red"
        self.make_move(to_remove[0], to_remove[1], "white")

    def redo(self, event):
        if len(self.__redo_stack) <= 0:
            return
        to_add = self.__redo_stack.pop()
        self.make_move(to_add[0], to_add[1], to_add[2])

    def __button1_callback(self, event):
        if (self.__canvas.find_withtag(tk.CURRENT)
                and self.__canvas.itemcget(tk.CURRENT, 'fill') == 'white'):
            cur_tag = self.__canvas.itemcget(tk.CURRENT, 'tag')
            if self.__playersTurn == "red":
                if self.isRedComputer or cur_tag.find('-') == -1:
                    return
                index_dash = cur_tag.find('-')
                index_space = cur_tag.find(' ')
                row = int(cur_tag[0:index_dash])
                col = int(cur_tag[index_dash + 1:index_space])
                self.make_move(row, col, "red")
                self.__redo_stack.clear()
            else:
                if self.isBlueComputer or cur_tag.find('-') == -1:
                    return
                index_dash = cur_tag.find('-')
                index_space = cur_tag.find(' ')
                row = int(cur_tag[0:index_dash])
                col = int(cur_tag[index_dash + 1:index_space])
                self.make_move(row, col, "blue")
                self.__redo_stack.clear()

    def is_red_winner(self, tiles):
        for row in range(11):
            self.__visited.clear()
            if self.__is_tile_connected_red(row, 0, tiles):
                self.__visited.clear()
                self.game_over("red")
                return True
        self.__visited.clear()
        return False

    def is_blue_winner(self, tiles):
        for col in range(11):
            self.__visited.clear()
            if self.__is_tile_connected_blue(0, col, tiles):
                self.__visited.clear()
                self.game_over("blue")
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
        t_color = tile.fillColor
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
        t_color = tile.fillColor
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
        self.y_board_red = YBoard(11, "red")
        self.y_board_blue = YBoard(11, "blue")

    def apply(self):
        self.isBlueComputer = self.gui.isBlueComputer.get()
        self.isRedComputer = self.gui.isRedComputer.get()
        self.isSwapRule = self.gui.isSwapRule.get()
        self.blueComputerLevel = self.gui.blueComputerLevel.get()
        self.redComputerLevel = self.gui.redComputerLevel.get()
        if self.gui.isRedBeginning.get():
            self.playerBegins = "red"
        else:
            self.playerBegins = "blue"
        self.__playersTurn = self.playerBegins

    def restart_game(self):
        self.gui.blueComputerLevel.set(value=1)
        self.gui.redComputerLevel.set(value=1)
        self.gui.isRedBeginning.set(value=True)
        self.gui.isRedComputer.set(value=False)
        self.gui.isBlueComputer.set(value=False)
        self.gui.isSwapRule.set(value=False)
        self.apply()
        self.__ai.setup_dijkstra_blue()
        self.__ai.setup_dijkstra_red()
        self.__clear_board()
        self.occupiedTiles.clear()
        self.isSwapRuleDone = False

    def change_transformable(self, canvas, x, y, width):
        self.board.change_transformable(canvas, x, y, width)

    def __place_hex_on_y(self, x, y, color):
        self.y_board_red.place_hex(x, y, color)
        self.y_board_blue.place_hex(x, y, color)#TODO: MADIG
