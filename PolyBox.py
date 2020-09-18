from Vector2 import Vec2
import math as m


class PolyBox:
    def __init__(self, x, y, width, height, angle, tag):
        self.position = Vec2(x, y)
        self.size = Vec2(width, height)
        self.angle = angle
        self.__mCoordinates = []
        self.tag = tag
        self.fill = "gray"
        self.outlineColor = "black"
        self.outlineThickness = 4
        self.__init_poly_box()

    def __init_poly_box(self):
        x = self.position.x
        y = self.position.y
        h = self.size.y
        w = self.size.x
        delta_x = (h / 2) / m.tan(m.radians(self.angle))
        self.__mCoordinates.append(x)
        self.__mCoordinates.append(y + h / 2)
        self.__mCoordinates.append(x + delta_x)
        self.__mCoordinates.append(y)
        self.__mCoordinates.append(x + w - delta_x)
        self.__mCoordinates.append(y)
        self.__mCoordinates.append(x + w)
        self.__mCoordinates.append(y + h / 2)
        self.__mCoordinates.append(x + w - delta_x)
        self.__mCoordinates.append(y + h)
        self.__mCoordinates.append(x + delta_x)
        self.__mCoordinates.append(y + h)

    def draw(self, canvas):
        canvas.create_polygon(self.__mCoordinates, outline=self.outlineColor,
                              fill=self.fill, width=self.outlineThickness, tag=self.tag)
        #canvas.create_text(self.__mCenterPos.x, self.__mCenterPos.y, text=self.__text, fill='white',
         #                  font=self.__font, tag=self.__tag)