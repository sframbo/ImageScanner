import numpy as np

x = np.full((5,5,5), {"x":1, "y":2})


# print(x)
print(x[1,1,1]['x'])
x[1,1,1]['x'] = 3
print(x[1,1,1]['x'])
print(x)
x[1,3,3]['y'] = 6
print(x[1,1,1]['x'])
print(x)