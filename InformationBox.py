from Vector2 import Vec2
import tkinter as tk
from PolyBox import PolyBox


class InfoBox:

    def __init__(self, x, y, width, height):
        self.position = Vec2(x, y)
        self.size = Vec2(width, height)
        self.box = PolyBox(x, y, width, height, 30, "info-box")
        self.box.fill = "purple"

    def set_text(self, text):
        self.text.configure(text=text)

    def set_font_size(self, s):
        self.text.configure(font=s)

    def set_background_color(self, bg):
        self.text.configure(bg=bg)

    def draw(self, canvas):
        self.box.draw(canvas)