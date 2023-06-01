"""
This is the main driver class in the game.
"""

import pygame as p
import Player
import Board
from queue import Queue


class GameState:
    def __init__(self):
        self.player = Player.Player([])
        self.ai1 = Player.Player([])
        self.ai2 = Player.Player([])
        self.ai3 = Player.Player([])
        self.queue = Queue()
        self.queue.put(self.player)
        self.queue.put(self.ai1)
        self.queue.put(self.ai2)
        self.queue.put(self.ai3)



    def play(self, screen, bg, clock, FPS):


        board = Board.Board()
        board.prepare_piles()
        board.deal_the_cards(self.player, self.ai1, self.ai2, self.ai3)

        running = True

        while running:
            screen.fill('black')
            screen.blit(bg, (0, 0))
            board.display_cards(self.player, self.ai1, self.ai2, self.ai3, screen)

            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    pass

            p.display.flip()
            clock.tick(FPS)
