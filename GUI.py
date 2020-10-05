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
        self.__blue_changed = False
        self.__game_changed = False
        self.__red_changed = False
        self.__apply_changes_drawn = False
        self.__lastRedBeginning = True
        self.__lastRedPlayer = True
        self.__lastBluePlayer = True
        self.__currentGameSettings = [self.__isRedBeginning.get(), self.__isSwapRule.get()]
        self.__currentBlueSettings = [self.__isBlueComputer.get(), self.__blueComputerLevel.get()]
        self.__currentRedSettings = [self.__isRedComputer.get(), self.__redComputerLevel.get()]
        self.__menuBar = tk.Menu(root)
        self.__menuRed = tk.Menu(self.__menuBar, tearoff=0)
        self.__menuLevelRed = tk.Menu(self.__menuRed, tearoff=0)
        self.__menuBlue = tk.Menu(self.__menuBar, tearoff=0)
        self.__menuLevelBlue = tk.Menu(self.__menuBlue, tearoff=0)
        self.__menuGame = tk.Menu(self.__menuBar, tearoff=0)
        self.__init_menu()

    def __init_menu(self):
        self.__menuRed.add_radiobutton(label="Player", value=0, var=self.__isRedComputer, command=self.process_red)
        self.__menuRed.add_radiobutton(label="Computer", value=1,
                                       variable=self.__isRedComputer, command=self.process_red)
        self.__menuLevelRed.add_radiobutton(label="Level 1", value=1,
                                            variable=self.__redComputerLevel, command=self.process_red)
        self.__menuLevelRed.add_radiobutton(label="Level 2", value=2,
                                            variable=self.__redComputerLevel, command=self.process_red)
        self.__menuLevelRed.add_radiobutton(label="Level 3", value=3,
                                            variable=self.__redComputerLevel, command=self.process_red)
        self.__menuRed.add_cascade(label="Computer Level", menu=self.__menuLevelRed)
        self.__menuBar.add_cascade(label="Red", menu=self.__menuRed)
        self.__menuBlue.add_radiobutton(label="Player", value=0, var=self.__isBlueComputer,
                                        command=self.process_blue)
        self.__menuBlue.add_radiobutton(label="Computer", value=1, var=self.__isBlueComputer,
                                        command=self.process_blue)
        self.__menuLevelBlue.add_radiobutton(label="Level 1", value=1, var=self.__blueComputerLevel,
                                             command=self.process_blue)
        self.__menuLevelBlue.add_radiobutton(label="Level 2", value=2, var=self.__blueComputerLevel,
                                             command=self.process_blue)
        self.__menuLevelBlue.add_radiobutton(label="Level 3", value=3, var=self.__blueComputerLevel,
                                             command=self.process_blue)
        self.__menuGame.add_radiobutton(label="Red begins", value=1, var=self.__isRedBeginning,
                                        command=self.process_game)
        self.__menuGame.add_radiobutton(label="Blue begins", value=0, var=self.__isRedBeginning,
                                        command=self.process_game)
        self.__menuGame.add_checkbutton(label="Swap rule", var=self.__isSwapRule, command=self.process_game)
        self.__menuBlue.add_cascade(label="Computer Level", menu=self.__menuLevelBlue)
        self.__menuBar.add_cascade(label="Blue", menu=self.__menuBlue)
        self.__menuBar.add_cascade(label="Game", menu=self.__menuGame)
        self.__root.config(menu=self.__menuBar)

    def process_game(self):
        if self.__currentGameSettings[0] != self.__isRedBeginning.get() and not self.__apply_changes_drawn:
            self.__menuBar.add_command(label="Apply Changes", command=self.__apply)
            self.__apply_changes_drawn = True
            self.__game_changed = True

        if self.__currentGameSettings[1] != self.__isSwapRule.get() and not self.__apply_changes_drawn:
            self.__menuBar.add_command(label="Apply Changes", command=self.__apply)
            self.__apply_changes_drawn = True
            self.__game_changed = True

        if (self.__currentGameSettings[0] == self.__isRedBeginning.get()
                and self.__currentGameSettings[1] == self.__isSwapRule.get()):
            self.__game_changed = False

        if not self.__blue_changed and not self.__red_changed and not self.__game_changed:
            self.__menuBar.delete(4)
            self.__apply_changes_drawn = False

        if self.__isRedBeginning.get():
            self.__game.playerBegins = "red"
        else:
            self.__game.playerBegins = "blue"
        self.__game.isSwapRule = self.__isSwapRule.get()

    def process_blue(self):
        if self.__currentBlueSettings[0] != self.__isBlueComputer.get() and not self.__apply_changes_drawn:
            self.__menuBar.add_command(label="Apply Changes", command=self.__apply)
            self.__apply_changes_drawn = True
            self.__blue_changed = True

        if self.__currentBlueSettings[1] != self.__blueComputerLevel.get() and not self.__apply_changes_drawn:
            self.__menuBar.add_command(label="Apply Changes", command=self.__apply)
            self.__apply_changes_drawn = True
            self.__blue_changed = True

        if (self.__currentBlueSettings[0] == self.__isBlueComputer.get()
                and self.__currentBlueSettings[1] == self.__blueComputerLevel.get()):
            self.__blue_changed = False

        if not self.__blue_changed and not self.__red_changed and not self.__game_changed:
            self.__menuBar.delete(4)
            self.__apply_changes_drawn = False

        self.__game.blueComputerLevel = self.__blueComputerLevel.get()
        self.__game.isBlueComputer = self.__isBlueComputer.get()

    def process_red(self):
        if self.__currentRedSettings[0] != self.__isRedComputer.get() and not self.__apply_changes_drawn:
            self.__menuBar.add_command(label="Apply Changes", command=self.__apply)
            self.__apply_changes_drawn = True
            self.__red_changed = True

        if self.__currentRedSettings[1] != self.__redComputerLevel.get() and not self.__apply_changes_drawn:
            self.__menuBar.add_command(label="Apply Changes", command=self.__apply)
            self.__apply_changes_drawn = True
            self.__red_changed = True

        if (self.__currentRedSettings[0] == self.__isRedComputer.get()
                and self.__currentRedSettings[1] == self.__redComputerLevel.get()):
            self.__red_changed = False

        if not self.__blue_changed and not self.__red_changed and not self.__game_changed:
            self.__menuBar.delete(4)
            self.__apply_changes_drawn = False

        self.__game.redComputerLevel = self.__redComputerLevel.get()
        self.__game.isRedComputer = self.__isRedComputer.get()

    def __apply(self):
        self.__menuBar.delete(4)
        self.__apply_changes_drawn = False
        self.__game_changed = False
        self.__blue_changed = False
        self.__red_changed = False
        self.__currentGameSettings[0] = self.__isRedBeginning.get()
        self.__currentGameSettings[1] = self.__isSwapRule.get()
        self.__currentBlueSettings[0] = self.__isBlueComputer.get()
        self.__currentBlueSettings[1] = self.__blueComputerLevel.get()
        self.__currentRedSettings[0] = self.__isRedComputer.get()
        self.__currentRedSettings[1] = self.__redComputerLevel.get()
        self.__game.apply()
