class Core:
    def __init__(self, width: int = 1440, height: int = 900):
        self.__width = width
        self.__height = height

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @width.setter
    def width(self, val):
        self.__width = val

    @height.setter
    def height(self, val):
        self.__height = val
