from __future__ import annotations

import math
import random
from twenty48 import Game
from twenty48.Board import Board
from AI import AI
from abc import ABC, abstractmethod
import time
import ctypes

class MarkovDPAI(AI):
    """
    template class for using different policy functions
    """

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
        # time.sleep(0.1)
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
            boards.append((0.9, board.copy().set_tile_value([space], [2])))

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
                penalty = 10**13

            if max(tiles) > tiles[15]:
                penalty += 2 * max_tile

            path = [3,2,1,0,4,5,6,7,11,10,9,8,12,13,14,15]

            for j, tile in enumerate(path):
                if j < 15 and tiles[tile] > tiles[path[j+1]]:
                    penalty += 4 * (tiles[tile] - tiles[path[j+1]])

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
    



class ExpectiMax3(Policy):
    def __init__(self, number_of_boards = 1000):
        #self.num_games = num_games
        #self.depth = None
        self.number_of_boards = number_of_boards
        self.position_penalty = 0.65
        self.path_penalty_factor = 1
        self.loss_penalty = 100000
        self.score_starting_value = -100000
        self.score_estimator = MarkovDPAI(NextTurn())
        self.score_estimator_games = 1

    def set_depth(self, depth: int):
        self.depth = depth

    def eval_score(self, board: Board, move: Board.Move) -> int:
        board = board.move(move)
        boards = []
        prev_boards = [(1, board)]
        while len(prev_boards) < self.number_of_boards:
            for board_tuple in prev_boards:
                board = board_tuple[1]
                empty_squares = board.get_empty_squares()
                for space in empty_squares:
                    boards.append((len(empty_squares) * 0.1 * board_tuple[0], board.copy().set_tile_value([space], [4])))
                    boards.append((len(empty_squares) * 0.9 * board_tuple[0], board.copy().set_tile_value([space], [2])))
                
            for board in boards:
                try:
                    self.score_estimator = MarkovDPAI(ExpectiMax3(self.number_of_boards - len(prev_boards) -999))
                    board[1].move(self.score_estimator.get_input(board[1]))
                except:
                    pass
            if boards:
                prev_boards = boards.copy()
                boards = []
            else:
                break

        boards = prev_boards
        # print(f'boards: {len(boards)}')

        scores = [self.score_starting_value]
        for board_tuple in boards:
            board = board_tuple[1]
           
            # if self.score_estimator and (max(board.get_tiles()) >= 1024 and len(board.get_empty_squares()) < 4):
            #     # print(f'use board score ---')
            #     try:
            #         board_score = board.move(self.score_estimator.get_input(board)).get_score()
            #     except:
            #         board_score = board.get_score()
            # else:
            board_score = board.get_score()
            
            penalty = 0
            tiles = board.get_tiles()
            max_tile = max(tiles)
            if not board.get_legal_moves():
                penalty = self.loss_penalty

            # encourage largest tile in bottom corner
            if max(tiles) > tiles[15]:
                penalty += self.position_penalty * board_score
                

            # encourage monotonic runs by adding tile difference penalty
            path = [3,2,1,0,4,5,6,7,11,10,9,8,12,13,14,15]
            #path2 = [12,8,4,0,1,5,9,13,14,10,6,2,3,7,11,15]


            path_pen = 0
            #path2_pen = 0


            for j, tile in enumerate(path):
                if j < 15 and tiles[tile] > tiles[path[j+1]]:
                    path_pen += (tiles[tile] - tiles[path[j+1]])

            # for j, tile in enumerate(path2):
            #     if j < 15 and tiles[tile] > tiles[path2[j+1]]:
            #         path2_pen += (tiles[tile] - tiles[path2[j+1]])

            
            

            penalty += self.path_penalty_factor * path_pen
            # print(board_score, penalty)
            scores.append(board_tuple[0] * (board_score - penalty))
        # print(f'{move}: {sum(scores)}')
        return sum(scores)


