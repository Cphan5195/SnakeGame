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
import pickle #S: added pickle module for high scores
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

#S: Duplicated message_display in order to use a separate function to display the crash score when the player loses
def message_display_crash(text, x, y, color=black):
    large_text = pygame.font.SysFont('comicsansms', 20)#S: Smaller font than the original
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()

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
    screen.blit(background, (0, 0))
    crashscore = str(game.snake_score()) #S: added crashscore to print to player the score they got
    try:
        with open('highscores.dat', 'rb') as file:#S: opens any existing high scores
            highscores = pickle.load(file)
    except:
        highscores = [0] * 3#S: minimum of three scores for the top three to prevent errors in access
    '''
    S: Using the pickle method of storing the high scores as an array, the above code loads the existing high scores unless there are none, in which case the array is turned into zeroes
    '''
    highscores.append(game.snake_score())#S: appends the current score to the list of high scores
    highscores = sorted(highscores, reverse=True)#S: sorts the high scores from highest to lowest
       
    crashstring = 'Crashed: Your score was ' + crashscore #S: added crashstring to print to player with good formatting 
    message_display_crash(crashstring, game.settings.width / 2 * 15, game.settings.height / 3 * 15, white) #S: replaced original string with crashstring, calling the duplicated function
    message_display_crash("TOP THREE BEST SCORES", game.settings.width / 2 * 15, game.settings.height / 3 * 18, white)#S: heading of scoreboard
    firststring = '#1: ' + str(highscores[0]))#S: accessing sorted array to find first place score
    secondstring = '#2: ' + str(highscores[1])#S: accessing sorted array to find second place score
    thirdstring = '#3: ' + str(highscores[2]))#S: accessing sorted array to find third place score
    message_display_crash(firststring, game.settings.width / 2 * 15, game.settings.height / 3 * 21, white)#S: displaying first place score
    message_display_crash(secondstring, game.settings.width / 2 * 15, game.settings.height / 3 * 24, white)#S: displaying second place score
    message_display_crash(thirdstring, game.settings.width / 2 * 15, game.settings.height / 3 * 27, white)#S: displaying third place score
    with open('highscores.dat', 'wb') as file:#S: stores the high score array in the file so that it is stored on disk and not just when the program is executed
        pickle.dump(highscores, file)
    
    time.sleep(5)#S: made the text stay longer on screen


def initial_interface():
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # S: thorpy ui code, which will be used later with variable set by user
            menu.react(event)

        # S: this is the background variable as earlier used, to improve how the screen is displayed
        screen.blit(background, (0, 0))
        message_display('Gluttonous', game.settings.width /
                        2 * 15, game.settings.height / 4 * 15)

        menu.react(event)#S: thorpy ui code, which will be used later with variable set by user
        

        screen.blit(background, (0, 0))#S: this is the background variable as earlier used, to improve how the screen is displayed
        message_display('Gluttonous', game.settings.width / 2 * 15, game.settings.height / 4 * 15)


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
            speed += 0.8

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
