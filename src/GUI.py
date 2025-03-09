import tkinter as tk


class Gui:
    def __init__(self, canvas, root, apply_method, restart_method, resize_method):
        self.__root = root
        self.__canvas = canvas
        self.blueComputerLevel = tk.IntVar(value=1)
        self.redComputerLevel = tk.IntVar(value=1)
        self.isRedBeginning = tk.BooleanVar(value=True)
        self.isRedComputer = tk.BooleanVar(value=False)
        self.isBlueComputer = tk.BooleanVar(value=False)
        self.isSwapRule = tk.BooleanVar(value=False)
        self.__menuBar = tk.Menu(root)
        self.__menuRed = tk.Menu(self.__menuBar, tearoff=0)
        self.__menuLevelRed = tk.Menu(self.__menuRed, tearoff=0)
        self.__menuBlue = tk.Menu(self.__menuBar, tearoff=0)
        self.__menuLevelBlue = tk.Menu(self.__menuBlue, tearoff=0)
        self.__menuGame = tk.Menu(self.__menuBar, tearoff=0)
        self.__init_menu(apply_method, restart_method, resize_method)

    def __init_menu(self, apply_method, restart_method, resize_method):
        self.__menuRed.add_radiobutton(label="Player", value=0, var=self.isRedComputer)
        self.__menuRed.add_radiobutton(label="Computer", value=1, variable=self.isRedComputer)
        self.__menuLevelRed.add_radiobutton(label="Level 1", value=1, variable=self.redComputerLevel)
        self.__menuLevelRed.add_radiobutton(label="Level 2", value=2, variable=self.redComputerLevel)
        self.__menuLevelRed.add_radiobutton(label="Level 3", value=3, variable=self.redComputerLevel)
        self.__menuRed.add_cascade(label="Computer Level", menu=self.__menuLevelRed)
        self.__menuBar.add_cascade(label="Red", menu=self.__menuRed)
        self.__menuBlue.add_radiobutton(label="Player", value=0, var=self.isBlueComputer)
        self.__menuBlue.add_radiobutton(label="Computer", value=1, var=self.isBlueComputer)
        self.__menuLevelBlue.add_radiobutton(label="Level 1", value=1, var=self.blueComputerLevel)
        self.__menuLevelBlue.add_radiobutton(label="Level 2", value=2, var=self.blueComputerLevel)
        self.__menuLevelBlue.add_radiobutton(label="Level 3", value=3, var=self.blueComputerLevel)
        self.__menuGame.add_radiobutton(label="Red begins", value=1, var=self.isRedBeginning)
        self.__menuGame.add_radiobutton(label="Blue begins", value=0, var=self.isRedBeginning)
        self.__menuGame.add_checkbutton(label="Swap rule", var=self.isSwapRule, )
        self.__menuBlue.add_cascade(label="Computer Level", menu=self.__menuLevelBlue)
        self.__menuBar.add_cascade(label="Blue", menu=self.__menuBlue)
        self.__menuBar.add_cascade(label="Game", menu=self.__menuGame)
        self.__menuBar.add_command(label="Apply Changes", command=apply_method)
        self.__menuBar.add_command(label="Restart Game", command=restart_method)
        self.__menuBar.add_command(label="Resize Game", command=resize_method)
        self.__root.config(menu=self.__menuBar)


