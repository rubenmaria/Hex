import tkinter as tk
import time as t
from GUI import Gui
from Board import Board
from Game import Game
WIDTH, HEIGHT = 1100, 600


def main():
    root = tk.Tk()
    root.title("Hex")
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
    board = Board(WIDTH * 1 / 12, HEIGHT * 1/10, WIDTH / 2, canvas)
    game = Game(board, canvas)
    game.mouse_input_config()
    gui = Gui(canvas, root, game)
    game.draw()
    canvas.pack()

    def resizer(event):
        width, height = event.width - 4, event.height - 4
        if WIDTH == width and HEIGHT == height:
            return
        canvas.delete(tk.ALL)
        canvas.config(width=width, height=height)
        game.change_transformable(canvas, width * 1 / 12, height * 1/10, width / 2 + width / 10)

    canvas.update_idletasks()
    canvas.after(1)
    root.bind("<Configure>", resizer)
    root.mainloop()


if __name__ == '__main__':
    main()
