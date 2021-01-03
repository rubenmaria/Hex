import math as m
import tkinter.font as tkf
from Vector2 import Vec2


class Hexagon:
    def __init__(self, width, x, y, outline_color, fill_color, outline_thickness, tag):  # x - left most edge, y - top
        radius = (width / 2) / m.cos(m.radians(30))
        self.width = width  # distance between the left most edge and the center point
        self.height = radius * 2
        self.sideLength = radius
        self.__outlineThickness = outline_thickness
        self.__outlineColor = outline_color
        self.__radius = radius
        self.__centerPos = Vec2(x + width, y + radius)
        self.__points = []
        self.__coordinates = []
        self.__init_hexagon()
        self.tag = tag
        self.fillColor = fill_color
        self.isText = False
        self.text = ""
        self.__font = None
        self.__textGraphic = None
        self.__textColor = 'white'
        self.__hexCanvasObject = None

    def __init_hexagon(self):
        r = self.__radius
        x = self.__centerPos.x
        y = self.__centerPos.y
        for i in range(7):
            rad = m.radians(30.0 + i * 60)
            cos_val = m.cos(rad)
            sin_val = m.sin(rad)
            p = Vec2(x + cos_val * r, y + sin_val * r)
            self.__coordinates.append(p.x)
            self.__coordinates.append(p.y)
            self.__points.append(p)

    def draw(self, canvas):
        self.__hexCanvasObject = canvas.create_polygon(self.__coordinates, outline=self.__outlineColor,
                                                       fill=self.fillColor, width=self.__outlineThickness, tag=self.tag)
        self.__textGraphic = canvas.create_text(self.__centerPos.x, self.__centerPos.y, text=self.text,
                                                fill=self.__textColor, font=self.__font, tag=self.tag)

    def add_text(self, text, canvas, color='white'):
        w = m.floor(self.width / 3)
        self.text = text
        self.__font = tkf.Font(family="Lucida Grande", size=w)
        self.__textColor = color
        self.isText = True
        self.draw(canvas)

    def change_text(self, canvas, text):
        canvas.itemconfig(self.__textGraphic, text=text)

    def set_color(self, canvas, color):
        self.fillColor = color
        canvas.itemconfig(self.tag, fill=color)

    def change_transformable(self, canvas, width, x, y):
        r = (width / 2) / m.cos(m.radians(30))
        xc = x + width
        yc = y + r
        coordinates = []
        for i in range(7):
            rad = m.radians(30.0 + i * 60)
            cos_val = m.cos(rad)
            sin_val = m.sin(rad)
            p = Vec2(xc + cos_val * r, yc + sin_val * r)
            coordinates.append(p.x)
            coordinates.append(p.y)
        self.__coordinates = coordinates
        w = m.floor(width / 3)
        self.__font = tkf.Font(family="Lucida Grande", size=w)
        self.__centerPos = Vec2(xc, yc)
        self.draw(canvas)