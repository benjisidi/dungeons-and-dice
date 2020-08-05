from typing import List, Tuple
import numpy as np
import random


class Dice:
    @staticmethod
    def roll_dice(n, d):
        return [random.randint(1, d) for i in range(n)]

    def __init__(self, dice_array: List[Tuple[int, int]]):
        self.dice = dice_array

    def roll(self):
        return [self.roll_dice(n, d) for (n, d) in self.dice]

    def roll_n(self, n):
        return [self.roll() for i in range(n)]


if __name__ == "__main__":
    test = Dice([(2, 4), (3, 6)])
    print(test.roll_n(5))
