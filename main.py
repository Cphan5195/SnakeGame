# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018

@author: zou
"""

from turtle import back
import pygame
import thorpy  # S: imported thorpy
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT

from game import Game

black = pygame.Color(0, 0, 0)
# add game background
gamebackground = pygame.Color(124, 194, 72)
white = pygame.Color(255, 255, 255)

green = pygame.Color(0, 200, 0)
bright_green = pygame.Color(0, 255, 0)
red = pygame.Color(200, 0, 0)
bright_red = pygame.Color(255, 0, 0)
blue = pygame.Color(32, 178, 170)
bright_blue = pygame.Color(32, 200, 200)
yellow = pygame.Color(255, 205, 0)
bright_yellow = pygame.Color(255, 255, 0)

game = Game()
rect_len = game.settings.rect_len
snake = game.snake
pygame.init()
fpsClock = pygame.time.Clock()
# T. create the screen/ can be modified bigger
screen = pygame.display.set_mode(
    (game.settings.width * 15, game.settings.height * 15))
# added background as new way to fill the UI
background = pygame.Surface(
    (game.settings.width * 15, game.settings.height * 15))
background.fill((0, 0, 100))
pygame.display.set_caption('Gluttonous')


thorpy.theme.set_theme('human')
slider = thorpy.SliderX(100, (12, 35), "FUNCTIONAL")
line = thorpy.Line(200, "h")
checker_radio = thorpy.Checker("hard", type_="radio")
box = thorpy.Box(elements=[slider, line, checker_radio])
menu = thorpy.Menu(box)
# Sharang: trying out thorpy for GUI element addition. Above is a test slider and below is initialising it, go to thorpy documentation to understand better
for element in menu.get_population():
    element.surface = screen
box.set_topleft((100, 100))
box.blit()
box.update()

crash_sound = pygame.mixer.Sound('./sound/crash.wav')


def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, x, y, color=black):
    large_text = pygame.font.SysFont('comicsansms', 50)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    # pygame.display.update() #solved for blink bug on the front page


def button(msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            if parameter != None:
                action(parameter)
            else:
                action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    smallText = pygame.font.SysFont('comicsansms', 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect)


def quitgame():
    pygame.quit()
    quit()


def crash():
    pygame.mixer.Sound.play(crash_sound)
    message_display('crashed', game.settings.width / 2 * 15,
                    game.settings.height / 3 * 15, white)
    time.sleep(1)


def initial_interface():
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            menu.react(event)  # S: thorpy ui code?

        screen.blit(background, (0, 0))
        message_display('Gluttonous', game.settings.width / 2 *
                        15, game.settings.height / 4 * 15)  # blink bug

        button('Go!', 80, 240, 80, 40, green, bright_green, game_loop, 'human')
        button('Quit', 270, 240, 80, 40, red, bright_red, quitgame)
        box.set_topleft((game.settings.width / 4 * 15,
                        game.settings.height / 4 * 15))
        box.blit()
        box.update()
        pygame.display.flip()
        pygame.time.Clock().tick(15)


def game_loop(player, fps=10):  # fps start with 10
    game.restart_game()
    speed = fps  # Tien. added a variable for fps to edit the speed,

    while not game.game_end():

        pygame.event.pump()

        move = human_move()

        if(game.do_move(move) == 1):  # Tien. speed increase when the score increases
            # Tien. if statement added, to method "do_move" (whenever it returns to 1(scores)) fps increment by 5
            speed += 0.5

        screen.fill(gamebackground)
        # add game background
        # can be change through gamebackground

        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(white, screen)

        pygame.display.flip()

        fpsClock.tick(speed)  # switch parameter (from (fps) to (speed)

    crash()


def human_move():
    direction = snake.facing

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        elif event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == ord('d'):
                direction = 'right'
            if event.key == K_LEFT or event.key == ord('a'):
                direction = 'left'
            if event.key == K_UP or event.key == ord('w'):
                direction = 'up'
            if event.key == K_DOWN or event.key == ord('s'):
                direction = 'down'
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    move = game.direction_to_int(direction)
    return move


if __name__ == "__main__":
    initial_interface()
