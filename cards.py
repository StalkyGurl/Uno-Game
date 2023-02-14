'''
This is a file that contains all of the cards, Draw pile and Discard pile.
'''

import pygame as p


# Loading all cards images

back = p.image.load('images/back.png')

# Wild cards
wild = p.image.load('images/wild.png')
wild_draw_four = p.image.load('images/wild_draw_4.png')

# Blue cards
B_skip = p.image.load('images/B_block.png')
B_draw_two = p.image.load('images/B_plus_two.png')
B_reverse = p.image.load('images/B_reverse.png')
B_zero = p.image.load('images/B0.png')
B_one = p.image.load('images/B1.png')
B_two = p.image.load('images/B2.png')
B_three = p.image.load('images/B3.png')
B_four = p.image.load('images/B4.png')
B_five = p.image.load('images/B5.png')
B_six = p.image.load('images/B6.png')
B_seven = p.image.load('images/B7.png')
B_eight = p.image.load('images/B8.png')
B_nine = p.image.load('images/B9.png')

# Green cards
G_skip = p.image.load('images/G_block.png')
G_draw_two = p.image.load('images/G_plus_two.png')
G_reverse = p.image.load('images/G_reverse.png')
G_zero = p.image.load('images/G0.png')
G_one = p.image.load('images/G1.png')
G_two = p.image.load('images/G2.png')
G_three = p.image.load('images/G3.png')
G_four = p.image.load('images/G4.png')
G_five = p.image.load('images/G5.png')
G_six = p.image.load('images/G6.png')
G_seven = p.image.load('images/G7.png')
G_eight = p.image.load('images/G8.png')
G_nine = p.image.load('images/G9.png')

# Red cards
R_skip = p.image.load('images/R_block.png')
R_draw_two = p.image.load('images/R_plus_two.png')
R_reverse = p.image.load('images/R_reverse.png')
R_zero = p.image.load('images/R0.png')
R_one = p.image.load('images/R1.png')
R_two = p.image.load('images/R2.png')
R_three = p.image.load('images/R3.png')
R_four = p.image.load('images/R4.png')
R_five = p.image.load('images/R5.png')
R_six = p.image.load('images/R6.png')
R_seven = p.image.load('images/R7.png')
R_eight = p.image.load('images/R8.png')
R_nine = p.image.load('images/R9.png')

# Yellow cards
Y_skip = p.image.load('images/Y_block.png')
Y_draw_two = p.image.load('images/Y_plus_two.png')
Y_reverse = p.image.load('images/Y_reverse.png')
Y_zero = p.image.load('images/Y0.png')
Y_one = p.image.load('images/Y1.png')
Y_two = p.image.load('images/Y2.png')
Y_three = p.image.load('images/Y3.png')
Y_four = p.image.load('images/Y4.png')
Y_five = p.image.load('images/Y5.png')
Y_six = p.image.load('images/Y6.png')
Y_seven = p.image.load('images/Y7.png')
Y_eight = p.image.load('images/Y8.png')
Y_nine = p.image.load('images/Y9.png')

# Scaling the all th cards
card_height = 70
card_width = 50

wild = p.transform.scale(wild, (card_height, card_width))
wild_draw_four = p.transform.scale(wild_draw_four, (card_height, card_width))

B_draw_two = p.transform.scale(B_draw_two, (card_height, card_width))
B_reverse = p.transform.scale(B_reverse, (card_height, card_width))
B_zero = p.transform.scale(B_zero, (card_height, card_width))
B_one = p.transform.scale(B_one, (card_height, card_width))
B_two = p.transform.scale(B_two, (card_height, card_width))
B_three = p.transform.scale(B_three, (card_height, card_width))
B_four = p.transform.scale(B_four, (card_height, card_width))
B_five = p.transform.scale(B_five, (card_height, card_width))
B_six = p.transform.scale(B_six, (card_height, card_width))
B_seven = p.transform.scale(B_seven, (card_height, card_width))
B_eight = p.transform.scale(B_eight, (card_height, card_width))
B_nine = p.transform.scale(B_nine, (card_height, card_width))

G_draw_two = p.transform.scale(G_draw_two, (card_height, card_width))
G_reverse = p.transform.scale(G_reverse, (card_height, card_width))
G_zero = p.transform.scale(G_zero, (card_height, card_width))
G_one = p.transform.scale(G_one, (card_height, card_width))
G_two = p.transform.scale(G_two, (card_height, card_width))
G_three = p.transform.scale(G_three, (card_height, card_width))
G_four = p.transform.scale(G_four, (card_height, card_width))
G_five = p.transform.scale(G_five, (card_height, card_width))
G_six = p.transform.scale(G_six, (card_height, card_width))
G_seven = p.transform.scale(G_seven, (card_height, card_width))
G_eight = p.transform.scale(G_eight, (card_height, card_width))
G_nine = p.transform.scale(G_nine, (card_height, card_width))

R_draw_two = p.transform.scale(R_draw_two, (card_height, card_width))
R_reverse = p.transform.scale(R_reverse, (card_height, card_width))
R_zero = p.transform.scale(R_zero, (card_height, card_width))
R_one = p.transform.scale(R_one, (card_height, card_width))
R_two = p.transform.scale(R_two, (card_height, card_width))
R_three = p.transform.scale(R_three, (card_height, card_width))
R_four = p.transform.scale(R_four, (card_height, card_width))
R_five = p.transform.scale(R_five, (card_height, card_width))
R_six = p.transform.scale(R_six, (card_height, card_width))
R_seven = p.transform.scale(R_seven, (card_height, card_width))
R_eight = p.transform.scale(R_eight, (card_height, card_width))
R_nine = p.transform.scale(R_nine, (card_height, card_width))

Y_draw_two = p.transform.scale(Y_draw_two, (card_height, card_width))
Y_reverse = p.transform.scale(Y_reverse, (card_height, card_width))
Y_zero = p.transform.scale(Y_zero, (card_height, card_width))
Y_one = p.transform.scale(Y_one, (card_height, card_width))
Y_two = p.transform.scale(Y_two, (card_height, card_width))
Y_three = p.transform.scale(Y_three, (card_height, card_width))
Y_four = p.transform.scale(Y_four, (card_height, card_width))
Y_five = p.transform.scale(Y_five, (card_height, card_width))
Y_six = p.transform.scale(Y_six, (card_height, card_width))
Y_seven = p.transform.scale(Y_seven, (card_height, card_width))
Y_eight = p.transform.scale(Y_eight, (card_height, card_width))
Y_nine = p.transform.scale(Y_nine, (card_height, card_width))