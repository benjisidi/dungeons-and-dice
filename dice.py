from typing import List, Tuple
import numpy as np
import random


def roll(n, f):
    return [random.randint(1, f) for i in range(n)]


def roll_cluster(dice_list, n=1):
    return [[roll(n, f) for (n, f) in dice_list] for i in range(n)]


def expected_result(dice_list):
    return [n * (f + 1) / 2 for (n, f) in dice_list]


if __name__ == "__main__":
    test_dice = [(1, 4), (2, 6)]
    print(expected_result(test_dice))
