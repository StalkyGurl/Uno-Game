'''
This is the main file.
'''

import pygame as p
import MainMenu
import GameState


# The main function
def main():

    WIDTH = 1080
    HEIGHT = 720
    FPS = 60

    p.init()
    p.display.set_caption('Uno')
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    bg = p.image.load('images/deck.png')
    bg = p.transform.scale(bg, (WIDTH, HEIGHT))

    main_menu = MainMenu.MainMenu(WIDTH, screen, bg, clock, FPS)
    main_menu.start()


if __name__ == '__main__':
    main()