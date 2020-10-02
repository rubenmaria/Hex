import tkinter as tk
from tkinter import font as tkf
from Vector2 import Vec2


class OptionFrame:

    def __init__(self, root, x, y, window_width, window_height, font_size):
        self.currCheckboxIndex = 0
        self.__font_size = font_size
        self.__window_width = window_width
        self.__window_height = window_height
        self.__slider_length = 30
        self.__resize_font_size_factor = font_size / (window_width + window_height)
        self.__resize_width_factor = self.__slider_length / window_width
        self.__width = 0
        self.__height = 0
        self.__firstWidth = True
        self.__position = Vec2(x, y)
        self.__rectSize = Vec2(0, 0)
        self.__master = root
        self.__offsetY = y
        self.states = []
        self.__font = None
        self.__all_widgets = []
        self.__coordinates = []
        self.__checkboxes = []
        self.__buttons = []
        self.__sliders = []
        self.__current_gui_index = 0
        self.__gap_positions_and_size = []
        self.__font = tkf.Font(family="Fixedsys", size=self.__font_size)

    def add_checkbox(self,  text, color, var, **kwargs):
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
        self.__height += box.winfo_reqheight()
        if self.__firstWidth:
            self.__width = box.winfo_reqwidth()
            self.__firstWidth = False
        self.__rectSize.y = box.winfo_reqheight()
        self.__offsetY += self.__rectSize.y + 2
        self.__coordinates.append(x - 2)
        self.__coordinates.append(y - 2)
        self.__coordinates.append(x + width)
        self.__coordinates.append(y + self.__rectSize.y)
        self.__update()
        self.__checkboxes.append(box)
        self.__all_widgets.append(box)
        self.currCheckboxIndex = len(self.__checkboxes) - 1
        self.__current_gui_index += 1

    def draw(self, canvas):
        for i in range(0, len(self.__coordinates), 4):
            canvas.create_rectangle(self.__coordinates[i], self.__coordinates[i + 1],
                                    self.__width, self.__coordinates[i + 3], width=1)

    def add_slider(self, start, end, orient, text, canvas):
        x = self.__position.x
        y = self.__offsetY
        slider = tk.Scale(self.__master, from_=start, to=end, orient=orient, sliderlength=self.__slider_length)
        slider.update()
        s_height = slider.winfo_reqheight() / 2
        s_width = slider.winfo_reqwidth()
        text = canvas.create_text(x, y + s_height, text=text, fill="black", font=self.__font, anchor=tk.NW)
        bounds = canvas.bbox(text)
        width = bounds[2] - bounds[0]
        self.__height += bounds[3] - bounds[1]
        slider.place(x=x + width, y=y)
        if self.__firstWidth:
            self.__width = width + s_width
            self.__firstWidth = False
        self.__coordinates.append(x - 2)
        self.__coordinates.append(y - 2)
        self.__coordinates.append(x + width + s_width)
        self.__coordinates.append(y + s_height * 2)
        self.__offsetY += s_height * 2
        self.__update()
        self.__sliders.append(slider)
        self.__current_gui_index += 1
        self.__all_widgets.append(slider)

    def add_gap(self, size_y):
        self.__offsetY += size_y
        self.__gap_positions_and_size.append((self.__current_gui_index, size_y))
        self.__height += size_y

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
        self.__buttons.append(but)
        self.__current_gui_index += 1
        self.__height += height
        self.__all_widgets.append(but)

    def __update(self):
        width = self.__coordinates[2]
        for i in range(0, len(self.__coordinates), 4):
            if width < self.__coordinates[i + 2]:
                width = self.__coordinates[i + 2]
        self.__width = width

    def select(self, index):
        self.__checkboxes[index].select()

    def deselect(self, index):
        self.__checkboxes[index].select()

    def resize(self, x, y, width, height, canvas):
        pass


