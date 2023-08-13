from __future__ import annotations
from twenty48.Board import Board
from AI import AI
from abc import ABC, abstractmethod


class MarkovDPAI(AI):

    def __init__(self, policy: Policy):
        self.policy = policy

    def get_input(self, board: Board) -> Board.Move:
        return self.policy.get_move(board)


class Policy(ABC):

    def get_move(self, board: Board) -> Board.Move:
        # returns move with best score
        scores = {move: 0 for move in board.get_legal_moves()}

        for move in board.get_legal_moves():
            scores[move] = self.eval_score(board.copy(), move)

        best_move = max(scores, key=lambda x: scores[x])
        return best_move

    @abstractmethod
    def eval_score(self, board: Board, move: Board.Move) -> int:
        pass


class NextTurn(Policy):
    # returns the highest score on the next turn
    def eval_score(self, board: Board, move: Board.Move) -> int:
        return board.move(move).get_score()

