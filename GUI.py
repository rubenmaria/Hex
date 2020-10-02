from OptionFrame import OptionFrame
import tkinter as tk
import math as m


class Gui:
    def __init__(self, x, y, width, height, canvas, root, game):
        self.__game = game
        self.resize_factor = 16 / 600
        self.__optionFrame = OptionFrame(root, x, y, width, height, 16)
        self.__root = root
        self.__canvas = canvas
        self.__isRedBeginning = tk.BooleanVar(value=False)
        self.__isBlueBeginning = tk.BooleanVar(value=False)
        self.__isRedPlayer = tk.BooleanVar(value=False)
        self.__isRedComputer = tk.BooleanVar(value=False)
        self.__isBluePlayer = tk.BooleanVar(value=False)
        self.__isBlueComputer = tk.BooleanVar(value=False)
        self.__isSwapRule = tk.BooleanVar(value=False)
        self.__lastRedBeginning = True
        self.__lastRedPlayer = True
        self.__lastBluePlayer = True
        self.__init_option_frame()

    def __init_option_frame(self):
        self.__optionFrame.add_checkbox("Red: Player", "black", self.__isRedPlayer,
                                        command=self.processing_red_beginning_player_input)
        self.__optionFrame.select(self.__optionFrame.currCheckboxIndex)
        self.__optionFrame.add_checkbox("Red: Computer", "black", self.__isRedComputer,
                                        command=self.processing_red_beginning_player_input)
        self.__optionFrame.add_slider(1, 3, tk.HORIZONTAL, "Level:", self.__canvas)
        self.__optionFrame.add_gap(20)
        self.__optionFrame.add_checkbox("Blue: Player", "black", self.__isBluePlayer)
        self.__optionFrame.select(self.__optionFrame.currCheckboxIndex)
        self.__optionFrame.add_checkbox("Blue: Computer", "black", self.__isBlueComputer)
        self.__optionFrame.add_slider(1, 3, tk.HORIZONTAL, "Level:", self.__canvas)
        self.__optionFrame.add_gap(20)
        self.__optionFrame.add_checkbox("Red begins", "black",  self.__isRedBeginning,
                                        command=self.processing_beginning_color_input)
        self.__optionFrame.select(self.__optionFrame.currCheckboxIndex)
        self.__optionFrame.add_checkbox("Blue begins", "black", self.__isBlueBeginning,
                                        command=self.processing_beginning_color_input)
        self.__optionFrame.add_gap(20)
        self.__optionFrame.add_checkbox("swap rule", "black", self.__isSwapRule)
        self.__optionFrame.select(self.__optionFrame.currCheckboxIndex)
        self.__optionFrame.add_gap(20)
        self.__optionFrame.add_button("Apply", self.__apply)

    def draw(self):
        self.__optionFrame.draw(self.__canvas)

    def processing_beginning_color_input(self):
        if self.__isRedBeginning.get() and self.__isBlueBeginning.get():
            if self.__lastRedBeginning:
                self.__isRedBeginning.set(tk.FALSE)
                self.__lastRedBeginning = False
            else:
                self.__isBlueBeginning.set(tk.FALSE)
                self.__lastRedBeginning = True

        if self.__isRedBeginning.get():
            self.__game.playerBegins = "red"
        else:
            self.__game.playerBegins = "blue"

    def processing_red_beginning_player_input(self):
        if self.__isRedPlayer.get() and self.__isRedComputer.get():
            if self.__lastRedPlayer:
                self.__isRedPlayer.set(tk.FALSE)
                self.__lastRedPlayer = False
            else:
                self.__isRedComputer.set(tk.FALSE)
                self.__lastRedPlayer = True

    def __apply(self):
        self.__game.apply()

    def resize(self, x, y, width, height, canvas):
        self.__optionFrame.resize(x, y, width, height, canvas)