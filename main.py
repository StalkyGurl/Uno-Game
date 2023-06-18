"""
This is the main file that creates the new main menu and runs it
"""

import pygame as p
import MainMenu


# The main function
def main():

    # Settings
    width = 1080
    height = 720
    fps = 30

    # Initializing pygame and making screen and clock
    p.init()
    p.display.set_caption('Uno')
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()

    # Loading and scaling the background
    bg = p.image.load('images/menu.png')
    bg = p.transform.scale(bg, (width, height))

    # Creating and starting the main menu
    main_menu = MainMenu.MainMenu(width, screen, bg, clock, fps)
    main_menu.start()


if __name__ == '__main__':
    main()
