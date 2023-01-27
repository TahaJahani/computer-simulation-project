import time
import pygame
from pygame.rect import *



SIZE = 1000, 400
RED = (255, 0, 0)
GRAY = (150, 150, 150)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode(SIZE)

rect = pygame.Rect(100, 50, 50, 50)
v = [1, 1]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    rect.move_ip(v)

    if rect.left < 0:
        v[0] *= -1
    if rect.right > SIZE[0]:
        v[0] *= -1
    if rect.top < 0:
        v[1] *= -1
    if rect.bottom > SIZE[1]:
        v[1] *= -1

    screen.fill(GRAY)
    pygame.draw.rect(screen, RED, rect, 0)
    pygame.display.flip()
    time.sleep(0.001)

pygame.quit()