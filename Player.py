"""
This file contains Player class.
"""

import Cards
import Button
import pygame as p
from random import choice


class Player:
    def __init__(self, nick):
        self.hand = []
        self.cards_to_take = 0
        self.blocked = False
        self.nick = nick

    # Function to check if card can be placed
    def checkCard(self, picked_card, board):
        top_card = board.discard_pile[-1]
        if isinstance(picked_card, Cards.SpecialCard) and picked_card.wild:
            return True
        elif isinstance(top_card, Cards.SpecialCard) and (top_card.wild or top_card.wild_draw_four) \
                and top_card.wild_color_choice == picked_card.color:
            return True
        elif isinstance(top_card, Cards.SpecialCard) and picked_card.color == top_card.color:
            return True
        elif isinstance(top_card, Cards.SpecialCard) and \
                isinstance(picked_card, Cards.SpecialCard) and ((picked_card.block and top_card.block) or
                                                                (picked_card.reverse and top_card.reverse) or
                                                                (picked_card.draw == 2 and top_card.draw == 2)):
            return True
        elif picked_card.color == top_card.color or \
                (not isinstance(picked_card, Cards.SpecialCard) and not isinstance(top_card, Cards.SpecialCard) and
                 picked_card.value == top_card.value):
            return True
        else:
            return False

    # Function to display a screen that asks player to pick a color
    def AskForAColor(self):
        colors = {'B': 0, 'G': 0, 'Y': 0, 'R': 0, 'N': 0}

        for card in self.hand:
            colors[card.color] += 1

        width = 1080

        blue_button = Button.Button(image=p.image.load("images/button.png"), pos=(width // 2, 200),
                                    text_input="BLUE [" + str(colors['B']) + "]",
                                    font=p.font.SysFont("Comic Sans", 40, True),
                                    base_color="#082869", hovering_color="#0D53DE")
        green_button = Button.Button(image=p.image.load("images/button.png"), pos=(width // 2, 350),
                                     text_input="GREEN [" + str(colors['G']) + "]",
                                     font=p.font.SysFont("Comic Sans", 40, True),
                                     base_color="#0E6908", hovering_color="#17DE0B")
        yellow_button = Button.Button(image=p.image.load("images/button.png"), pos=(width // 2, 500),
                                      text_input="YELLOW [" + str(colors['Y']) + "]",
                                      font=p.font.SysFont("Comic Sans", 40, True),
                                      base_color="#69700F", hovering_color="#DFF007")
        red_button = Button.Button(image=p.image.load("images/button.png"), pos=(width // 2, 650),
                                   text_input="RED [" + str(colors['R']) + "]",
                                   font=p.font.SysFont("Comic Sans", 40, True),
                                   base_color="#750B0B", hovering_color="#FA0202")

        p.init()
        screen = p.display.set_mode((1080, 720))
        bg = p.image.load('images/color_choice.png')

        running = True
        while running:

            screen.fill('black')
            screen.blit(bg, (0, 0))

            text = Button.get_font(70).render("PICK A COLOR", True, "#000000")
            text_rect = text.get_rect(center=(1080 // 2, 50))

            screen.blit(text, text_rect)

            blue_button.update(screen)
            green_button.update(screen)
            yellow_button.update(screen)
            red_button.update(screen)

            blue_button.changeColor(p.mouse.get_pos())
            green_button.changeColor(p.mouse.get_pos())
            yellow_button.changeColor(p.mouse.get_pos())
            red_button.changeColor(p.mouse.get_pos())

            for e in p.event.get():
                if e.type == p.QUIT:
                    return 'B'
                    running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    if blue_button.checkForInput(p.mouse.get_pos()):
                        return 'B'
                    elif green_button.checkForInput(p.mouse.get_pos()):
                        return 'G'
                    elif yellow_button.checkForInput(p.mouse.get_pos()):
                        return 'Y'
                    elif red_button.checkForInput(p.mouse.get_pos()):
                        return 'R'
                    running = False
            p.display.update()

    # Function to make a move
    def makeMove(self, picked_card, board, gamestate):

        if isinstance(board.discard_pile[-1], Cards.SpecialCard) and board.discard_pile[-1].wild:
            board.discard_pile[-1].wild_color_choice = None

        board.discard_pile.append(picked_card)
        self.hand.remove(picked_card)

        if isinstance(picked_card, Cards.SpecialCard) and picked_card.wild:
            if gamestate.queue[0] == gamestate.player:
                color = self.AskForAColor()
                picked_card.wild_color_choice = color
            else:
                colors = {'B': 0, 'G': 0, 'Y': 0, 'R': 0, 'N': 0}
                for card in self.hand:
                    colors[card.color] += 1

                max_color = max(colors.items(), key=lambda x: x[1])[0]

                picked_card.wild_color_choice = max_color
                print("[Log] AI picked " + max_color + " color!")

        if isinstance(picked_card, Cards.SpecialCard) and picked_card.draw != 0:
            gamestate.queue[1].cards_to_take += picked_card.draw

        if isinstance(picked_card, Cards.SpecialCard) and picked_card.reverse:
            current_player = gamestate.queue.pop(0)
            gamestate.queue.reverse()
            gamestate.queue.insert(0, current_player)
            board.reversed_queue = not board.reversed_queue

        if isinstance(picked_card, Cards.SpecialCard) and picked_card.block:
            gamestate.queue[1].blocked = True

    # Function to check if any card in player's hand can be placed
    def hasPlaceableCard(self, board):
        for card in self.hand:
            if self.checkCard(card, board):
                return True

        return False

    # Function to pick a card from a draw pile
    def pickCard(self, board):
        taken_card = board.draw_pile.pop()
        self.hand.append(taken_card)

    # Function to generate coordinates of cards in Player's hand
    def genCoords(self):

        width = 1080
        height = 720

        lenP = len(self.hand)

        coords = []

        j = 0
        if lenP > 4:
            for card in self.hand:
                coords.append([card, (120 + ((width - 20) / lenP) * j), height - 150])
                j += 1
        elif lenP == 1:
            card = self.hand[0]
            coords.append([card, width / 2, height - 150])
        elif lenP > 0:
            for card in self.hand:
                coords.append([card, (220 + ((width - 120) / lenP) * j), height - 150])
                j += 1

        return coords
