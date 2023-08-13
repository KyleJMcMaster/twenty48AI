from __future__ import annotations
from twenty48.Board import Board
from AI import AI
from abc import ABC, abstractmethod



class MarkovDPAI(AI):

    def __init__(self, score_function: ScoreFunction):
        self.score_function = score_function

    def get_input(self, board: Board) -> Board.Move:
        scores = {move: 0 for move in board.get_legal_moves()}

        for move in board.get_legal_moves():
            scores[move] = self.score_function.eval_score(board.copy(), move)
        best_move = max(scores, key=lambda x: scores[x])
        return best_move



class ScoreFunction(ABC):

    @abstractmethod
    def eval_score(self, board:Board, move:Board.Move) -> int:
        pass


class NextTurn(ScoreFunction):

    def eval_score(self, board:Board, move:Board.Move) -> int:
        return board.move(move).get_score()
