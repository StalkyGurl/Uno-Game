"""
This is the main driver class in the game.
"""

import pygame as p
import Player
import AI
import Board


class GameState:
    def __init__(self):
        self.player = Player.Player()
        self.ai1 = AI.AI()
        self.ai2 = AI.AI()
        self.ai3 = AI.AI()
        self.queue = []
        self.queue.append(self.player)
        self.queue.append(self.ai1)
        self.queue.append(self.ai2)
        self.queue.append(self.ai3)

    # Function that switches turns
    def switchTurn(self, board):
        board.complete_piles()
        old_turn = self.queue.pop(0)
        self.queue.append(old_turn)

    # Function to check if someone won
    def checkWin(self):
        for player in self.queue:
            if len(player.hand) == 0:
                self.queue.remove(player)
                return player

    # Function to check if the game has ended
    def checkEnd(self):
        if len(self.queue) == 1:
            return True
        else:
            return False

    # Function to print end game score and ranking
    def printEndGame(self):
        pass

    # Function that makes all the actions connected to AI turn
    def AITurn(self, board):
        activeAI = self.queue[0]
        activeAI.makeAIMove(board)
        self.switchTurn(board)

        winner = self.checkWin()  # maybe later I will add here something

        # When the game ends
        if self.checkEnd():
            self.printEndGame()

    # The most important function, function to play the game
    def play(self, screen, bg, clock, FPS):

        width = 1080
        height = 720

        board = Board.Board()
        board.prepare_piles()
        board.deal_the_cards(self.queue)

        running = True
        picked_card = None
        added_card = False
        coords = self.player.genCoords()

        draw_rect = p.Rect(width // 2 - 200, height // 2 - 120, 140, 220)
        discard_rect = p.Rect(width // 2 + 10, height // 2 - 120, 140, 220)

        while running:
            screen.fill('black')
            screen.blit(bg, (0, 0))
            board.display_cards(self.player, self.ai1, self.ai2, self.ai3, screen)

            # Player actions
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    if self.queue[0] == self.player:
                        if discard_rect.collidepoint(e.pos):
                            try:
                                if self.player.checkCard(picked_card, board):
                                    self.player.makeMove(picked_card, board)
                                    picked_card = None
                                    added_card = False
                                    coords = self.player.genCoords()
                                    self.switchTurn(board)
                                    winner = self.checkWin() # maybe later I will add here something

                                    # When the game ends
                                    if self.checkEnd():
                                        self.printEndGame()

                            except:
                                pass

                        elif draw_rect.collidepoint(e.pos):
                            if not self.player.hasPlaceableCard(board) and not added_card:
                                self.player.pickCard(board)
                                added_card = True
                                coords = self.player.genCoords()
                                if not self.player.hasPlaceableCard(board):
                                    self.switchTurn(board)
                                    added_card = False

                        else:
                            for coord in coords:
                                rect = p.Rect(coord[1] - 110, coord[2] - 70, 140, 220)
                                if rect.collidepoint(e.pos):
                                    picked_card = coord[0]

            # AI actions:
            if self.queue[0] != self.player:
               self.AITurn(board)

            p.display.flip()
            clock.tick(FPS)
