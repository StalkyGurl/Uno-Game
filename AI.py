"""
This file contains AI class.
"""

from Player import *


class AI(Player):
    def __init__(self):
        super().__init__()

    def makeAIMove(self, board):
        if self.hasPlaceableCard(board):
            for card in self.hand:
                if self.checkCard(card, board):
                    self.makeMove(card, board)
                    break
        else:
            self.pickCard(board)
            if self.checkCard(self.hand[-1], board):
                self.makeMove(self.hand[-1], board)
