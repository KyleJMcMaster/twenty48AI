from __future__ import annotations

import math
import random

from twenty48.Board import Board
from AI import AI
from abc import ABC, abstractmethod
import time

class MarkovDPAI(AI):
    """
    template class for using different policy functions
    """

    def __init__(self, policy: Policy):
        self.policy = policy

    def get_input(self, board: Board) -> Board.Move:
        '''self.policy.set_depth(3)
        if len(board.get_empty_squares()) <= 0:
            self.policy.set_depth(8)
        elif len(board.get_empty_squares()) <= 2:
            self.policy.set_depth(6)
        elif len(board.get_empty_squares()) <= 8:
            self.policy.set_depth(4)'''
        return self.policy.get_move(board)


class Policy(ABC):

    def get_move(self, board: Board) -> Board.Move:
        # returns move with best score
        scores = {move: 0 for move in board.get_legal_moves()}

        for move in board.get_legal_moves():
            scores[move] = self.eval_score(board.copy(), move)

        best_move = max(scores, key=lambda x: scores[x])
        return best_move

    def set_depth(self, depth: int):
        # optional method to increase the compute depth of certain policies
        pass

    @abstractmethod
    def eval_score(self, board: Board, move: Board.Move) -> int:
        pass


class NextTurn(Policy):
    """
    Naive policy that evaluates moves based on the score after applying each move
    """

    def eval_score(self, board: Board, move: Board.Move) -> int:
        time.sleep(0.1)
        return board.move(move).get_score()


class MonteCarloExpectedValue(Policy):
    """
    Evaluates score by running random games to completion after applying each move
    """

    def __init__(self, num_games: int = 100):
        """
        :param num_games: number of games to play to get average score
        """
        self.num_games = num_games

    def set_depth(self, depth: int):
        self.num_games = depth

    def eval_score(self, board: Board, move: Board.Move) -> int:
        board = board.move(move)
        score = 0
        for i in range(self.num_games):
            game_board = board.copy()
            gameover = False
            while not gameover:
                moves = game_board.get_legal_moves()
                move = random.choice(moves)
                game_board.move(move)
                game_board.set_random_square()
                if not game_board.get_legal_moves():
                    gameover = True
            score += game_board.get_score()

        return score // self.num_games


class MinMax(Policy):
    """
    Naive MinMax without pruning
    """

    def __init__(self, depth: int = 40000):
        self.depth = depth

    def set_depth(self, depth: int):
        self.depth = depth

    def eval_score(self, board: Board, move: Board.Move) -> int:
        board_parents = board.list_possible_states(move)
        boards = []
        threshold = True
        while threshold:
            for board in board_parents:
                for move in board.get_legal_moves():
                    boards = boards + board.list_possible_states(move)
            if len(boards) >= self.depth or not boards:
                threshold = False
                boards = board_parents
            print(f'num states: {len(boards)}      ', end='\r')
            board_parents = boards.copy()
            boards = []

        wc_score = 100000000
        for board in board_parents:
            if board.get_score() < wc_score:
                wc_score = board.get_score()

        return -1 * wc_score


class ExpectiMax(Policy):
    """
    Expectimax with depth of n
    """

    def __init__(self, num_games: int = 15):
        self.num_games = num_games

    def set_depth(self, depth: int):
        self.num_games = depth

    def eval_score(self, board: Board, move: Board.Move) -> int:
        board = board.move(move)
        boards = []
        for space in board.get_empty_squares():
            boards.append((0.1, board.copy().set_tile_value([space], [4])))
            boards.append((0.9, board.copy().set_tile_value([space], [4])))

        score = 0
        for board_tuple in boards:
            board_score = 0.0
            board = board_tuple[1]
            for i in range(self.num_games):
                game_board = board.copy()
                gameover = False
                if not game_board.get_legal_moves():
                    gameover = True
                while not gameover:
                    moves = game_board.get_legal_moves()
                    move = random.choice(moves)
                    game_board.move(move)
                    game_board.set_random_square()
                    if not game_board.get_legal_moves():
                        gameover = True

                board_score += game_board.get_score()

            # encourage monotonic runs by adding tile difference penalty

        return score // len(boards)


class ExpectiMax2(Policy):
    def __init__(self, num_games: int = 300, depth: int = 4):
        self.num_games = num_games
        self.depth = depth

    def set_depth(self, depth: int):
        self.depth = depth

    def eval_score(self, board: Board, move: Board.Move) -> int:
        board = board.move(move)
        boards = []
        prev_boards = [(1, board)]
        while len(prev_boards) < 8000:
            for board_tuple in prev_boards:
                board = board_tuple[1]
                empty_squares = board.get_empty_squares()
                for space in empty_squares:
                    boards.append((len(empty_squares) * 0.1 * board_tuple[0], board.copy().set_tile_value([space], [4])))
                    boards.append((len(empty_squares) * 0.9 * board_tuple[0], board.copy().set_tile_value([space], [2])))
            if boards:
                prev_boards = boards.copy()
                boards = []
            else:
                break

        boards = prev_boards
        # print(f'boards: {len(boards)}')

        scores = [-1000000]
        for board_tuple in boards:
            '''
            board_score = 0.0
            board = board_tuple[1]
            for i in range(self.num_games):
                game_board = board.copy()
                gameover = False
                if not game_board.get_legal_moves():
                    gameover = True
                while not gameover:
                    moves = game_board.get_legal_moves()
                    move = random.choice(moves)
                    game_board.move(move)
                    game_board.set_random_square()
                    if not game_board.get_legal_moves():
                        gameover = True

                board_score += game_board.get_score()
            '''
            board_score = board.get_score()
            # encourage monotonic runs by adding tile difference penalty
            penalty = 0
            tiles = board.get_tiles()
            max_tile = max(tiles)
            if not board.get_legal_moves():
                penalty = 10**8

            if max(tiles) > tiles[15]:
                penalty += 2 * max_tile

            path = [3,2,1,0,4,5,6,7,11,10,9,8,12,13,14,15]

            for j, tile in enumerate(path):
                if j < 15 and tiles[tile] > tiles[path[j+1]]:
                    penalty += 1 * (tiles[tile] - tiles[path[j+1]])

            '''
            for j, tile in enumerate(path):
                if j < 15:
                    penalty += abs(tiles[tile] - tiles[path[j + 1]])
                if tile < 12:
                    penalty += abs(tiles[tile] - tiles[tile + 4])
            '''

            scores.append(board_tuple[0] * (board_score * 3 - penalty))
        print(sum(scores))
        return sum(scores)
