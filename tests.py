import numpy as np
from enum import Enum
from typing import NewType
from dataclasses import dataclass
from lib import *

x = prepare_slice(".R. YYR .Y. RYY .Y. .R.")
print(x)

print(x['front'][0] == CLEAR)