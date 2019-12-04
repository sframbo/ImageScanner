from dataclasses import dataclass

@dataclass
class Color:
    name: str
    initial: str


RED = Color('RED', 'R')
BLUE = Color('BLUE', 'B')
YELLOW = Color('Yellow', 'Y')
GREEN = Color('Green', 'G')
CLEAR = Color('CLEAR', '.')
WHITE = Color('WHITE', 'W')
ZAFFRE = Color('ZAFFRE', 'Z')


# accepts a  string and returns a color
def translate_to(str):
    switch = {
        'R': RED,
        'B': BLUE,
        'Y': YELLOW,
        'G': GREEN,
        'W': WHITE,
        'Z': ZAFFRE,
        '.': CLEAR
    }
    return switch.get(str, ZAFFRE)




