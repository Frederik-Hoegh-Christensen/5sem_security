import random


def SplitToShare(ar, num):

    # Generating three random shares from given input
    share1 = random.randint(0, num)
    share2 = random.randint(0, num - share1)
    share3 = num - share1 - share2
    ar = [share1, share2, share3]
    return ar


def CalculateShares(a, b, c):

    res = int(a)+int(b)+int(c)
    return res
