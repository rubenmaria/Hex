import tkinter as tk
from tkinter import font as tkf
from Vector2 import Vec2


class OptionFrame:

    def __init__(self, root, x, y):
        # self.master = tk.Frame(root)
        # self.master.pack(side=tk.RIGHT)
        self.currCheckboxIndex = 0
        self.__width = 0
        self.__firstWidth = True
        self.__position = Vec2(x, y)
        self.__rectSize = Vec2(0, 0)
        self.__master = root
        self.__offsetY = y
        self.states = []
        self.__font = None
        self.__coordinates = []
        self.__checkboxes = []

    def add_checkbox(self,  text, color, size, var, **kwargs):
        self.__font = tkf.Font(family="Fixedsys", size=size)
        x = self.__position.x
        y = self.__offsetY
        cmd = kwargs.get("command")

        if cmd is not None:
            box = tk.Checkbutton(self.__master, text=text, variable=var, font=self.__font,
                               bg="white", fg=color, command=cmd)
        else:
            box = tk.Checkbutton(self.__master, text=text, variable=var, font=self.__font,
                                    bg="white", fg=color)

        box.place(x=x, y=y)
        box.update()
        width = box.winfo_reqwidth()
        if self.__firstWidth:
            self.__width = box.winfo_reqwidth()
            self.__firstWidth = False
        self.__rectSize.y = box.winfo_reqheight()
        self.__offsetY += self.__rectSize.y + 2
        self.__coordinates.append(x - 2)
        self.__coordinates.append(y - 2)
        self.__coordinates.append(x + width)
        self.__coordinates.append(y + self.__rectSize.y)
        self.__update_width()
        self.__checkboxes.append(box)
        self.currCheckboxIndex = len(self.__checkboxes) - 1

    def draw(self, canvas):
        for i in range(0, len(self.__coordinates), 4):
            canvas.create_rectangle(self.__coordinates[i], self.__coordinates[i + 1],
                                    self.__width, self.__coordinates[i + 3], width=1)

    def add_slider(self, start, end, orient, text, canvas):
        x = self.__position.x
        y = self.__offsetY
        slider = tk.Scale(self.__master, from_=start, to=end, orient=orient)
        slider.update()
        s_height = slider.winfo_reqheight() / 2
        s_width = slider.winfo_reqwidth()
        text = canvas.create_text(x, y + s_height, text=text, fill="black", font=self.__font, anchor=tk.NW)
        bounds = canvas.bbox(text)
        width = bounds[2] - bounds[0]
        slider.place(x=x + width, y=y)
        if self.__firstWidth:
            self.__width = width + s_width
            self.__firstWidth = False
        self.__coordinates.append(x - 2)
        self.__coordinates.append(y - 2)
        self.__coordinates.append(x + width + s_width)
        self.__coordinates.append(y + s_height * 2)
        self.__offsetY += s_height * 2
        self.__update_width()

    def add_gap(self, size_y):
        self.__offsetY += size_y

    def add_button(self, text, cmd):
        x = self.__position.x
        y = self.__offsetY
        but = tk.Button(self.__master, text=text, font=self.__font, anchor=tk.N, command=cmd)
        width = but.winfo_reqwidth()
        if self.__firstWidth:
            self.__width = but.winfo_reqwidth()
            self.__firstWidth = False
        height = but.winfo_reqheight()
        width_half = (self.__width - self.__position.x) / 4
        but.config(anchor=tk.N)
        but.place(x=x + width_half, y=y)

    def __update_width(self):
        width = self.__coordinates[2]
        for i in range(0, len(self.__coordinates), 4):
            if width < self.__coordinates[i + 2]:
                width = self.__coordinates[i + 2]
        self.__width = width

    def select(self, index):
        self.__checkboxes[index].select()

    def deselect(self, index):
        self.__checkboxes[index].select()