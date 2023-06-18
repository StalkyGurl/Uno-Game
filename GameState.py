"""
This file contains Game State Class that runs the game
"""

import pygame as p

import Cards
import Player
import AI
import Board
import sys

CARDS = dict()
SHOW_LOG = False


class GameState:
    def __init__(self, name):
        self.player = Player.Player(name)
        self.ai1 = AI.AI()
        self.ai2 = AI.AI()
        self.ai3 = AI.AI()

        self.queue = []
        self.queue.append(self.player)
        self.queue.append(self.ai1)
        self.queue.append(self.ai2)
        self.queue.append(self.ai3)

        self.podium = []

        self.log = []

    # Function that switches turns
    def switch_turn(self, board):
        board.complete_piles()
        old_turn = self.queue.pop(0)
        self.queue.append(old_turn)
        player_text = "Player" if self.queue[0] == self.player else self.queue[0].nick
        self.log.append("[Log] Now it's " + player_text + "'s turn!")
        if self.queue[0].blocked:
            self.queue[0].blocked = False
            player_text = "Player" if self.queue[0] == self.player else self.queue[0].nick
            self.log.append("[Log] " + player_text + " is blocked!")
            self.switch_turn(board)
        elif self.queue[0].cards_to_take > 0:
            player_text = "Player" if self.queue[0] == self.player else self.queue[0].nick
            self.log.append("[Log] " + player_text + " needs to take " + str(self.queue[0].cards_to_take) + " cards!")
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
                self.log.append("[Log] Player " + player_text + " finished the game!")
                return player

    # Function to check if the game has ended
    def check_end(self):
        if len(self.queue) == 1:
            self.log.append("[Log] The game has ended. Only 1 player left!")
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
            screen.fill((0, 0, 0))
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
    def ai_turn(self, board, screen):
        coord_dict = {self.ai1: (220, 275), self.ai2: (540, 220), self.ai3: (860, 275)}
        activeAI = self.queue[0]
        hand_len = len(activeAI.hand)

        # AI plays faster if Player already won
        if self.player in self.queue:
            p.time.wait(1000)
        else:
            p.time.wait(500)

        activeAI.make_ai_move(board, self)
        new_hand_len = len(activeAI.hand)
        self.switch_turn(board)
        # Play animation if any card was placed
        if new_hand_len <= hand_len:
            self.animate_card(coord_dict[activeAI], (660, 310), board.discard_pile[-1], board, screen, True)
        winner = self.check_win()
        self.podium.append(winner)

    # Function to animate card
    def animate_card(self, start_pos, end_pos, card, board, screen, override):
        global SHOW_LOG

        bg = p.image.load('images/deck.png')
        bg = p.transform.scale(bg, (1080, 720))

        x, y = start_pos
        end_x, end_y = end_pos

        if self.player in self.queue:
            total_frames = 20
        else:
            total_frames = 10

        dx = (end_x - x) / total_frames
        dy = (end_y - y) / total_frames

        for frame in range(total_frames):
            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    sys.exit()
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_l:
                        SHOW_LOG = not SHOW_LOG
                        if SHOW_LOG:
                            screen = p.display.set_mode((1380, 720))
                            self.display_log(screen)
                        else:
                            screen = p.display.set_mode((1080, 720))

            x += dx
            y += dy

            self.update_screen(screen, bg, board, None, False)
            self.display_log(screen)

            if len(board.discard_pile) >= 2 and override:
                last_card = board.discard_pile[-2]
                last_card.draw_card(screen, 660, 310, CARDS)

            card.draw_card(screen, x, y, CARDS)

            p.display.update()

    # Function to display log on the screen
    def display_log(self, screen):
        log = []
        for text in self.log:
            if len(text) > 36:
                log.append(text[:36])
                log.append("-" + text[36:])
            else:
                log.append(text)

        if len(log) > 32:
            log = log[-32:]

        for i, text in enumerate(log):
            text = p.font.SysFont("Arial", 20).render(text, True, "#FFFFFF")
            text_rect = text.get_rect()
            text_rect.left = 1090
            text_rect.top = 5 + (i * 22)
            screen.blit(text, text_rect)

    # Function to update the screen
    def update_screen(self, screen, bg, board, picked_card, if_help):
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        board.display_cards(self.queue[0], self.player, self.ai1, self.ai2, self.ai3, screen, picked_card, CARDS)
        if if_help:
            help_text = p.font.SysFont("Comic Sans", 16, True).render("RIGHT-CLICK FOR HELP!", True, "#FFFFFF")
            help_rect = help_text.get_rect(center=(540, 477))
            screen.blit(help_text, help_rect)

    # Function to run the game
    def play(self, clock, fps):

        # Global variables
        global CARDS
        global SHOW_LOG
        CARDS = Cards.load_cards()

        # Window size
        width = 1080
        height = 720
        log_space = 300

        # Background
        bg = p.image.load('images/deck.png')
        bg = p.transform.scale(bg, (width, height))

        screen = p.display.set_mode((width, height))

        # Board preparations
        board = Board.Board()
        board.prepare_piles()
        board.deal_the_cards(self.queue)

        # If first card is a special card
        if isinstance(board.discard_pile[-1], Cards.SpecialCard):
            if board.discard_pile[-1].block:
                self.log.append("You are blocked!")
                self.switch_turn(board)
            elif board.discard_pile[-1].reverse:
                current_player = self.queue.pop(0)
                self.queue.reverse()
                self.queue.insert(0, current_player)
                board.reversed_queue = not board.reversed_queue
            elif board.discard_pile[-1].draw:
                self.log.append("You have to take 2 cards!")
                self.player.hand.append(board.draw_pile.pop())
                self.player.hand.append(board.draw_pile.pop())
                self.switch_turn(board)

        SHOW_LOG = False
        running = True
        picked_card = None
        added_card = False
        say_uno = False
        help_window_displayed = False
        display_text_help = False
        tick_counter = 0

        coords = self.player.gen_coords()

        draw_rect = p.Rect(width // 2 - 200, height // 2 - 120, 140, 220)
        discard_rect = p.Rect(width // 2 + 10, height // 2 - 120, 140, 220)

        self.update_screen(screen, bg, board, picked_card, display_text_help)

        # The main game loop
        while running:

            # Count the time player spends on thinking and display a tip
            if self.queue[0] == self.player and tick_counter < 420:
                tick_counter += 1
            if tick_counter == 420:
                display_text_help = True
                tick_counter += 1
                self.update_screen(screen, bg, board, picked_card, display_text_help)

            # Player actions
            for e in p.event.get():
                # End the game
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_ESCAPE:
                        running = False
                        self.print_end_screen()
                    # Toggle log
                    if e.key == p.K_l:
                        SHOW_LOG = not SHOW_LOG
                        if SHOW_LOG:
                            screen = p.display.set_mode((width + log_space, height))
                            self.update_screen(screen, bg, board, picked_card, display_text_help)
                            self.display_log(screen)
                        else:
                            screen = p.display.set_mode((width, height))
                            self.update_screen(screen, bg, board, picked_card, display_text_help)

                elif e.type == p.MOUSEBUTTONDOWN and e.button == 1 and not help_window_displayed:
                    if len(self.queue) > 0 and self.queue[0] == self.player:
                        if discard_rect.collidepoint(e.pos):
                            try:
                                if self.player.check_card(picked_card, board):
                                    # Making a move
                                    self.player.make_move(picked_card, board, self)
                                    display_text_help = False
                                    tick_counter = 0
                                    self.log.append("You put " + picked_card.translate_card() + " card!")
                                    if SHOW_LOG:
                                        screen = p.display.set_mode((width + log_space, height))
                                    self.switch_turn(board)
                                    tick_counter = 0
                                    self.update_screen(screen, bg, board, picked_card, display_text_help)
                                    self.display_log(screen)
                                    for coord in coords:
                                        if coord[0] == picked_card:
                                            start_coords = (coord[1], coord[2])
                                            break
                                    self.animate_card(start_coords, (660, 310), picked_card, board, screen, True)

                                    # Uno popup
                                    if len(self.player.hand) == 1:
                                        say_uno = True
                                        if not self.player.display_uno_button(screen,
                                                                              clock, [self.ai1.nick,
                                                                                      self.ai2.nick,
                                                                                      self.ai3.nick], self):
                                            self.player.hand.append(board.draw_pile.pop())
                                            self.player.hand.append(board.draw_pile.pop())
                                        self.update_screen(screen, bg, board, picked_card, display_text_help)
                                        say_uno = False
                                        if SHOW_LOG:
                                            self.display_log(screen)
                                    picked_card = None
                                    added_card = False
                                    coords = self.player.gen_coords()
                                    winner = self.check_win()
                                    self.podium.append(winner)

                                    # When the game ends
                                    if self.check_end():
                                        running = False
                                        self.print_end_screen()

                                else:
                                    # If you cannot place the picked card
                                    self.log.append("You cannot place this card!")
                                    self.update_screen(screen, bg, board, picked_card, display_text_help)
                                    if SHOW_LOG:
                                        self.display_log(screen)

                            except:
                                pass

                        elif draw_rect.collidepoint(e.pos):
                            if not added_card:
                                # Picking a card from a draw pile
                                self.player.pick_card(board)
                                self.log.append("You picked a card from a draw pile!")
                                self.animate_card((440, 340), (540, 520), self.player.hand[-1], board, screen, False)
                                added_card = True
                                coords = self.player.gen_coords()
                                screen.fill((0, 0, 0))
                                screen.blit(bg, (0, 0))

                                # Switch turn if player doesn't have any matching card
                                if not self.player.has_placeable_card(board):
                                    self.switch_turn(board)
                                    added_card = False
                                    picked_card = None
                                else:
                                    self.log.append("Click on draw pile again to skip your turn.")
                            else:
                                self.switch_turn(board)
                                added_card = False
                                picked_card = None

                            self.update_screen(screen, bg, board, picked_card, display_text_help)
                            if SHOW_LOG:
                                self.display_log(screen)

                        else:
                            # Picking any card from Player's hand
                            for coord in coords:
                                rect = p.Rect(coord[1] - 110, coord[2] - 70, 140, 220)
                                if rect.collidepoint(e.pos):
                                    picked_card = coord[0]
                                    self.update_screen(screen, bg, board, picked_card, display_text_help)
                                    self.log.append("You picked " + picked_card.translate_card() + " card!")
                                    if SHOW_LOG:
                                        self.display_log(screen)

                # Displaying help popup
                elif e.type == p.MOUSEBUTTONDOWN and e.button == 3 and not say_uno and not help_window_displayed:
                    if len(self.queue) > 0 and self.queue[0] == self.player:
                        display_text_help = False
                        help_window_displayed = True
                        help_bg = p.image.load('images/help.png')
                        screen.blit(help_bg, (150, 100))
                elif e.type == p.MOUSEBUTTONDOWN and e.button == 3 and help_window_displayed:
                    self.update_screen(screen, bg, board, picked_card, display_text_help)
                    help_window_displayed = False

            # AI actions:
            if len(self.queue) > 0 and self.queue[0] != self.player:
                self.ai_turn(board, screen)
                coords = self.player.gen_coords()
                self.update_screen(screen, bg, board, picked_card, display_text_help)
                if SHOW_LOG:
                    self.display_log(screen)

                # When the game ends
                if self.check_end():
                    running = False
                    self.print_end_screen()

            p.display.flip()
            clock.tick(fps)
