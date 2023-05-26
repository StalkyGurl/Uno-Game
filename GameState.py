"""
This is the main driver class in the game.
"""

import pygame as p
import Cards
class GameState():
    def __init__(self):
        pass

    def play(self, screen, bg, clock, FPS):

        Cards.load_cards()
        running = True

        while running:
            screen.fill('black')
            screen.blit(bg, (0, 0))
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
            p.display.flip()
            clock.tick(FPS)