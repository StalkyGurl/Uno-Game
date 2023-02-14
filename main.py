'''
This is the main driver file.
'''

import pygame as p

WIDTH = 720
HEIGHT = 480
FPS = 60

p.init()
p.display.set_caption('Uno')
screen = p.display.set_mode((WIDTH,HEIGHT))
clock = p.time.Clock()
bg = p.image.load('images/deck.png')
bg = p.transform.scale(bg, (WIDTH, HEIGHT))


# The main function
def main():
    running = True
    while running:
        screen.fill('black')
        screen.blit(bg, (0, 0))
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        p.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()