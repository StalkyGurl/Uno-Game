"""
This file contains MainMenu class.
"""

import sys
import pygame as p
import Button
import GameState


class MainMenu:
    def __init__(self, width, screen, bg, clock, fps):
        self.width = width
        self.screen = screen
        self.bg = bg
        self.clock = clock
        self.FPS = fps

    # Function that displays a screen that asks the player for their nickname
    def ask_for_nick(self):
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
                    if len(text) == 0:
                        game = GameState.GameState("Player")
                    else:
                        game = GameState.GameState(text)
                    game.play(self.screen, self.clock, self.FPS)
                if event.type == p.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == p.KEYDOWN:
                    if event.key == p.K_ESCAPE:
                        done = True
                        if len(text) == 0:
                            game = GameState.GameState("Player")
                        else:
                            game = GameState.GameState(text)
                        game.play(self.screen, self.clock, self.FPS)
                    elif active:
                        if event.key == p.K_RETURN:
                            done = True
                            if len(text) == 0:
                                game = GameState.GameState("Player")
                            else:
                                game = GameState.GameState(text)
                            game.play(self.screen, self.clock, self.FPS)
                        elif event.key == p.K_BACKSPACE:
                            text = text[:-1]
                        elif len(text) < 20:
                            text += event.unicode

            txt_surface = font.render(str(text), True, color)
            input_box.w = 820
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            p.draw.rect(screen, color, input_box, 2)

            p.display.flip()
            clock.tick(30)

    # Function that runs the game
    def start(self):

        running = True
        while running:
            self.screen.blit(self.bg, (0, 0))
            menu_mouse_pos = p.mouse.get_pos()
            menu_text = Button.get_font(70).render("UNO CARD GAME", True, "#000000")
            menu_rect = menu_text.get_rect(center=(self.width // 2, 100))

            play_button = Button.Button(image=p.image.load("images/button.png"), pos=(self.width // 2, 300),
                                        text_input="PLAY", font=Button.get_font(40), base_color="#000000",
                                        hovering_color="#FFFFFF")
            quit_button = Button.Button(image=p.image.load("images/button.png"), pos=(self.width // 2, 500),
                                        text_input="QUIT", font=Button.get_font(40), base_color="#000000",
                                        hovering_color="#FFFFFF")

            self.screen.blit(menu_text, menu_rect)

            for button in [play_button, quit_button]:
                button.change_color(menu_mouse_pos)
                button.update(self.screen)

            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    sys.exit()
                if e.type == p.MOUSEBUTTONDOWN:
                    if play_button.check_for_input(menu_mouse_pos):
                        self.ask_for_nick()
                    if quit_button.check_for_input(menu_mouse_pos):
                        p.quit()
                        sys.exit()
                if e.type == p.KEYDOWN:
                    if e.key == p.K_ESCAPE:
                        p.quit()
                        sys.exit()

            p.display.update()
