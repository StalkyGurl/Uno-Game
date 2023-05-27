"""
This file contains Player class.
"""


class Player:
    def __init__(self, hand, cards_to_take=0, blocked=False):
        self.hand = hand
        self.cards_to_take = cards_to_take
        self.blocked = blocked
