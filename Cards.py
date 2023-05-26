"""
This file contains Card class and the function to load cards.
"""

import pygame as p
import os

class Card():
    def __init__(self, value, color):
        self.value = value
        self.color = color

def load_cards():

    folder_path = 'images/cards'

    # Scaling the all th cards
    card_height = 70
    card_width = 50

    # Loading all cards images
    card_name_list = os.listdir(folder_path)
    cards = dict()

    for image_name in card_name_list:
        name = image_name[:-4]
        cards[name] = p.image.load("images/cards/" + image_name)
        cards[name] = p.transform.scale(cards[name], (card_height, card_width))

    back_card = p.image.load('images/back.png')
    back_card = p.transform.scale(back_card, (card_height, card_width))
