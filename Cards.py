"""
This file contains Card class and the functions to generate the list of cards and to load cards
"""

import pygame as p
import os

CARDS = dict()


class Card:
    def __init__(self, value, color, id):
        self.value = value
        self.color = color
        self.id = id  # color + value + natural number [0, 1]

    # Function that draws a card on screen
    def draw_card(self, screen, x, y, cards):
        screen.blit(cards[self.color + "_back"], (x - 110, y - 70))
        screen.blit(cards[str(self.value)], (x - 110, y - 70))

    # Function to return the card's name
    def translate_card(self):
        color_dict = {'B': 'Blue ', 'G': 'Green ', 'Y': 'Yellow ', 'R': 'Red '}
        return color_dict[self.color] + str(self.value)

class SpecialCard(Card):
    def __init__(self, color, id, draw=0, block=False,
                 reverse=False, wild=False, wild_draw_four=False):
        self.color = color
        self.id = id  # here id is: color (or none if Wild card)
        # + the name of the card + natural number [0, 3]
        self.draw = draw
        self.block = block
        self.reverse = reverse
        self.wild = wild
        self.wild_draw_four = wild_draw_four
        self.wild_color_choice = None

    # Function that draws a card on screen
    def draw_card(self, screen, x, y, cards):
        if self.wild and not self.wild_draw_four:
            screen.blit(cards["wild"], (x - 110, y - 70))
        elif self.wild and self.wild_draw_four:
            screen.blit(cards["wild+4"], (x - 110, y - 70))
        elif self.block:
            screen.blit(cards[self.color + "_back"], (x - 110, y - 70))
            screen.blit(cards["block"], (x - 110, y - 70))
        elif self.reverse:
            screen.blit(cards[self.color + "_back"], (x - 110, y - 70))
            screen.blit(cards["rev"], (x - 110, y - 70))
        else:
            screen.blit(cards[self.color + "_back"], (x - 110, y - 70))
            screen.blit(cards["+2"], (x - 110, y - 70))

    # Function to return the card's name
    def translate_card(self):
        if self.wild_draw_four:
            return "Wild Draw 4"
        elif self.wild:
            return "Wild"
        elif self.block:
            func = "Skip "
        elif self.reverse:
            func = "Reverse "
        elif self.draw:
            func = "Draw 2 "

        color_dict = {'B': 'blue', 'G': 'green', 'Y': 'yellow', 'R': 'red'}

        return func + color_dict[self.color]

# Function to generate the list of all cards in the game
def generate_list_of_cards():
    list_of_cards = []
    colors = ['B', 'G', 'Y', 'R']

    for color in colors:
        list_of_cards.append(Card(0, color, color + '00'))
        list_of_cards.append(SpecialCard(color, color + 'draw_two' + '0', 2))
        list_of_cards.append(SpecialCard(color, color + 'draw_two' + '1', 2))
        list_of_cards.append(SpecialCard(color, color + 'skip' + '0', 0, True))
        list_of_cards.append(SpecialCard(color, color + 'skip' + '1', 0, True))
        list_of_cards.append(SpecialCard(color, color + 'reverse' + '0', 0, False, True))
        list_of_cards.append(SpecialCard(color, color + 'reverse' + '1', 0, False, True))

        for value in range(1, 3):
            list_of_cards.append(Card(value, color, color + str(value) + '0'))
            list_of_cards.append(Card(value, color, color + str(value) + '1'))

    for number in range(4):
        list_of_cards.append(SpecialCard('N', "Wild" + str(number), 0, False, False, True))
        list_of_cards.append(SpecialCard('N', "Wild_draw_four" + str(number), 4, False, False, True, True))

    return list_of_cards


# Function to load images of cards
def load_cards():

    folder_path = 'images/cards'

    # Scaling the all th cards
    card_height = 220
    card_width = 140

    # Loading all cards images
    card_name_list = os.listdir(folder_path)
    cards = dict()

    for image_name in card_name_list:
        name = image_name[:-4]
        cards[name] = p.image.load("images/cards/" + image_name)
        cards[name] = p.transform.scale(cards[name], (card_width, card_height))

    return cards
