import tkinter as tk
from GUI import Gui
from Board import Board
from Game import Game
WIDTH, HEIGHT = 1000, 600


def main():  # TODO: Which players turn represented as general information as tkinter label
    root = tk.Tk()
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
    board = Board(50, 100, 500, canvas)
    game = Game(board, canvas)
    game.mouse_input_config()
    gui = Gui(50 + board.width, board.offsetYRect, canvas, root, game)
    gui.draw()
    game.draw()
    canvas.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
