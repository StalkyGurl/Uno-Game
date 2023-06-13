"""
This file contains MainMenu class.
"""

import sys
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

    def askForNick(self):
        p.init()
        screen = p.display.set_mode((1080, 720))
        bg = p.image.load('images/deck.png')
        bg = p.transform.scale(bg, (1080, 720))
        clock = p.time.Clock()

        font = p.font.SysFont("Arial", 60)

        input_box = p.Rect(150, 300, 820, 80)
        color_inactive = p.Color('black')
        color_active = p.Color('white')
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            screen.blit(bg, (0, 0))

            text_title = Button.get_font(50).render("TYPE YOUR NAME AND PRESS ENTER", True, "#000000")
            text_rect = text_title.get_rect(center=(1080 // 2, 150))

            screen.blit(text_title, text_rect)

            for event in p.event.get():
                if event.type == p.QUIT:
                    done = True
                    game = GameState.GameState("Player")
                    game.play(self.screen, self.clock, self.FPS)
                if event.type == p.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == p.KEYDOWN:
                    if active:
                        if event.key == p.K_RETURN:
                            done = True
                            game = GameState.GameState(text)
                            game.play(self.screen, self.clock, self.FPS)
                        elif event.key == p.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            txt_surface = font.render(str(text), True, color)
            input_box.w = 820
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            p.draw.rect(screen, color, input_box, 2)

            p.display.flip()
            clock.tick(60)

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

            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    sys.exit()
                if e.type == p.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.askForNick()
                        #game = GameState.GameState()
                        #game.play(self.screen, self.bg, self.clock, self.FPS)
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        p.quit()
                        sys.exit()
                if e.type == p.KEYDOWN:
                    if e.key == p.K_ESCAPE:
                        p.quit()
                        sys.exit()

            p.display.update()