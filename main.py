from AI import RandomAI
from MarkovDPAI import *
from twenty48tools.Reporter import FileReporter
from twenty48tools.Encoder import PickleEncoder
from twenty48.Game import Game
import colr
import sys

if __name__ =='__main__':
    # r = FileReporter(MarkovDPAI(NextTurn()), PickleEncoder())
    # r.generate_report(100)

    if len(sys.argv) == 1:
        g = Game(input=MarkovDPAI(ExpectiMax2(15)))
        g.play_game()
        
    elif sys.argv[1] == "random":
        g = Game(input=RandomAI())
        g.play_game()
    elif sys.argv[1] == "next_turn":
        g = Game(input=MarkovDPAI(NextTurn()))
        g.play_game()
    elif sys.argv[1] == "MCEV":
        g = Game(input=MarkovDPAI(MonteCarloExpectedValue()))
        g.play_game()
    elif sys.argv[1] == "minmax":
        g = Game(input=MarkovDPAI(MinMax()))
        g.play_game()
    elif sys.argv[1] == "emax":
        g = Game(input=MarkovDPAI(ExpectiMax()))
        g.play_game()
    elif sys.argv[1] == "emax2":
        g = Game(input=MarkovDPAI(ExpectiMax2(15)))
        g.play_game()
    else:
        g = Game(input=MarkovDPAI(ExpectiMax2(15)))
        g.play_game()
    