class ExpectiMax4(Policy):

    def __init__(self, pos_pen = 0.8, path_pen=1, empty_pen = 0.00001):
        self.loss_penalty = -100000
        self.depth = 4
        self.position_penalty = pos_pen
        self.path_penalty_factor = path_pen
        self.empty_space_pen = empty_pen

    def eval_score(self, board:Board, move: Board.Move) -> int:
        result = self.loss_penalty
        result = max(result, self.expectiminmax(board.copy().move(move), choose_move = False, depth= self.depth))
        return result
    
    def expectiminmax(self, board: Board, choose_move:bool, depth:int) -> float:
    
        if depth == 0 or not board.get_legal_moves():
            return self.estimate_score(board)


        if choose_move:
            result = self.loss_penalty
            for move in board.get_legal_moves():
                result = max(result, self.expectiminmax(board.copy().move(move), choose_move = False, depth= depth-1))
        
        else:
            result = 0
            empty_squares = board.get_empty_squares()
            for space in empty_squares:
                result += (0.1/len(empty_squares)) * self.expectiminmax(board.copy().set_tile_value([space], [4]), choose_move = True, depth= depth-1)
                result += (0.9/len(empty_squares)) * self.expectiminmax(board.copy().set_tile_value([space], [2]), choose_move = True, depth= depth-1)
        return result

    def estimate_score(self, board:Board):

        board_score = board.get_score()
        penalty = 0
        tiles = board.get_tiles()

        if max(tiles) > tiles[15]:
                penalty += self.position_penalty * board_score
        
        path = [3,2,1,0,4,5,6,7,11,10,9,8,12,13,14,15]
        path_pen = 0
        for j, tile in enumerate(path):
                if j < 15 and tiles[tile] > tiles[path[j+1]]:
                    path_pen += (tiles[tile] - tiles[path[j+1]])
        penalty += self.path_penalty_factor * path_pen

        penalty += self.empty_space_pen * board_score * (16 - len(board.get_empty_squares()))

        return board_score - penalty
    


class ExpectiMax5(Policy):

    def __init__(self, pos_pen = 0.5, path_pen=0.5):
        self.loss_penalty = -100000
        self.depth = 4
        self.position_penalty = pos_pen
        self.path_penalty_factor = path_pen

    def eval_score(self, board:Board, move: Board.Move) -> int:
        result = self.loss_penalty
        result = max(result, self.expectiminmax_ab(board.copy().move(move), choose_move = False, depth= self.depth, a=result + self.loss_penalty, b=result))
        return result
    
    
    def expectiminmax_ab(self, board: Board, choose_move:bool, depth:int, a:float, b:float) -> float:
    
        if depth == 0 or not board.get_legal_moves():
            return self.estimate_score(board)


        if choose_move:
            result = self.loss_penalty
            for move in board.get_legal_moves():
                result = max(result, self.expectiminmax_ab(board.copy().move(move), choose_move = False, depth= depth-1, a=result + self.loss_penalty, b=result))
            return result
        
        else:
            result = 0
            empty_squares = board.get_empty_squares()
            N = len(empty_squares)
            max_tile = int(max(board.get_tiles()))
            max_value = (max_tile << 1) * max_tile.bit_length() # (n*2^n+1)
            min_value = self.loss_penalty

            A = N * (a-max_value) + max_value
            B = N * (b - min_value) + min_value
            sum = 0
            for space in empty_squares:
                for tile in [[0.1, 4],[0.9,2]]:
                    Ax = max(A, min_value)
                    Bx = min(B, max_value)

                    result = (tile[0]/N) * self.expectiminmax_ab(board.copy().set_tile_value([space], [tile[1]]), choose_move = True, depth= depth-1, a=Ax, b=Bx)
                    if result <= A:
                        print('prune!!')
                        return a
                    if result >= B:
                        print('prune!!')
                        return b
                    sum += result
                    A += max_value - result
                    B += min_value - result
                
            return sum/N

    def estimate_score(self, board:Board):

        board_score = board.get_score()
        penalty = 0
        tiles = board.get_tiles()

        if max(tiles) > tiles[15]:
                penalty += self.position_penalty * board_score
        
        path = [3,2,1,0,4,5,6,7,11,10,9,8,12,13,14,15]
        path_pen = 0
        for j, tile in enumerate(path):
                if j < 15 and tiles[tile] > tiles[path[j+1]]:
                    path_pen += (tiles[tile] - tiles[path[j+1]])
        penalty += self.path_penalty_factor * path_pen

        return board_score - penalty



