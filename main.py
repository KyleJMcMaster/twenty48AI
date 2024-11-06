from AI import RandomAI
from MarkovDPAI import *
from Reporter import LightConcurrentReporter
from twenty48.Game import Game
from twenty48.Display import Display, NoneDisplay
from twenty48.Board import Board
import tkinter as tk
import sys
import pandas as pd
import numpy as np



class WindowDisplay(Display):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2048 Game")
        self.tiles = [None for _ in range(16)]
        self.spaces = [[0,0] for _ in range(16)]
        self.score_label = tk.Label(self.window, text="Score: 0")
        self.score_label.grid(row=0)

        for i in range(16):
            self.tiles[i] = tk.Canvas(self.window, width=200, height=200)
            self.tiles[i].grid(row=int(i / 4) + 1, column=(i % 4) + 1)
            self.spaces[i][0] = self.tiles[i].create_rectangle(10, 10, 190, 190, fill="#CCC0B3")
            self.spaces[i][1] = self.tiles[i].create_text(100, 100, text= '', fill="#CCC0B3",
                                      font=("Helvetica", 48))

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




def eval_ai():
    
    ai_input=ExpectiMax7(   path_pen=   6.56164911529463,
                            loss_penalty= 10.0,
                            score_factor= 2.24397373076686,
                            depth = 7)
    r = LightConcurrentReporter(ai_input, 100)
    report = pd.DataFrame(r.generate_report(), columns=['score','max_tile'])
    print(f'------------------')
    # print(report)
    print(np.mean(report['score']), len(report[report['max_tile']>=2048])/50.0)
    num_under_512 = len(report[report['max_tile']<512])
    num_over_1024 = len(report[report['max_tile']>=1024])
    num_over_2048 = len(report[report['max_tile']>=2048])
    num_over_4096 = len(report[report['max_tile']>=4096])
    num_over_8192 = len(report[report['max_tile']>=8192])
    print(f'Number of games under 512: {num_under_512}')
    print(f'Number of games over 1024: {num_over_1024}')
    print(f'Number of games over 2048: {num_over_2048}')
    print(f'Number of games over 4096: {num_over_4096}')
    print(f'Number of games over 8192: {num_over_8192}')




def demo():
    # run graphical demo of different AI models in game

    display = WindowDisplay()
    if len(sys.argv) == 1:
        results = []
        while True:
            g = Game(input=MCTS(), display=display)
            result = g.play_game()
            results.append([result.score, result.turns[-1].max_tile])
            print([result.score, result.turns[-1].max_tile])
            time.sleep(2)
        
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


if __name__ =='__main__':
    # eval_ai()
    demo()
    # tune_params()