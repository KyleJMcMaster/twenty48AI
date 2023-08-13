from AI import RandomAI
from MarkovDPAI import MarkovDPAI, NextTurn
from twenty48tools.Reporter import FileReporter
from twenty48tools.Encoder import PickleEncoder
from twenty48.Game import Game

if __name__ =='__main__':
    r = FileReporter(MarkovDPAI(NextTurn()), PickleEncoder())
    r.generate_report(100)
    # g = Game(input=MarkovDPAI(NextTurn()))
    # g.play_game()

