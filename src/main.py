import tkinter as tk
import time as t
from GUI import Gui
from Board import Board
from Game import Game
WIDTH, HEIGHT = 1200, 700


def main():
    root = tk.Tk()
    root.title("Hex")
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
    board = Board(WIDTH * 1 / 12, HEIGHT * 1/10, WIDTH / 2, canvas)
    game = Game(root, board, canvas)
    game.mouse_input_config()
    game.draw()
    canvas.pack()
    root.bind("<Control-z>", game.undo)
    root.bind("<Control-y>", game.redo)
    canvas.update_idletasks()
    canvas.after(1)
    root.mainloop()


if __name__ == '__main__':
    main()
