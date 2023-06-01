"""
This file contains Player class.
"""

import Cards


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
        elif isinstance(top_card, Cards.SpecialCard) and (top_card.block or top_card.reverse or top_card.draw or
                                                          picked_card.block or picked_card.reverse or picked_card.draw):
            if picked_card.color == top_card.color:
                return True
            else:
                return False
        elif picked_card.color == top_card.color or picked_card.value == picked_card.value:
            return True
        else:
            return False


    # Function to make a move
    def makeMove(self, picked_card, board):
        top_card = board.discard_pile[-1]
        if self.checkCard(picked_card, top_card):
            self.hand.remove(picked_card)
            board.discard_pile.append(picked_card)
