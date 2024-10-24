from AI import RandomAI
from MarkovDPAI import *
from Reporter import LightConcurrentReporter
from twenty48tools.Encoder import PickleEncoder
from twenty48.Game import Game
from twenty48.Display import Display, NoneDisplay
from twenty48.Board import Board
import tkinter as tk
import colr
import sys
import pandas as pd
import numpy as np
# from ax.service.ax_client import AxClient


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
    params1 = [0
               
    ]
    

    for param1 in params1:
        
            ai_input=MarkovDPAI(ExpectiMax6(path_pen= 7.447178,
                                                pos_pen= 0,
                                                loss_penalty= 8.661336,
                                                score_factor= 1.920944))
            r = LightConcurrentReporter(ai_input, 100)
            report = pd.DataFrame(r.generate_report(), columns=['score','max_tile'])
            print(f'---------{param1}---------')
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

            # ai_input=MarkovDPAI(ExpectiMax6(path_pen= 3.23005488885216,
            #                                     pos_pen= 0,
            #                                     loss_penalty= 10.0,
            #                                     score_factor= 1.01855712728175))
            # r = LightConcurrentReporter(ai_input, 100)
            # report = pd.DataFrame(r.generate_report(), columns=['score','max_tile'])
            # print(f'---------{param1}---------')
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

            # ai_input=MarkovDPAI(ExpectiMax6(path_pen= 9.0,
            #                                     pos_pen= 0,
            #                                     loss_penalty= 5.65082143071092,
            #                                     score_factor= 3.366347776324679))
            # r = LightConcurrentReporter(ai_input, 100)
            # report = pd.DataFrame(r.generate_report(), columns=['score','max_tile'])
            # print(f'---------{param1}---------')
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
        


def perform_trial(parameters):
    path_penalty = parameters.get('path_penalty')
    position_penalty = parameters.get('position_penalty')
    full_tiles_penalty = parameters.get('full_tiles_penalty')
    loss_penalty = parameters.get('loss_penalty')
    score_factor = parameters.get('score_factor')

    ai_input=MarkovDPAI(ExpectiMax6(path_pen=path_penalty, pos_pen=position_penalty, empty_pen=full_tiles_penalty, loss_penalty=loss_penalty, score_factor=score_factor))
    r = LightConcurrentReporter(ai_input, 50)
    report = pd.DataFrame(r.generate_report(), columns=['score','max_tile'])
    print(np.mean(report['score']), len(report[report['max_tile']>=2048])/50.0)
    return len(report[report['max_tile']>=2048])/50.0


def tune_params():
    ax_client = AxClient()
    ax_client.create_experiment(name='optimize Params',
                                parameters=[
                                    {'name': 'path_penalty',
                                     'type': 'range',
                                     'bounds': [0.0, 5.0]},
                                    {'name': 'position_penalty',
                                     'type': 'range',
                                     'bounds': [0.0, 5.0]},
                                    {'name': 'full_tiles_penalty',
                                     'type': 'range',
                                     'bounds': [0.0, 2.0]},
                                    {'name': 'loss_penalty',
                                     'type': 'range',
                                     'bounds': [0.0, 10.0]},
                                    {'name': 'score_factor',
                                     'type': 'range',
                                     'bounds': [0.0, 2.0]},
                                ],
                                status_quo={'path_penalty':1,
                                            'position_penalty':0.8,
                                            'full_tiles_penalty':0.00001,
                                            'loss_penalty':1.5,
                                            'score_factor':1})
    
    for _ in range(75):
        parameters, trial_index = ax_client.get_next_trial()
        ax_client.complete_trial(trial_index=trial_index, raw_data=perform_trial(parameters))

    best_parameters, metrics = ax_client.get_best_parameters()
    print(f'The best parameters are: {best_parameters}')
    print(f'with score {metrics}')


def demo():
    # r = FileReporter(MarkovDPAI(NextTurn()), PickleEncoder())
    # r.generate_report(100)

    display = WindowDisplay()
    if len(sys.argv) == 1:
        results = []
        while True:
            g = Game(input=MarkovDPAI(ExpectiMax6(path_pen= 7.447177595213156,
                                                pos_pen= 0,
                                                loss_penalty= 8.661335883267595,
                                                score_factor= 1.920943938130582)), display=display)
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