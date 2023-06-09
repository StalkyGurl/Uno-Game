"""
This file contains AI class.
"""

from Player import *
from random import choice, randint


class AI(Player):
    def __init__(self):
        super().__init__()
        self.nick = self.generateNickname()

    # Function to generate random nickname for AI
    def generateNickname(self):
        prefixes = ["lady", "miss", "mister", "master", "funny", "crazy", "lord", "dr",
                    "desperate", "incredible", "cheesy", "xxx", "x", "xXx", "stalky", "sneaky",
                    "king", "queen"]
        names = ["pizza", "doggo", "kitten", "ghost", "killer", "cousin", "teddy", "potato",
                 "spaghetti", "cheese", "slayer", "dragon", "panda", "donut", "icecream", "girl",
                 "boy", "gurl", "boi"]
        numbers = "0123456789"
        symbols = "_- "

        nick = ''
        nick += choice(prefixes)
        nick += symbols[randint(0, 2)]
        nick += choice(names)

        for _ in range(randint(0, 3)):
            nick += numbers[randint(0, 9)]

        return nick

    # Function to generate random AI move
    def makeAIMove(self, board, gamestate):
        if self.hasPlaceableCard(board):
            for card in self.hand:
                if self.checkCard(card, board):
                    self.makeMove(card, board, gamestate)
                    print("[Log] " + self.nick + " put " + card.id + " card.")
                    break
        else:
            self.pickCard(board)
            print("[Log] " + self.nick + " picked a card from a pile.")
            if self.checkCard(self.hand[-1], board):
                self.makeMove(self.hand[-1], board, gamestate)
                print("[Log] " + self.nick + " put picked card (" + board.discard_pile[-1].id + ")")
