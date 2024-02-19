from AI import RandomAI
from MarkovDPAI import *
from twenty48tools.Reporter import FileReporter
from twenty48tools.Encoder import PickleEncoder
from twenty48.Game import Game
from twenty48.Display import Display
from twenty48.Board import Board
import tkinter as tk
import colr
import sys


class WindowDisplay(Display):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2048 Game")
        self.tiles = [None for _ in range(16)]
        self.score_label = tk.Label(self.window, text="Score: 0")
        self.score_label.grid(row=0)

        for i in range(16):
            self.tiles[i] = tk.Canvas(self.window, width=200, height=200)
            self.tiles[i].grid(row=int(i / 4) + 1, column=(i % 4) + 1)

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
            self.tiles[i].create_rectangle(10, 10, 190, 190, fill=colour)
            self.tiles[i].create_text(100, 100, text=str(tile) if tile != 0 else '', fill=text_colour,
                                      font=("Helvetica", 48))
        self.score_label.config(text="Score: " + str(board.get_score()))
        self.window.update_idletasks()
        self.window.update()

if __name__ =='__main__':
    # r = FileReporter(MarkovDPAI(NextTurn()), PickleEncoder())
    # r.generate_report(100)

    display = WindowDisplay()
    if len(sys.argv) == 1:
        while True:
            g = Game(input=MarkovDPAI(ExpectiMax2(15)), display=display)
            g.play_game()

        
    elif sys.argv[1] == "random":
        ai_input=RandomAI()

    elif sys.argv[1] == "next_turn":
        ai_input=MarkovDPAI(NextTurn())

    elif sys.argv[1] == "MCEV":
        ai_input=MarkovDPAI(MonteCarloExpectedValue())


    elif sys.argv[1] == "minmax":
        ai_input=MarkovDPAI(MinMax())


    elif sys.argv[1] == "emax":
        ai_input=MarkovDPAI(ExpectiMax())

    elif sys.argv[1] == "emax2":
        ai_input=MarkovDPAI(ExpectiMax2(15))

    else:
        ai_input=MarkovDPAI(ExpectiMax2(15))
        
    
    g = Game(input=ai_input, display=display)
    g.play_game()
    input("press enter to end game")


