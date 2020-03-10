from ImageScanner import image_scanner
from lib import make_random


# interact=False
# rotate=True
# data="input.txt",
# timed=True
# plot_f=True
# compared=True
# _print=True


if __name__ == '__main__':
    # # BASIC
    # image_scanner(data="./inputs/input.txt", compared=False, timed=False)

    # # BIG BASIC
    # image_scanner(data="./inputs/bigboy.txt", plot_f=False)

    # # BIG BASIC + NO-MATCH
    image_scanner(data="./inputs/bigboy2.txt", plot_=False, plot_f=False, rotate=False)

    # # BIG BOSS - a mess of match violations
    # image_scanner(data="./inputs/random.txt")

















    # for _ in range(10):
    #     make_random(10, 5, True, 5)
    #     image_scanner(data="./inputs/temp.txt", plot_f=False, plot_=False, rotate=False, _print=False)




