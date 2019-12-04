from typing import NewType

Side = NewType('Side', str)

FRONT = Side('front')
LEFT = Side('left')
BACK = Side('back')
RIGHT = Side('right')
TOP = Side('top')
BOTTOM = Side('bottom')


def translate_to_side(str):
    switch = {
        'front': FRONT,
        'left': LEFT,
        'back': BACK,
        'right': RIGHT,
        'top': TOP,
        'bottom': BOTTOM,

    }
    return switch.get(str, BOTTOM)


