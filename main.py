import tkinter as tk
import time as t
from GUI import Gui
from Board import Board
from Game import Game
WIDTH, HEIGHT = 1100, 600


def main():
    root = tk.Tk()
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
    board = Board(WIDTH * 1 / 22, HEIGHT * 1/6, WIDTH * 5 / 11, canvas)
    game = Game(board, canvas)
    game.mouse_input_config()
    gui = Gui(WIDTH * 1 / 22 + board.width, board.offsetYRect, WIDTH, HEIGHT , canvas, root, game)
    gui.draw()
    game.draw()
    canvas.pack()

    def resizer(event):
        width, height = event.width - 4, event.height - 4
        if WIDTH == width and HEIGHT == height:
            return
        canvas.delete(tk.ALL)
        canvas.config(width=width, height=height)
        game.change_transformable(canvas, width * 1 / 22, height * 1/6, width * 5 / 11)
        gui.resize(width * 1 / 22 + board.width, board.offsetYRect, width, height, canvas)

    canvas.update_idletasks()
    canvas.after(1)
    root.bind("<Configure>", resizer)
    root.mainloop()


if __name__ == '__main__':
    main()
