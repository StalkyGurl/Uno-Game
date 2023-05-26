"""
This file contains MainMenu class.
"""

import os
import pygame as p
import Button
import GameState

class MainMenu():
    def __init__(self, width, screen, bg, clock, FPS):
        self.width = width
        self.screen = screen
        self.bg = bg
        self.clock = clock
        self.FPS = FPS
    def start(self):

        running = True
        while running:
            self.screen.blit(self.bg, (0, 0))
            MENU_MOUSE_POS = p.mouse.get_pos()
            MENU_TEXT = Button.get_font(70).render("UNO CARD GAME", True, "#000000")
            MENU_RECT = MENU_TEXT.get_rect(center=(self.width // 2, 100))

            PLAY_BUTTON = Button.Button(image=p.image.load("images/button.png"), pos=(self.width // 2, 300),
                                text_input="PLAY", font=Button.get_font(40), base_color="#000000",
                                hovering_color="#FFFFFF")
            QUIT_BUTTON = Button.Button(image=p.image.load("images/button.png"), pos=(self.width // 2, 500),
                                 text_input="QUIT", font=Button.get_font(40), base_color="#000000", hovering_color="#FFFFFF")

            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    running = False
                if event.type == p.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        game = GameState.GameState()
                        game.play(self.screen, self.bg, self.clock, self.FPS)
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        p.quit()
                        running = False

            p.display.update()