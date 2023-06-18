"""
This file contains Board class
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
        self.reversed_queue = False

    # Function that prepares and shuffles piles of cards
    def prepare_piles(self):
        card_deck = Cards.generate_list_of_cards()
        shuffle(card_deck)

        for card in card_deck:
            if not isinstance(card, Cards.SpecialCard) or (isinstance(card, Cards.SpecialCard) and not card.wild):
                self.discard_pile.append(card)
                card_deck.remove(card)
                self.draw_pile = card_deck
                break

    # Function to complete piles if necessary
    def complete_piles(self):
        if len(self.draw_pile) <= 5:
            cards_to_move = self.discard_pile[:-1]
            self.discard_pile = [self.discard_pile[-1]]
            shuffle(cards_to_move)
            self.draw_pile.extend(cards_to_move)
        elif len(self.discard_pile) == 0:
            self.discard_pile.append(self.draw_pile.pop())

    # Function that deals the cards to all players
    def deal_the_cards(self, players):
        for player in players:
            for _ in range(7):
                player.hand.append(self.draw_pile.pop())

    # Function that displays cards on screen
    def display_cards(self, turn, p1, a2, a3, a4, screen, picked_card, cards):
        # Show arrows
        if self.reversed_queue:
            arrow = p.image.load('images/right.png')
            screen.blit(arrow, (735, 350))
        else:
            arrow = p.image.load('images/left.png')
            screen.blit(arrow, (225, 350))

        lenP = len(p1.hand)
        len2 = len(a2.hand)
        len3 = len(a3.hand)
        len4 = len(a4.hand)

        # Show nicknames and card amount
        if len2 > 0:
            if turn == a2:
                a2_name = p.font.SysFont("Comic Sans", 25).render(a2.nick + " [" + str(len2) + "]", True, "#FF7870")
            else:
                a2_name = p.font.SysFont("Comic Sans", 25).render(a2.nick + " [" + str(len2) + "]", True, "#FFFFFF")
            a2_name = p.transform.rotate(a2_name, 90)
            a2_name_rect = a2_name.get_rect(center=(20, 275))
            screen.blit(a2_name, a2_name_rect)

        if len3 > 0:
            if turn == a3:
                a3_name = p.font.SysFont("Comic Sans", 25).render(a3.nick + " [" + str(len3) + "]", True, "#FF7870")
            else:
                a3_name = p.font.SysFont("Comic Sans", 25).render(a3.nick + " [" + str(len3) + "]", True, "#FFFFFF")
            a3_name_rect = a3_name.get_rect(center=(540, 20))
            screen.blit(a3_name, a3_name_rect)

        if len4 > 0:
            if turn == a4:
                a4_name = p.font.SysFont("Comic Sans", 25).render(a4.nick + " [" + str(len4) + "]", True, "#FF7870")
            else:
                a4_name = p.font.SysFont("Comic Sans", 25).render(a4.nick + " [" + str(len4) + "]", True, "#FFFFFF")
            a4_name = p.transform.rotate(a4_name, 270)
            a4_name_rect = a4_name.get_rect(center=(1060, 275))
            screen.blit(a4_name, a4_name_rect)

        # Show piles
        card_height = 220
        card_width = 140

        back_card = p.image.load('images/back.png')
        back_card = p.transform.scale(back_card, (card_width, card_height))
        back_card_s = p.transform.scale(back_card, (card_width - 60, card_height - 75))
        back_card_r = p.transform.rotate(back_card_s, 90)
        back_card_l = p.transform.rotate(back_card_r, 180)

        screen.blit(back_card, (WIDTH // 2 - 200, HEIGHT // 2 - 120))

        last_card = self.discard_pile[-1]

        if isinstance(last_card, Cards.SpecialCard) and last_card.wild and \
                self.discard_pile[-1].wild_color_choice is not None:

            rectangle_width = 150
            rectangle_height = 230

            rectangle_x = WIDTH // 2 + 10 - 5
            rectangle_y = HEIGHT // 2 - 120 - 5

            color = last_card.wild_color_choice

            if color == 'B':
                p.draw.rect(screen, (0, 135, 245), (rectangle_x, rectangle_y, rectangle_width, rectangle_height), 5)
            elif color == 'G':
                p.draw.rect(screen, (0, 245, 0), (rectangle_x, rectangle_y, rectangle_width, rectangle_height), 5)
            elif color == 'Y':
                p.draw.rect(screen, (245, 245, 0), (rectangle_x, rectangle_y, rectangle_width, rectangle_height), 5)
            else:
                p.draw.rect(screen, (245, 0, 0), (rectangle_x, rectangle_y, rectangle_width, rectangle_height), 5)

        last_card.draw_card(screen, WIDTH // 2 + 120, HEIGHT // 2 - 50, cards)

        # Show player's cards
        j = 0
        if lenP > 4:
            for card in p1.hand:
                if card == picked_card:
                    card.draw_card(screen, (140 + ((WIDTH - 110) / lenP) * j), HEIGHT - 170, cards)
                else:
                    card.draw_card(screen, (140 + ((WIDTH - 110) / lenP) * j), HEIGHT - 150, cards)
                j += 1

        elif lenP == 1:
            card = p1.hand[0]
            if card == picked_card:
                card.draw_card(screen, WIDTH / 2, HEIGHT - 170, cards)
            else:
                card.draw_card(screen, WIDTH / 2, HEIGHT - 150, cards)

        elif lenP > 0:
            for card in p1.hand:
                if card == picked_card:
                    card.draw_card(screen, (250 + ((WIDTH - 150) / lenP) * j), HEIGHT - 170, cards)
                else:
                    card.draw_card(screen, (250 + ((WIDTH - 150) / lenP) * j), HEIGHT - 150, cards)
                j += 1

        # Show AI's cards
        if len2 > 20:
            for i in range(20):
                screen.blit(back_card_l, (40, (150 - ((HEIGHT - 300) / 20) * i + 250)))
        elif len2 > 4:
            for i in range(len2):
                screen.blit(back_card_l, (40, (150 - ((HEIGHT - 300) / len2) * i + 250)))
        elif len2 > 0:
            for i in range(len2):
                screen.blit(back_card_l, (40, (150 - ((HEIGHT - 400) / len2) * i + 250)))

        if len3 > 20:
            for i in range(20):
                screen.blit(back_card_s, ((250 + ((WIDTH - 500) / 20) * i), 40))
        elif len3 > 4:
            for i in range(len3):
                screen.blit(back_card_s, ((250 + ((WIDTH - 500) / len3) * i), 40))
        elif len3 > 0:
            for i in range(len3):
                screen.blit(back_card_s, ((350 + ((WIDTH - 700) / len3) * i), 40))

        if len4 > 20:
            for i in range(20):
                screen.blit(back_card_r, (WIDTH - 200, (150 - ((HEIGHT - 300) / 20) * i + 250)))
        elif len4 > 4:
            for i in range(len4):
                screen.blit(back_card_r, (WIDTH - 200, (150 - ((HEIGHT - 300) / len4) * i + 250)))
        elif len4 > 0:
            for i in range(len4):
                screen.blit(back_card_r, (WIDTH - 200, (150 - ((HEIGHT - 400) / len4) * i + 250)))
