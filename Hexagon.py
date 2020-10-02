import math as m
import tkinter.font as tkf
from Vector2 import Vec2


class Hexagon:
    def __init__(self, width, x, y, outline_color, fill_color, outline_thickness, tag):  # x - left most edge, y - top
        radius = (width / 2) / m.cos(m.radians(30))
        self.width = width  # distance between the left most edge and the center point
        self.height = radius * 2
        self.side_length = radius
        self.__mOutlineThick = outline_thickness
        self.__mOutColor = outline_color
        self.__mRadius = radius
        self.__mCenterPos = Vec2(x + width, y + radius)
        self.__mPoints = []
        self.__mCoordinates = []
        self.__init_hexagon()
        self.tag = tag
        self.fillColor = fill_color
        self.__is_text = False
        self.text = ""
        self.__font = None
        self.__text_graphic = None
        self.__textColor = 'white'
        self.__hex_canvas_object = None

    def __init_hexagon(self):
        r = self.__mRadius
        x = self.__mCenterPos.x
        y = self.__mCenterPos.y
        for i in range(7):
            rad = m.radians(30.0 + i * 60)
            cos_val = m.cos(rad)
            sin_val = m.sin(rad)
            p = Vec2(x + cos_val * r, y + sin_val * r)
            self.__mCoordinates.append(p.x)
            self.__mCoordinates.append(p.y)
            self.__mPoints.append(p)

    def draw(self, canvas):
        self.__hex_canvas_object = canvas.create_polygon(self.__mCoordinates, outline=self.__mOutColor,
                                                         fill=self.fillColor, width=self.__mOutlineThick, tag=self.tag)
        self.__text_graphic = canvas.create_text(self.__mCenterPos.x, self.__mCenterPos.y, text=self.text,
                                                 fill=self.__textColor, font=self.__font, tag=self.tag)

    def get_radius(self):
        return self.__mRadius

    def add_text(self, text, canvas, color='white'):
        w = m.floor(self.width / 3)
        self.text = text
        self.__font = tkf.Font(family="Lucida Grande", size=w)
        self.__textColor = color
        self.draw(canvas)

    def change_text(self, canvas, text):
        canvas.itemconfig(self.__text_graphic, text=text)

    def get_fill_color(self, canvas):
        return canvas.itemcget(self.tag, 'fill')

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
        self.__mCoordinates = coordinates
        w = m.floor(width / 3)
        self.__font = tkf.Font(family="Lucida Grande", size=w)
        self.__mCenterPos = Vec2(xc, yc)
        self.draw(canvas)