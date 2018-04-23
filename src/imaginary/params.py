from enum import Enum
from typing import (
    Any,
    Text,
    Tuple,
)


class EnumParam(Enum):

    def serialize(self) -> Any:
        return self.value


class Type(EnumParam):
    jpeg = 'jpeg'
    png = 'png'
    webp = 'webp'
    auto = 'auto'


class Gravity(EnumParam):
    north = 'north'
    south = 'south'
    centre = 'centre'
    west = 'west'
    east = 'east'
    smart = 'smart'


class Colorspace(EnumParam):
    srgb = 'srgb'
    bw = 'bw'


class Extend(EnumParam):
    black = 'black'
    copy = 'copy'
    mirror = 'mirror'
    white = 'white'
    background = 'background'


class Color:
    red: int
    green: int
    blue: int

    def __init__(self, red: int, green: int, blue: int) -> None:
        self.red = red
        self.green = green
        self.blue = blue

    def serialize(self) -> Text:
        return f'{self.red},{self.green},{self.blue}'
