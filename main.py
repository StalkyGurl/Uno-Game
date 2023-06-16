"""
This is the main file that creates the new main menu and runs it
"""

import pygame as p
import MainMenu


# The main function
def main():

    width = 1080
    height = 720
    fps = 30

    p.init()
    p.display.set_caption('Uno')
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    bg = p.image.load('images/menu.png')
    bg = p.transform.scale(bg, (width, height))

    main_menu = MainMenu.MainMenu(width, screen, bg, clock, fps)
    main_menu.start()


if __name__ == '__main__':
    main()
