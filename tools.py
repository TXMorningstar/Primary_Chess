class PrintColor(object):
    FOREGROUND = {
        "black": "30;",
        "red": "31;",
        "green": "32;",
        "yellow": "33;",
        "blue": "34;",
        "pink": "35;",
        "light_blue": "36;",
        "white": "37;"
    }
    BACKGROUND = {
        "black": "40m",
        "red": "41m",
        "green": "42m",
        "yellow": "43m",
        "blue": "44m",
        "pink": "45m",
        "light_blue": "46m",
        "white": "47m"
    }


def cprint(msg:str, fg:str = "white", bg:str = "black", end:str = "\n"):
    print("\033[0;%s%s%s\033[0m" % (PrintColor.FOREGROUND[fg], PrintColor.BACKGROUND[bg], msg), end=end)


def switch_side(turn: int) -> int:
    """切换执子方，传入一个int，0代表红1代表黑"""
    global SIDE
    if SIDE == 1:
        SIDE = 21
    else:
        SIDE == 1
