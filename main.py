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
    


    # ai_input=ExpectiMax8(depth = 6, path_pen=3.3034937206974053, loss_penalty=3.3034937206974053, score_factor=1.1410012397734988, num_trials=754)
    # r = LightConcurrentReporter(ai_input, 100)
    # report = pd.DataFrame(r.generate_report(), columns=['score','max_tile'])
    # print(f'------------------')
    # # print(report)
    # print(np.mean(report['score']), len(report[report['max_tile']>=2048])/50.0)
    # num_under_512 = len(report[report['max_tile']<512])
    # num_over_1024 = len(report[report['max_tile']>=1024])
    # num_over_2048 = len(report[report['max_tile']>=2048])
    # num_over_4096 = len(report[report['max_tile']>=4096])
    # num_over_8192 = len(report[report['max_tile']>=8192])
    # print(f'Number of games under 512: {num_under_512}')
    # print(f'Number of games over 1024: {num_over_1024}')
    # print(f'Number of games over 2048: {num_over_2048}')
    # print(f'Number of games over 4096: {num_over_4096}')
    # print(f'Number of games over 8192: {num_over_8192}')

    ai_input=ExpectiMax8(depth = 7, path_pen=3.3034937206974053, loss_penalty=3.3034937206974053, score_factor=1.1410012397734988, num_trials=1000)
    r = LightConcurrentReporter(ai_input, 100)
    report = pd.DataFrame(r.generate_report(), columns=['score','max_tile'])
    print(f'------------------')
    # print(report)
    print(np.mean(report['score']), len(report[report['max_tile']>=2048])/100.0)
    max_score = max(report['score'])
    num_under_512 = len(report[report['max_tile']<512])
    num_over_1024 = len(report[report['max_tile']>=1024])
    num_over_2048 = len(report[report['max_tile']>=2048])
    num_over_4096 = len(report[report['max_tile']>=4096])
    num_over_8192 = len(report[report['max_tile']>=8192])
    num_over_16348 = len(report[report['max_tile']>=16348])
    print(f'Number of games under 512: {num_under_512}')
    print(f'Number of games over 1024: {num_over_1024}')
    print(f'Number of games over 2048: {num_over_2048}')
    print(f'Number of games over 4096: {num_over_4096}')
    print(f'Number of games over 8192: {num_over_8192}')
    print(f'Number of games over 16348: {num_over_16348}')
    print(f'Max score {max_score}')

    ai_input=ExpectiMax8(depth = 7, path_pen=2.8496881554134417, loss_penalty=20.0, score_factor= 1.2143101689275857, num_trials=1000)
    r = LightConcurrentReporter(ai_input, 100)
    report = pd.DataFrame(r.generate_report(), columns=['score','max_tile'])
    print(f'------------------')
    # print(report)
    print(np.mean(report['score']), len(report[report['max_tile']>=2048])/100.0)
    max_score = max(report['score'])
    num_under_512 = len(report[report['max_tile']<512])
    num_over_1024 = len(report[report['max_tile']>=1024])
    num_over_2048 = len(report[report['max_tile']>=2048])
    num_over_4096 = len(report[report['max_tile']>=4096])
    num_over_8192 = len(report[report['max_tile']>=8192])
    num_over_16348 = len(report[report['max_tile']>=16348])
    print(f'Number of games under 512: {num_under_512}')
    print(f'Number of games over 1024: {num_over_1024}')
    print(f'Number of games over 2048: {num_over_2048}')
    print(f'Number of games over 4096: {num_over_4096}')
    print(f'Number of games over 8192: {num_over_8192}')
    print(f'Number of games over 16348: {num_over_16348}')
    print(f'Max score {max_score}')

    ai_input=ExpectiMax8(depth = 7, path_pen=0.45127922428126166, loss_penalty=12.544226964630045, score_factor=0.12761368167679277, num_trials=1000)
    r = LightConcurrentReporter(ai_input, 100)
    report = pd.DataFrame(r.generate_report(), columns=['score','max_tile'])
    print(f'------------------')
    # print(report)
    print(np.mean(report['score']), len(report[report['max_tile']>=2048])/100.0)
    max_score = max(report['score'])
    num_under_512 = len(report[report['max_tile']<512])
    num_over_1024 = len(report[report['max_tile']>=1024])
    num_over_2048 = len(report[report['max_tile']>=2048])
    num_over_4096 = len(report[report['max_tile']>=4096])
    num_over_8192 = len(report[report['max_tile']>=8192])
    num_over_16348 = len(report[report['max_tile']>=16348])
    print(f'Number of games under 512: {num_under_512}')
    print(f'Number of games over 1024: {num_over_1024}')
    print(f'Number of games over 2048: {num_over_2048}')
    print(f'Number of games over 4096: {num_over_4096}')
    print(f'Number of games over 8192: {num_over_8192}')
    print(f'Number of games over 16348: {num_over_16348}')
    print(f'Max score {max_score}')

    ai_input=ExpectiMax8(depth = 7, path_pen=1.4215126940585034, loss_penalty=14.285895921045633, score_factor=0.5722546594578515, num_trials=1000)
    r = LightConcurrentReporter(ai_input, 100)
    report = pd.DataFrame(r.generate_report(), columns=['score','max_tile'])
    print(f'------------------')
    # print(report)
    print(np.mean(report['score']), len(report[report['max_tile']>=2048])/100.0)
    max_score = max(report['score'])
    num_under_512 = len(report[report['max_tile']<512])
    num_over_1024 = len(report[report['max_tile']>=1024])
    num_over_2048 = len(report[report['max_tile']>=2048])
    num_over_4096 = len(report[report['max_tile']>=4096])
    num_over_8192 = len(report[report['max_tile']>=8192])
    num_over_16348 = len(report[report['max_tile']>=16348])
    print(f'Number of games under 512: {num_under_512}')
    print(f'Number of games over 1024: {num_over_1024}')
    print(f'Number of games over 2048: {num_over_2048}')
    print(f'Number of games over 4096: {num_over_4096}')
    print(f'Number of games over 8192: {num_over_8192}')
    print(f'Number of games over 16348: {num_over_16348}')
    print(f'Max score {max_score}')

    # ai_input=ExpectiMax8(depth = 7, path_pen=3.4846910016306003, loss_penalty=10.0, score_factor=1.1104202438519803, num_trials=800)
    # r = LightConcurrentReporter(ai_input, 100)
    # report = pd.DataFrame(r.generate_report(), columns=['score','max_tile'])
    # print(f'------------------')
    # # print(report)
    # print(np.mean(report['score']), len(report[report['max_tile']>=2048])/50.0)
    # num_under_512 = len(report[report['max_tile']<512])
    # num_over_1024 = len(report[report['max_tile']>=1024])
    # num_over_2048 = len(report[report['max_tile']>=2048])
    # num_over_4096 = len(report[report['max_tile']>=4096])
    # num_over_8192 = len(report[report['max_tile']>=8192])
    # print(f'Number of games under 512: {num_under_512}')
    # print(f'Number of games over 1024: {num_over_1024}')
    # print(f'Number of games over 2048: {num_over_2048}')
    # print(f'Number of games over 4096: {num_over_4096}')
    # print(f'Number of games over 8192: {num_over_8192}')

    # ai_input=ExpectiMax7(depth = 4)
    # r = LightConcurrentReporter(ai_input, 100)
    # report = pd.DataFrame(r.generate_report(), columns=['score','max_tile'])
    # print(f'------------------')
    # # print(report)
    # print(np.mean(report['score']), len(report[report['max_tile']>=2048])/50.0)
    # num_under_512 = len(report[report['max_tile']<512])
    # num_over_1024 = len(report[report['max_tile']>=1024])
    # num_over_2048 = len(report[report['max_tile']>=2048])
    # num_over_4096 = len(report[report['max_tile']>=4096])
    # num_over_8192 = len(report[report['max_tile']>=8192])
    # print(f'Number of games under 512: {num_under_512}')
    # print(f'Number of games over 1024: {num_over_1024}')
    # print(f'Number of games over 2048: {num_over_2048}')
    # print(f'Number of games over 4096: {num_over_4096}')
    # print(f'Number of games over 8192: {num_over_8192}')

    # ai_input=MCTS2(100)
    # r = LightConcurrentReporter(ai_input, 100)
    # report = pd.DataFrame(r.generate_report(), columns=['score','max_tile'])
    # print(f'------------------')
    # # print(report)
    # print(np.mean(report['score']), len(report[report['max_tile']>=2048])/50.0)
    # num_under_512 = len(report[report['max_tile']<512])
    # num_over_1024 = len(report[report['max_tile']>=1024])
    # num_over_2048 = len(report[report['max_tile']>=2048])
    # num_over_4096 = len(report[report['max_tile']>=4096])
    # num_over_8192 = len(report[report['max_tile']>=8192])
    # print(f'Number of games under 512: {num_under_512}')
    # print(f'Number of games over 1024: {num_over_1024}')
    # print(f'Number of games over 2048: {num_over_2048}')
    # print(f'Number of games over 4096: {num_over_4096}')
    # print(f'Number of games over 8192: {num_over_8192}')





def demo():
    # run graphical demo of different AI models in game

    display = WindowDisplay()
    if len(sys.argv) == 1:
        results = []
        while True:
            g = Game(input=ExpectiMax8(depth = 7, path_pen=0.45127922428126166, loss_penalty=12.544226964630045, score_factor=0.12761368167679277, num_trials=1000), display=display)
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