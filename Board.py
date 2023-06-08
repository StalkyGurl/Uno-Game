"""
This file contains Board class.
"""

from Player import *
from random import shuffle
import pygame as p


WIDTH = 1080
HEIGHT = 720


class Board:
    def __init__(self):
        self.discard_pile = []
        self.draw_pile = []

    def prepare_piles(self):
        card_deck = Cards.generate_list_of_cards()
        shuffle(card_deck)

        for card in card_deck:
            if not isinstance(card, Cards.SpecialCard) or (isinstance(card, Cards.SpecialCard) and not card.wild):
                self.discard_pile.append(card)
                card_deck.remove(card)
                self.draw_pile = card_deck
                break

    def complete_piles(self):
        if len(self.draw_pile) <= 5:
            cards_to_move = self.discard_pile[:-1]
            self.discard_pile = self.discard_pile[-1]
            shuffle(cards_to_move)
            self.draw_pile.extend(cards_to_move)
        elif len(self.discard_pile) == 0:
            self.discard_pile.append(self.draw_pile.pop())

    def deal_the_cards(self, players):
        for player in players:
            for _ in range(7):
                player.hand.append(self.draw_pile.pop())

    def display_cards(self, p1, a2, a3, a4, screen):

        card_height = 220
        card_width = 140

        back_card = p.image.load('images/back.png')
        back_card = p.transform.scale(back_card, (card_width, card_height))
        back_card_s = p.transform.scale(back_card, (card_width - 50, card_height - 60))
        back_card_r = p.transform.rotate(back_card_s, 90)
        back_card_l = p.transform.rotate(back_card_r, 180)
        screen.blit(back_card, (WIDTH // 2 - 200, HEIGHT // 2 - 120))
        self.discard_pile[-1].drawCard(screen, WIDTH // 2 + 120, HEIGHT // 2 - 50)

        lenP = len(p1.hand)
        len2 = len(a2.hand)
        len3 = len(a3.hand)
        len4 = len(a4.hand)

        j = 0
        for card in p1.hand:
            card.drawCard(screen, (120 + ((WIDTH - 2 * 10) / lenP) * j), HEIGHT - 150)
            j += 1

        for i in range(len2):
            screen.blit(back_card_l, (40, (150 - ((HEIGHT - 2 * 150) // len2) * i + 250)))

        for i in range(len3):
            screen.blit(back_card_s, ((250 + ((WIDTH - 2 * 250) // len3) * i), 10))

        for i in range(len4):
            screen.blit(back_card_r, (WIDTH - 200, (150 - ((HEIGHT - 2 * 150) // len2) * i + 250)))
