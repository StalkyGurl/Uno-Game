"""
This is a file that contains all the cards, Draw pile and Discard pile.
"""

import pygame as p
import os

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

deck = p.image.load('images/deck.png')
back_card = p.image.load('images/back.png')
back_card = p.transform.scale(back_card, (card_height, card_width))
