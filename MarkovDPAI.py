from __future__ import annotations

import math
import random

from twenty48.Board import Board
from AI import AI
from abc import ABC, abstractmethod


class MarkovDPAI(AI):
    """
    template class for using different policy functions
    """

    def __init__(self, policy: Policy):
        self.policy = policy

    def get_input(self, board: Board) -> Board.Move:
        self.policy.set_depth(3)
        if len(board.get_empty_squares()) <= 0:
            self.policy.set_depth(8)
        elif len(board.get_empty_squares()) <= 2:
            self.policy.set_depth(6)
        elif len(board.get_empty_squares()) <= 8:
            self.policy.set_depth(4)
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

    def __init__(self, num_games: int = 300):
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
            penalty = 0
            tiles = board.get_tiles()
            if not board.get_legal_moves():
                penalty = 1000000000000
            for j, tile in enumerate(tiles):
                tile = 0 if tile == 0 else math.log2(tile)
                if j - 4 >= 0:
                    tile2 = 0 if tiles[j - 4] == 0 else math.log2(tiles[j - 4])
                    penalty += 2*abs(tile - tile2)
                if j + 4 <= 15:
                    tile2 = 0 if tiles[j + 4] == 0 else math.log2(tiles[j + 4])
                    penalty += 2*abs(tile2 - tile)
                if j - 1 >= 0:
                    tile2 = 0 if tiles[j - 1] == 0 else math.log2(tiles[j - 1])
                    penalty += abs(tile2 * (pow(-1, (j // 4))) - tile * (pow(-1, (j // 4))))
                if j + 1 <= 15:
                    tile2 = 0 if tiles[j + 1] == 0 else math.log2(tiles[j + 1])
                    penalty += abs(tile * (pow(-1, (j // 4))) - tile2 * (pow(-1, (j // 4))))
            score += board_tuple[0] * (board_score / self.num_games*4 - penalty)

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
        for i in range(self.depth):
            for board_tuple in prev_boards:
                board = board_tuple[1]
                for space in board.get_empty_squares():
                    boards.append((0.1 * board_tuple[0], board.copy().set_tile_value([space], [4])))
                    boards.append((0.9 * board_tuple[0], board.copy().set_tile_value([space], [2])))
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
            max_tile = max(board.get_tiles())
            board_score = sum(board.get_tiles()) + max_tile
            # encourage monotonic runs by adding tile difference penalty
            penalty = 0
            tiles = board.get_tiles()
            if not board.get_legal_moves():
                penalty = 10000000
            for j, tile in enumerate(tiles):
                tile = 0 if tile == 0 else math.log2(tile)

                if j < 12:
                    # tile2 = 0 if tiles[j + 4] == 0 else math.log2(tiles[j + 4])
                    penalty += abs(tile - tiles[j + 4])

                if j % 4 != 3:
                    # tile2 = 0 if tiles[j + 1] == 0 else math.log2(tiles[j + 1])
                    penalty += abs(tile - tiles[j + 1])
            scores.append(board_tuple[0] * (board_score*4 - penalty))

        return int(sum(scores) / len(scores))
