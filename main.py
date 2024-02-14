from AI import RandomAI
from MarkovDPAI import *
from twenty48tools.Reporter import FileReporter
from twenty48tools.Encoder import PickleEncoder
from twenty48.Game import Game
from twenty48.Display import WindowDisplay
import colr
import sys

if __name__ =='__main__':
    # r = FileReporter(MarkovDPAI(NextTurn()), PickleEncoder())
    # r.generate_report(100)

    display = WindowDisplay()
    if len(sys.argv) == 1:
        g = Game(input=MarkovDPAI(ExpectiMax2(15)), display = display)
        while True:
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
