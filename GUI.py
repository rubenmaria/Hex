import tkinter as tk


class Gui:
    def __init__(self, canvas, root, game):
        self.__game = game
        self.resize_factor = 16 / 600
        self.__root = root
        self.__canvas = canvas
        self.__blueComputerLevel = tk.IntVar(value=1)
        self.__redComputerLevel = tk.IntVar(value=1)
        self.__isRedBeginning = tk.BooleanVar(value=True)
        self.__isRedComputer = tk.BooleanVar(value=False)
        self.__isBlueComputer = tk.BooleanVar(value=False)
        self.__isSwapRule = tk.BooleanVar(value=False)
        self.__menuBar = tk.Menu(root)
        self.__menuRed = tk.Menu(self.__menuBar, tearoff=0)
        self.__menuLevelRed = tk.Menu(self.__menuRed, tearoff=0)
        self.__menuBlue = tk.Menu(self.__menuBar, tearoff=0)
        self.__menuLevelBlue = tk.Menu(self.__menuBlue, tearoff=0)
        self.__menuGame = tk.Menu(self.__menuBar, tearoff=0)
        self.__init_menu()

    def __init_menu(self):
        self.__menuRed.add_radiobutton(label="Player", value=0, var=self.__isRedComputer)
        self.__menuRed.add_radiobutton(label="Computer", value=1, variable=self.__isRedComputer)
        self.__menuLevelRed.add_radiobutton(label="Level 1", value=1, variable=self.__redComputerLevel)
        self.__menuLevelRed.add_radiobutton(label="Level 2", value=2, variable=self.__redComputerLevel)
        self.__menuLevelRed.add_radiobutton(label="Level 3", value=3, variable=self.__redComputerLevel)
        self.__menuRed.add_cascade(label="Computer Level", menu=self.__menuLevelRed)
        self.__menuBar.add_cascade(label="Red", menu=self.__menuRed)
        self.__menuBlue.add_radiobutton(label="Player", value=0, var=self.__isBlueComputer)
        self.__menuBlue.add_radiobutton(label="Computer", value=1, var=self.__isBlueComputer)
        self.__menuLevelBlue.add_radiobutton(label="Level 1", value=1, var=self.__blueComputerLevel)
        self.__menuLevelBlue.add_radiobutton(label="Level 2", value=2, var=self.__blueComputerLevel)
        self.__menuLevelBlue.add_radiobutton(label="Level 3", value=3, var=self.__blueComputerLevel)
        self.__menuGame.add_radiobutton(label="Red begins", value=1, var=self.__isRedBeginning)
        self.__menuGame.add_radiobutton(label="Blue begins", value=0, var=self.__isRedBeginning)
        self.__menuGame.add_checkbutton(label="Swap rule", var=self.__isSwapRule, )
        self.__menuBlue.add_cascade(label="Computer Level", menu=self.__menuLevelBlue)
        self.__menuBar.add_cascade(label="Blue", menu=self.__menuBlue)
        self.__menuBar.add_cascade(label="Game", menu=self.__menuGame)
        self.__menuBar.add_command(label="Apply Changes", command=self.__apply)
        self.__menuBar.add_command(label="New Game", command=self.__new_game)
        self.__root.config(menu=self.__menuBar)

    def __apply(self):
        self.__game.redComputerLevel = self.__redComputerLevel.get()
        self.__game.isRedComputer = self.__isRedComputer.get()
        self.__game.blueComputerLevel = self.__blueComputerLevel.get()
        self.__game.isBlueComputer = self.__isBlueComputer.get()
        self.__game.isSwapRule = self.__isSwapRule.get()
        if self.__isRedBeginning.get():
            self.__game.playerBegins = "red"
        else:
            self.__game.playerBegins = "blue"

    def __new_game(self):
        self.__blueComputerLevel.set(value=1)
        self.__redComputerLevel.set(value=1)
        self.__isRedBeginning.set(value=True)
        self.__isRedComputer.set(value=False)
        self.__isBlueComputer.set(value=False)
        self.__isSwapRule.set(value=False)
        self.__apply()
        self.__game.restart_game()