class ExpectiMax6(Policy):

    def __init__(self, pos_pen = 0, path_pen=7.447177595213156, empty_pen = 0, loss_penalty = 8.661335883267595, score_factor=1.920943938130582):
        self.loss_penalty = loss_penalty
        self.depth = 4
        self.position_penalty = pos_pen
        self.path_penalty_factor = path_pen
        self.empty_space_pen = empty_pen
        self.score_factor = score_factor

    def eval_score(self, board:Board, move: Board.Move) -> int:
        result = -1000000000
        result = max(result, self.expectiminmax(board.copy().move(move), choose_move = False, depth= self.depth))
        return result
    
    def expectiminmax(self, board: Board, choose_move:bool, depth:int) -> float:
    
        if depth == 0 or not board.get_legal_moves():
            return self.estimate_score(board)


        if choose_move:
            result = self.loss_penalty
            for move in board.get_legal_moves():
                result = max(result, self.expectiminmax(board.copy().move(move), choose_move = False, depth= depth-1))
        
        else:
            result = 0
            empty_squares = board.get_empty_squares()
            for space in empty_squares:
                result += (0.1/len(empty_squares)) * self.expectiminmax(board.copy().set_tile_value([space], [4]), choose_move = True, depth= depth-1)
                result += (0.9/len(empty_squares)) * self.expectiminmax(board.copy().set_tile_value([space], [2]), choose_move = True, depth= depth-1)
        return result

    def estimate_score(self, board:Board):

        board_score = board.get_score()
        penalty = 0
        tiles = board.get_tiles()

        if not board.get_legal_moves():
            penalty += self.loss_penalty * board_score

        if max(tiles) > tiles[15]:
                penalty += self.position_penalty * board_score
        
        path = [3,2,1,0,4,5,6,7,11,10,9,8,12,13,14,15]
        path_pen = 0
        for j, tile in enumerate(path):
                if j < 15 and tiles[tile] > tiles[path[j+1]]:
                    path_pen += (tiles[tile] - tiles[path[j+1]])
        penalty += self.path_penalty_factor * path_pen

        penalty += self.empty_space_pen * board_score * (16 - len(board.get_empty_squares()))

        return self.score_factor * board_score - penalty
class ScoreEst:

    @staticmethod
    def eval_score(board, input, num_games = 1) -> float:
        board_score = 0.0
        for i in range(num_games):
            game_board = board.copy()
            gameover = False
            if not game_board.get_legal_moves():
                gameover = True
            while not gameover:
                move = input.get_input(game_board)
                game_board.move(move)
                game_board.set_random_square()
                if not game_board.get_legal_moves():
                    gameover = True

            board_score += game_board.get_score()
        return board_score/num_games
    

class ExpectiMax7(AI):

    def __init__(self, depth=6, path_pen=10.282501707392333, loss_penalty = 0.0, score_factor=4.480025944804589):
        self.loss_penalty = loss_penalty
        self.depth = depth
        self.position_penalty = 0
        self.path_penalty_factor = path_pen
        self.empty_space_pen = 0
        self.score_factor = score_factor

        self.params = [
            self.depth,
            self.path_penalty_factor,
            self.loss_penalty,
            self.score_factor
        ]


        self.lib = ctypes.CDLL('./twency48.so')
        self.lib.get_next_move.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.POINTER(ctypes.c_double))
        self.lib.get_next_move.restype = ctypes.c_int

        self.c_params = (ctypes.c_double * len(self.params))(*self.params)




    def get_input(self, board:Board) -> Board.Move:
        score = board.get_score()
        tiles = board.get_tiles()
        
        c_tiles = (ctypes.c_int * len(tiles))(*tiles)
        result = self.lib.get_next_move(c_tiles, score, self.c_params)
        move = board.Move.UP
        if result == 2:
            move = Board.Move.UP
        if result == 3:
            move = Board.Move.DOWN
        if result == 1:
            move = Board.Move.LEFT
        if result == 0:
            move = Board.Move.RIGHT
        # print(move)
        return move
    
class MCTS(AI):

    def __init__(self, 
                 confidence = 0.99,
                 max_trials = 1000000,
                 tolerance = 1e-11,
                 max_iterations =100000):
        self.confidence =confidence
        self.max_trials =max_trials
        self.tolerance =tolerance
        self.max_iterations = max_iterations

        self.params = [
            self.confidence ,
            self.max_trials,
            self.tolerance ,
            self.max_iterations,
            11
        ]


        self.lib = ctypes.CDLL('./twency48.so')
        self.lib.get_MCTS_next_move.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.POINTER(ctypes.c_double))
        self.lib.get_MCTS_next_move.restype = ctypes.c_int

        self.c_params = (ctypes.c_double * len(self.params))(*self.params)




    def get_input(self, board:Board) -> Board.Move:
        score = board.get_score()
        tiles = board.get_tiles()
        max_tile = math.log2(max(tiles))
        
        self.c_params[4] = max(max_tile + 1, 7)
        print(self.c_params[4])
        c_tiles = (ctypes.c_int * len(tiles))(*tiles)
        result = self.lib.get_MCTS_next_move(c_tiles, score, self.c_params)
        move = board.Move.UP
        if result == 2:
            move = Board.Move.UP
        if result == 3:
            move = Board.Move.DOWN
        if result == 1:
            move = Board.Move.LEFT
        if result == 0:
            move = Board.Move.RIGHT
        # print(move)
        return move