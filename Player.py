"""
This file contains Player class.
"""

import Cards
import GameState

class Player:
    def __init__(self, hand, cards_to_take=0, blocked=False):
        self.hand = hand
        self.cards_to_take = cards_to_take
        self.blocked = blocked

    # Function to check if card can be placed
    def checkCard(self, picked_card, top_card):
        if isinstance(picked_card, Cards.SpecialCard) and picked_card.wild:
            return True
        elif isinstance(top_card, Cards.SpecialCard) and top_card.wild and top_card.wild_color_choice == top_card.color:
            return True
        elif isinstance(top_card, Cards.SpecialCard):
            if picked_card.color == top_card.color:
                return True
            elif isinstance(picked_card, Cards.SpecialCard) and (picked_card.block and top_card.block) or \
                    (picked_card.reverse and top_card.reverse) or (picked_card.block and top_card.block):
                return True
            else:
                return False
        elif picked_card.color == top_card.color or \
                (not isinstance(picked_card, Cards.SpecialCard) and picked_card.value == picked_card.value):
            return True
        else:
            return False

    # Function to make a move
    def makeMove(self, picked_card, board, gamestate):
        top_card = board.discard_pile[-1]
        if self.checkCard(picked_card, top_card):
            board.discard_pile.append(picked_card)
            self.hand.remove(picked_card)
            gamestate.switchTurn(board)

    # Function to generate coordinates of cards in Player's hand
    def genCoords(self):

        width = 1080
        height = 720

        lenP = len(self.hand)

        coords = []

        j = 0
        for card in self.hand:
            coords.append([card, (120 + ((width - 2 * 10) / lenP) * j), height - 150])
            j += 1

        return(coords)
