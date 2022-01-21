import enum


class Colour(object):

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, value):
        self._red = round(value)

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, value):
        self._green = round(value)

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, value):
        self._blue = round(value)

    @property
    def rgb(self):
        return self.red, self.green, self.blue

    def multiply(self, factor: float):
        return self.__class__(*[c * factor for c in self.rgb])

    def to_hex(self):
        return '#%02x%02x%02x' % self.red, self.green, self.blue

    @classmethod
    def from_rgb(cls, red, green, blue):
        return cls(red, green, blue)

    @classmethod
    def from_hex(cls, hex_):
        return cls(*tuple(int(hex_[i:i+2], 16) for i in (0, 2, 4)))

    @classmethod
    def from_hsl(cls, hue, saturation, value):
        raise NotImplementedError()


class Colours(object):
    White = Colour(255, 255, 255)
    Black = Colour(0, 0, 0)
    Red = Colour(255, 0, 0)
    Green = Colour(0, 255, 0)
    Blue = Colour(0, 0, 255)
    Purple = Colour(255, 0, 255)
    Yellow = Colour(255, 255, 0)
