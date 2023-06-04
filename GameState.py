"""
This is the main driver class in the game.
"""

import pygame as p

import Cards
import Player
import Board


class GameState:
    def __init__(self):
        self.player = Player.Player([])
        self.ai1 = Player.Player([])
        self.ai2 = Player.Player([])
        self.ai3 = Player.Player([])
        self.queue = []
        self.queue.append(self.player)
        self.queue.append(self.ai1)
        self.queue.append(self.ai2)
        self.queue.append(self.ai3)


    def switchTurn(self, board):
        board.complete_piles()
        old_turn = self.queue.pop(0)
        self.queue.append(old_turn)


    def play(self, screen, bg, clock, FPS):

        width = 1080
        height = 720

        board = Board.Board()
        board.prepare_piles()
        board.deal_the_cards(self.player, self.ai1, self.ai2, self.ai3)

        running = True
        picked_card = None
        coords = self.player.genCoords()

        draw_rect = p.Rect(width // 2 - 200, height // 2 - 120, 140, 220)
        discard_rect = p.Rect(width // 2 + 10, height // 2 - 120, 140, 220)

        while running:
            screen.fill('black')
            screen.blit(bg, (0, 0))
            board.display_cards(self.player, self.ai1, self.ai2, self.ai3, screen)

            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    if self.queue[0] == self.player:
                        print("yes")
                        if discard_rect.collidepoint(e.pos):
                            try:
                                self.player.makeMove(picked_card, board, self)
                                coords = self.player.genCoords()
                            except:
                                pass
                        else:
                            for coord in coords:
                                rect = p.Rect(coord[1] - 110, coord[2] - 70, 140, 220)
                                if rect.collidepoint(e.pos):
                                    picked_card = coord[0]

            p.display.flip()
            clock.tick(FPS)
