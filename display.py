# contains abstract class for display type
# also contains instances for text and windowed displays


from abc import ABC, abstractmethod
import tkinter as tk
from twenty48.Board import Board
from numpy import ndarray
import colr


class Display(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def display_board(self, board: Board):
        pass


class WindowDisplay(Display):

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2048 Game")
        self.tiles = [None for _ in range(16)]
        self.spaces = [[0,0] for _ in range(16)]
        self.score_label = tk.Label(self.window, text="Score: 0")
        self.score_label.grid(row=0)

        for i in range(16):
            self.tiles[i] = tk.Canvas(self.window, width=100, height=100)
            self.tiles[i].grid(row=int(i / 4) + 1, column=(i % 4) + 1)
            self.spaces[i][0] = self.tiles[i].create_rectangle(10, 10, 90, 90, fill="#CCC0B3")
            self.spaces[i][1] = self.tiles[i].create_text(50, 50, text= '', fill="#CCC0B3",
                                      font=("Helvetica", 24))
    def display_board(self, board: Board):
        tile_colours = {
            65536: "569BE0",
            32768: "#6BAED5",
            16384: "#F0513B",
            8192: "#27B053",
            4096: "#FB736D",
            2048: "#EDC22E",
            1024: "#EDC23F",
            512: "#EDC850",
            256: "#EDCC61",
            128: "#EDCF72",
            64: "#F65E3B",
            32: "#F67C5F",
            16: "#F59563",
            8: "#F2B179",
            4: "#EDE0C8",
            2: "#EEE4DA",
            0: "#CCC0B3"
        }

        for i in range(16):
            tile = board.get_tile(i)
            if tile not in tile_colours:
                colour = "#2E2C26"
            else:
                colour = tile_colours[tile]
            text_colour = "#000000" if tile > 0 else "#FFFFFF"
            
            self.tiles[i].itemconfigure(self.spaces[i][0],fill=colour)
            self.tiles[i].itemconfigure(self.spaces[i][1], text=str(tile) if tile != 0 else '', fill=text_colour)
        self.score_label.config(text="Score: " + str(board.get_score()))
        self.window.update_idletasks()
        self.window.update()


class TextDisplay(Display):

    def __init__(self):
        pass

    def display_board(self, board: Board):
        tile_colours = {
            2048: "EDC22E",
            1024: "#EDC23F",
            512: "#EDC850",
            256: "#EDCC61",
            128: "#EDCF72",
            64: "#F65E3B",
            32: "#F67C5F",
            16: "#F59563",
            8: "#F2B179",
            4: "#EDE0C8",
            2: "#EEE4DA",
            0: "#3e403f"
        }
        print(f"score: {board.get_score()}",end="\n")
        for i in range(16):
            tile = board.get_tile(i)
            print(colr.color(f"{tile}\t".expandtabs(6), back=tile_colours[tile], fore="000000"),
                  end=" ")
            if i % 4 == 3:
                print("\n")


class NoneDisplay(Display):

    def __init__(self):
        pass

    def display_board(self, board: Board):
        pass

# remove
class ProgressDisplay(Display):

    def __init__(self, num_games, max_turns: int = 300):
        self.max_turns = max_turns
        self.num_games = num_games
        self.turn = 0
        self.current_game = 0
    def display_board(self, board: ndarray):
        self.turn += 1
        if self.turn >= self.max_turns:
            self.max_turns += 1

        ProgressDisplay.printProgressBar(self.turn, self.max_turns, suffix=f'({self.current_game}/{self.num_games}) '
                                                                            f'Games Completed')

    @staticmethod
    def print_progressBar(iteration, total, prefix='Progress:', suffix='Complete', decimals=1, length=100, fill='█', printEnd="\r"):
        """
        FROM Greenstick at https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()