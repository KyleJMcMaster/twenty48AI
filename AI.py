
from twenty48.Board import Board
from twenty48.Input import Input
from abc import abstractmethod
from typing import List
import random


class AI(Input):

    @abstractmethod
    def get_input(self, board: Board) -> Board.Move:
        pass


class RandomAI(AI):

    def __init__(self, weights: List[float] = None):
        # weights is list of weights for each move
        # r:0, u:1, l:2, d:3
        if weights is None:
            self.weights = [0.25, 0.25, 0.25, 0.25]
        else:

            self.weights = weights

    def get_input(self, board: Board) -> Board.Move:
        move = random.choices(list(Board.Move), self.weights)[0]
        return move
