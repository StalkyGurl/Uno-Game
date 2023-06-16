"""
This is the main driver class of the game
"""

import pygame as p
import Player
import AI
import Board


class GameState:
    def __init__(self, name):
        self.player = Player.Player(name)
        self.ai1 = AI.AI()
        self.ai2 = AI.AI()
        self.ai3 = AI.AI()

        self.queue = []
        self.queue.append(self.player)
        self.queue.append(self.ai3)
        self.queue.append(self.ai2)
        self.queue.append(self.ai1)

        self.podium = []

    # Function that switches turns
    def switch_turn(self, board):
        board.complete_piles()
        old_turn = self.queue.pop(0)
        self.queue.append(old_turn)
        player_text = "Player's" if self.queue[0] == self.player else self.queue[0].nick
        print("[Log] Now it's " + player_text + "'s turn!")
        if self.queue[0].blocked:
            self.queue[0].blocked = False
            player_text = "Player" if self.queue[0] == self.player else self.queue[0].nick
            print("[Log] " + player_text + " is blocked!")
            self.switch_turn(board)
        elif self.queue[0].cards_to_take > 0:
            player_text = "Player" if self.queue[0] == self.player else self.queue[0].nick
            print("[Log] " + player_text + " needs to take " + str(self.queue[0].cards_to_take) + " cards!")
            for _ in range(self.queue[0].cards_to_take):
                self.queue[0].pick_card(board)
            self.queue[0].cards_to_take = 0
            self.switch_turn(board)

    # Function to check if someone won
    def check_win(self):
        for player in self.queue:
            if len(player.hand) == 0:
                self.queue.remove(player)
                player_text = "player" if player == self.player else player.nick
                print("[Log] Player " + player_text + " finished the game!")
                return player

    # Function to check if the game has ended
    def check_end(self):
        if len(self.queue) == 1:
            print("[Log] The game has ended. Only 1 player left!")
            return True
        else:
            return False

    # Function to print end game screen and podium
    def print_end_screen(self):
        while len(self.queue) > 0:
            min_cards = 1000
            next_player = None
            for player in self.queue:
                if len(player.hand) < min_cards:
                    min_cards = len(player.hand)
                    next_player = player
            self.queue.remove(next_player)
            self.podium.append(next_player)

        ranking = ""
        i = 1

        for player in self.podium:
            if player is not None:
                ranking += str(i) + ". " + player.nick + "\n"
                i += 1

        p.init()
        screen = p.display.set_mode((1080, 720))
        bg = p.image.load('images/results.jpg')
        bg = p.transform.scale(bg, (1080, 720))

        running = True

        while running:
            screen.fill('black')
            screen.blit(bg, (0, 0))

            text1 = p.font.SysFont("Comic Sans", 60).render("Podium:", True, "#FFFFFF")
            text1_rect = text1.get_rect(center=(1080 // 2, 225))
            screen.blit(text1, text1_rect)

            text_lines = ranking.splitlines()
            texts = {}
            text_rects = {}

            colors = [(155, 215, 200),
                      (215, 165, 15),
                      (150, 150, 150),
                      (90, 50, 30)]

            for idx, line in enumerate(text_lines):
                color = colors[idx % len(colors)]
                texts[line] = p.font.SysFont("Comic Sans", 45).render(line, True, color)
                text_rects[line] = texts[line].get_rect(center=(1080 // 2, 325 + idx * 70))
                screen.blit(texts[line], text_rects[line])

            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_ESCAPE:
                        running = False

            p.display.update()

    # Function that makes all the actions connected to AI turn
    def ai_turn(self, board, ):
        activeAI = self.queue[0]
        activeAI.make_ai_move(board, self)
        self.switch_turn(board)

        winner = self.check_win()
        self.podium.append(winner)

    # Function to run the game
    def play(self, screen, clock, fps):

        width = 1080
        height = 720

        bg = p.image.load('images/deck.png')
        bg = p.transform.scale(bg, (width, height))

        board = Board.Board()
        board.prepare_piles()
        board.deal_the_cards(self.queue)

        running = True
        picked_card = None
        added_card = False
        coords = self.player.gen_coords()

        draw_rect = p.Rect(width // 2 - 200, height // 2 - 120, 140, 220)
        discard_rect = p.Rect(width // 2 + 10, height // 2 - 120, 140, 220)

        while running:
            screen.blit(bg, (0, 0))
            board.display_cards(self.queue[0], self.player, self.ai1, self.ai2, self.ai3, screen, picked_card)

            # Player actions
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_ESCAPE:
                        running = False
                        self.print_end_screen()
                elif e.type == p.MOUSEBUTTONDOWN:
                    if len(self.queue) > 0 and self.queue[0] == self.player:
                        if discard_rect.collidepoint(e.pos):
                            try:
                                if self.player.check_card(picked_card, board):
                                    self.player.make_move(picked_card, board, self)
                                    picked_card = None
                                    added_card = False
                                    coords = self.player.gen_coords()
                                    self.switch_turn(board)
                                    winner = self.check_win()
                                    self.podium.append(winner)

                                    # When the game ends
                                    if self.check_end():
                                        running = False
                                        self.print_end_screen()

                                else:
                                    print("You cannot place this card!")

                            except:
                                pass

                        elif draw_rect.collidepoint(e.pos):
                            if not added_card:
                                self.player.pick_card(board)
                                added_card = True
                                coords = self.player.gen_coords()
                                if not self.player.has_placeable_card(board):
                                    self.switch_turn(board)
                                    added_card = False
                            else:
                                self.switch_turn(board)
                                added_card = False

                        else:
                            for coord in coords:
                                rect = p.Rect(coord[1] - 110, coord[2] - 70, 140, 220)
                                if rect.collidepoint(e.pos):
                                    picked_card = coord[0]
                                    print("You picked " + picked_card.id + " card!")

            # AI actions:
            if len(self.queue) > 0 and self.queue[0] != self.player:
                self.ai_turn(board, self)
                coords = self.player.gen_coords()

                # When the game ends
                if self.check_end():
                    running = False
                    self.print_end_screen()

            p.display.flip()
            clock.tick(fps)
