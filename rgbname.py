# test
#from random import randint

def read_rgb():
    with open("rgb.txt", "r") as f:
        for line in f:
           ele = line[:-1].split("\t")
           yield (ele[0], int(ele[2]), int(ele[3]), int(ele[4]))

rgb_iter = tuple(read_rgb())


def get_name(r, g, b):
    minimum = 10000
    name = ""
    for i in rgb_iter:
        d = abs(r - i[1]) + abs(g - i[2]) + abs(b - i[3])
        if d < minimum:
            minimum = d
            name = i[0]
    print(minimum)
    return name


# test
"""
for i in range(10):
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    print(r, g, b)
    print(get_name(r, g, b))
"""

