from dataclasses import dataclass

@dataclass
class Color:
    name: str
    initial: str
    hex: str


AQUA = Color('AQUA', 'A', '#00FFFF')
BLUE = Color('BLUE', 'B', '#0000CD')
CHARTREUSE = Color('CHARTREUSE', 'C', '#EE82EE')
DARKGOLDENROD = Color('DARKGOLDENROD', 'D', '#ADFF2F')
EBONY = Color('EBONY', 'E', '#FF4500')
FUCHSIA = Color('FUCHSIA', 'F', '#FF00FF')
GREEN = Color('Green', 'G', '#008000')
HOTPINK = Color('HOTPINK', 'H', '#FF69B4')
INDIGO = Color('INDIGO', 'I', '#4B0082')
NAVAJO = Color('NAVAJO', 'J', '#FFDEAD')
KHAKI = Color('KHAKI', 'K', '#F0E68C')
LAVENDER = Color('LAVENDER', 'L', '#E6E6FA')
MAGENTA = Color('MAGENTA', 'M', '#FF00FF')
NAVY = Color('NAVY', 'N', '#000080')
OLIVE = Color('OLIVE', 'O', '#808000')
PALEGREEN = Color('PALEGREEN', 'P', '#98FB98')
QUICKSILVER = Color('QUICKSILVER', 'Q', '#C0C0C0')
RED = Color('RED', 'R', '#FF0000')
SEASHELL = Color('SEASHELL', 'S', '#FFF5EE')
TAN = Color('TAN', 'T', '#D2B48C')
PERU = Color('PERU', 'U', '#CD853F')
IVORY = Color('IVORY', 'V', '#FFFFF0')
WHITE = Color('WHITE', 'W', '#F5F5F5')
XRAY = Color('XRAY', 'X', '#2F4F4F')
YELLOW = Color('Yellow', 'Y', '#FFFF00')
ZAFFRE = Color('ZAFFRE', 'Z', '#008080')

VOID = Color('VOID', '.', '#000000')
NO_COLOR = Color('CLEAR', '?', '#000000')


# accepts a  string and returns a color
def translate_to(str):
    switch = {

        'A' : AQUA,
        'B' : BLUE,
        'C' : CHARTREUSE,
        'D' : DARKGOLDENROD,
        'E' : EBONY,
        'F' : FUCHSIA,
        'G' : GREEN,
        'H' : HOTPINK,
        'I' : INDIGO,
        'J' : NAVAJO,
        'K' : KHAKI,
        'L' : LAVENDER,
        'M' : MAGENTA,
        'N' : NAVY,
        'O' : OLIVE,
        'P' : PALEGREEN,
        'Q' : QUICKSILVER,
        'R' : RED,
        'S' : SEASHELL,
        'T' : TAN,
        'U' : PERU,
        'V' : IVORY,
        'W' : WHITE,
        'X' : XRAY,
        'Y' : YELLOW,
        'Z' : ZAFFRE,
        '.' : VOID
    }
    return switch.get(str, ZAFFRE)





