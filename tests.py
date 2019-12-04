import numpy as np
from enum import Enum
from typing import NewType

class Color(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3


Color = NewType('Color', str)

RED = Color('R')
GREEN = Color('G')
MAGENTA = Color('M')
CLEAR = Color('.')



print(RED)
print(RED + MAGENTA)
