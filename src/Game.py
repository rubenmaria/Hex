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
        self.__root = root
        self.__playersTurn = "red"
        self.__playerBegins = "red"
        self.__isSwapRule = False
        self.__redComputerLevel = 1
        self.__blueComputerLevel = 1
        self.__isRedComputer = False
        self.__isBlueComputer = False
        self.board = board
        self.__canvas = canvas
        self.__destinationLength = 10
        self.__visited = set()
        self.occupiedTiles = set()
        self.y_board_red = YBoard(11, "red")
        self.y_board_blue = YBoard(11, "blue")
        self.__computer = Ai(board, canvas, self.occupiedTiles, self.y_board_red, self.y_board_blue)
        self.__isSwapRuleDone = False
        self.__undoStack = []
        self.__redoStack = []
        self.gui = Gui(canvas, root, self.apply, self.restart_game, self.resize)
        self.__update_ai()
    
    def resize(self):
        width = self.__root.winfo_width()
        height = self.__root.winfo_height()
        self.__canvas.delete(tk.ALL)
        self.__canvas.config(width=width, height=height)
        self.change_transformable(width * 1 / 20, height * 1 / 15, width / 2 + width / 15)

    def draw(self):
        self.board.draw(self.__canvas)

    def make_move(self, row, col, color):
        is_color_red = color == "red"
        is_color_blue = color == "blue"
        prev_color = self.board.tiles[row][col].fillColor
        self.board.tiles[row][col].set_color(self.__canvas, color)
        if is_color_red:
            self.__place_hex_on_y(row, col, "red")
            self.__computer.graph_blue[row + 1][col + 1].set_color("enemy", "red")
            self.__computer.graph_red[row + 1][col + 1].set_color("friendly", "red")
            self.__playersTurn = "blue"
            self.occupiedTiles.add((row, col))
            self.__undoStack.append((row, col, "red"))
            self.is_red_winner(self.board.tiles)
        elif is_color_blue:
            self.__place_hex_on_y(row, col, "blue")
            self.__computer.graph_blue[row + 1][col + 1].set_color("friendly", "blue")
            self.__computer.graph_red[row + 1][col + 1].set_color("enemy", "blue")
            self.__playersTurn = "red"
            self.occupiedTiles.add((row, col))
            self.__undoStack.append((row, col, "blue"))
            self.is_blue_winner(self.board.tiles)
        else:
            self.occupiedTiles.remove((row, col))
            self.board.tiles[row][col].set_color(self.__canvas, "white")
            self.__computer.graph_blue[row + 1][col + 1].set_color("impartial", "white")
            self.__computer.graph_red[row + 1][col + 1].set_color("impartial", "white")
            self.__redoStack.append((row, col, prev_color))

    def game_over(self, color):
        if color == "red":
            messagebox.showinfo("Game Over", "Red has won!")
        else:
            messagebox.showinfo("Game Over", "Blue has won!")
        self.restart_game()

    def __update_ai(self):
        #print(self.__ai.y_eval(self.y_board_red)[0].get_y(0, 0))

        if not self.__isRedComputer and not self.__isBlueComputer:
            self.__canvas.after(1, self.__update_ai)
            return
        self.is_red_winner(self.board.tiles)
        self.is_blue_winner(self.board.tiles)
        second_move = len(self.occupiedTiles) == 1
        first_move = len(self.occupiedTiles) == 0
        swap_rule = (second_move and self.__isSwapRule) and not self.__isSwapRuleDone
        if swap_rule and self.__playersTurn == "red" and self.__isBlueComputer and not self.__isRedComputer:
            msg = messagebox.askyesno("Swap Rule", "Do you want to Swap?")
            if msg:
                move = next(iter(self.occupiedTiles))
                row = move[0]
                col = move[1]
                self.__undoStack.pop()
                self.make_move(row, col, "red")
            self.__isSwapRuleDone = True
        elif swap_rule and self.__playersTurn == "blue" and not self.__isBlueComputer and self.__isRedComputer:
            msg = messagebox.askyesno("Swap Rule", "Do you want to Swap?")
            if msg:
                move = next(iter(self.occupiedTiles))
                row = move[0]
                col = move[1]
                self.__undoStack.pop()
                self.make_move(row, col, "blue")
            self.__isSwapRuleDone = True
        elif (self.__playersTurn == "red" and self.__isRedComputer and not first_move
              and not swap_rule):
            level = self.__redComputerLevel
            self.__root.title("Hex | Red Computer: Let me think...")
            tile = self.__computer.minimax(list(), "red", level, level, -m.inf, +m.inf, True, list())
            #tile = self.__ai.monte_carlo("red")
            row = tile[0]
            col = tile[1]
            self.make_move(row, col, "red")
        elif (self.__playersTurn == "blue" and self.__isBlueComputer and not first_move
              and not swap_rule):
            # tile = self.__ai.monte_carlo("blue")
            level = self.__blueComputerLevel
            self.__root.title("Hex | Blue Computer: Let me think...")
            tile = self.__computer.minimax(list(), "blue", level, level, -m.inf, +m.inf, True, list())
            row = tile[0]
            col = tile[1]
            self.make_move(row, col, "blue")
        elif self.__playersTurn == "blue" and self.__isBlueComputer and first_move and not self.__isSwapRule:
            self.make_move(5, 6, "blue")
        elif self.__playersTurn == "red" and self.__isRedComputer and first_move and not self.__isSwapRule:
            self.make_move(5, 6, "red")
        elif self.__playersTurn == "blue" and self.__isBlueComputer and first_move and self.__isSwapRule:
            row = 9
            col = 9
            self.make_move(row, col, "blue")
        elif self.__playersTurn == "red" and self.__isRedComputer and first_move and self.__isSwapRule:
            row = 9
            col = 9
            self.make_move(row, col, "red")
        elif self.__playersTurn == "red" and self.__isRedComputer and swap_rule:
            move = next(iter(self.occupiedTiles))
            row = move[0]
            col = move[1]
            if row in range(3, 8) and col in range(3, 8):
                messagebox.showinfo("Swap Rule", "Red Swapped your move!")
                self.board.tiles[row][col].set_color(self.__canvas, "red")
                self.__playersTurn = "blue"
            else:
                level = self.__redComputerLevel
                self.__root.title("Hex | Red Computer: Let me think...")
                tile = self.__computer.minimax(list(), "red", level, level, -m.inf, +m.inf, True, list())
                # tile = self.__ai.monte_carlo("red")
                row = tile[0]
                col = tile[1]
                self.make_move(row, col, "red")
            self.__isSwapRuleDone = True
        elif self.__playersTurn == "blue" and self.__isBlueComputer and swap_rule:
            move = next(iter(self.occupiedTiles))
            row = move[0]
            col = move[1]
            if row in range(3, 8) and col in range(3, 8):
                messagebox.showinfo("Swap Rule", "Blue Swapped your move!")
                self.board.tiles[row][col].set_color(self.__canvas, "blue")
                self.__playersTurn = "red"
            else:
                level = self.__blueComputerLevel
                self.__root.title("Hex | Blue Computer: Let me think...")
                tile = self.__computer.minimax(list(), "blue", level, level, -m.inf, +m.inf, True, list())
                row = tile[0]
                col = tile[1]
                self.make_move(row, col, "blue")
            self.__isSwapRuleDone = True
        self.__canvas.after(1, self.__update_ai)

    def mouse_input_config(self):
        self.__canvas.bind("<Button-1>", self.__button1_callback)

    def undo(self, event):
        if len(self.__undoStack) <= 0:
            return
        to_remove = self.__undoStack.pop()
        if to_remove[2] == "red":
            self.__playersTurn = "blue"
        else:
            self.__playersTurn = "red"
        self.make_move(to_remove[0], to_remove[1], "white")

    def redo(self, event):
        if len(self.__redoStack) <= 0:
            return
        to_add = self.__redoStack.pop()
        self.make_move(to_add[0], to_add[1], to_add[2])

    def __button1_callback(self, event):
        if (self.__canvas.find_withtag(tk.CURRENT)
                and self.__canvas.itemcget(tk.CURRENT, 'fill') == 'white'):
            cur_tag = self.__canvas.itemcget(tk.CURRENT, 'tag')
            if self.__playersTurn == "red":
                if self.__isRedComputer or cur_tag.find('-') == -1:
                    return
                index_dash = cur_tag.find('-')
                index_space = cur_tag.find(' ')
                row = int(cur_tag[0:index_dash])
                col = int(cur_tag[index_dash + 1:index_space])
                self.make_move(row, col, "red")
                self.__root.title("Hex | Blue's turn!")
                self.__redoStack.clear()
            else:
                if self.__isBlueComputer or cur_tag.find('-') == -1:
                    return
                index_dash = cur_tag.find('-')
                index_space = cur_tag.find(' ')
                row = int(cur_tag[0:index_dash])
                col = int(cur_tag[index_dash + 1:index_space])
                self.make_move(row, col, "blue")
                self.__root.title("Hex | Red's turn!")
                self.__redoStack.clear()

    def is_red_winner(self, tiles):
        for row in range(11):
            if self.__is_tile_connected_red(row, 0, tiles):
                self.__visited.clear()
                self.game_over("red")
                return
            self.__visited.clear()
        return

    def is_blue_winner(self, tiles):
        for col in range(11):
            if self.__is_tile_connected_blue(0, col, tiles):
                self.__visited.clear()
                self.game_over("blue")
                return
            self.__visited.clear()
        return

    def __is_tile_connected_red(self, row, col, tiles):
        self.__visited.add((row, col))
        if col > self.__destinationLength:
            return True
        if row > self.__destinationLength or col < 0 or row < 0:
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
        if row > self.__destinationLength:
            return True
        if col > self.__destinationLength or row < 0 or col < 0:
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
        self.__isBlueComputer = self.gui.isBlueComputer.get()
        self.__isRedComputer = self.gui.isRedComputer.get()
        self.__isSwapRule = self.gui.isSwapRule.get()
        self.__blueComputerLevel = self.gui.blueComputerLevel.get()
        self.__redComputerLevel = self.gui.redComputerLevel.get()
        if self.gui.isRedBeginning.get():
            self.__playerBegins = "red"
        else:
            self.__playerBegins = "blue"
        self.__playersTurn = self.__playerBegins

    def restart_game(self):
        self.gui.blueComputerLevel.set(value=1)
        self.gui.redComputerLevel.set(value=1)
        self.gui.isRedBeginning.set(value=True)
        self.gui.isRedComputer.set(value=False)
        self.gui.isBlueComputer.set(value=False)
        self.gui.isSwapRule.set(value=False)
        self.apply()
        self.__computer.setup_dijkstra_blue()
        self.__computer.setup_dijkstra_red()
        self.__clear_board()
        self.occupiedTiles.clear()
        self.__isSwapRuleDone = False

    def change_transformable(self, x, y, width):
        self.board.change_transformable(self.__canvas, x, y, width)

    def __place_hex_on_y(self, x, y, color):
        self.y_board_red.place_hex(x, y, color)
        self.y_board_blue.place_hex(x, y, color)
