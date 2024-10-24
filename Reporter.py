import time
from abc import ABC, abstractmethod
import multiprocessing as mp
import numpy as np

from datetime import datetime
from typing import List
from twenty48tools.Encoder import Encoder
from twenty48.Game import Game
from twenty48.Input import Input
from twenty48.Display import NoneDisplay, ProgressDisplay


class Reporter(ABC):

    @abstractmethod
    def __init__(self, input_:Input):
        pass

    @abstractmethod
    def generate_report(self, num_games: int):
        pass


class FileReporter(Reporter):
    # Plays n games and saves gameinfo objects as a binary file for efficient storage

    def __init__(self, input_:Input, encoder: Encoder, filename: str = None):
        self.input = input_
        self.display = NoneDisplay()
        self.encoder = encoder
        if filename is None:
            self.filename = str(datetime.now()) + ".txt"
        else:
            self.filename = filename

    def generate_report(self, num_games: int = 5):
        t = time.perf_counter()
        print(f"Saving to {self.filename}")
        for i in range(num_games):
            g = Game(display=self.display, input=self.input)
            info = g.play_game()
            self.encoder.encode(gameinfo=info, filename=self.filename)
            print(f"Game number {i+1} completed", end='\r')
        t = time.perf_counter() - t
        print(f"All games completed in {t} seconds")

class LightConcurrentReporter(Reporter):
    # plays n concurrent games and reports the quartiles, mean and std.dev of mean 
    def __init__(self,  input_:Input, threads:int = 10, filename: str = None):
        self.input = input_
        self.num_threads = threads
        self.display = NoneDisplay()
        self.results = mp.Queue()
        if filename is None:
            self.filename = str(datetime.now()) + ".txt"
        else:
            self.filename = filename


    def generate_report(self) -> list[float, float]:
        # reports mean and std of score
        processes = [mp.Process(target=self.play_game, args=(1, self.results)) for x in range(self.num_threads)]

        for p in processes:
            p.start()

        for p in processes:
            p.join()

        results = [self.results.get() for p in processes]
        
        return results


    def play_game(self, num_games: int, output):
        for _ in range(num_games):
            g = Game(display=self.display, input=self.input)
            game_info = g.play_game()
            output.put([game_info.score, game_info.turns[-1].max_tile])

        



