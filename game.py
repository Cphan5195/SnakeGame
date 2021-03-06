# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 15:19:25 2018

@author: zou
"""
'''
S: This is the imported modules, with pygame involving most of the game functions including image loading, screen display, movement.
The random module is used when placing down the strawberries and choosing which graphical representation is displayed, for user freshness.
Numpy module runs mathematical calculations which are used to determine positions of snakes and items.
'''
import pygame
import random
import thorpy  # S: imported thorpy, a graphical module for testing
import numpy as np

#S: This class simply defines the initial size and thus relative size of most of the objects in both scripts.
class Settings:
    def __init__(self):
        self.width = 28
        self.height = 28
        self.rect_len = 15

#S: This class defines everything to do with the snake the player controls.
class Snake:
    '''
S: The below function initialises the snake with images for what the head looks like in all directions 
as well as the tail in all directions, and the body which only has one direction. It starts the snake facing right
and then calls the initialise function.
    '''

    def __init__(self):

        self.image_up = pygame.image.load('images/head_up.bmp')
        self.image_down = pygame.image.load('images/head_down.bmp')
        self.image_left = pygame.image.load('images/head_left.bmp')
        self.image_right = pygame.image.load('images/head_right.bmp')

        self.tail_up = pygame.image.load('images/tail_up.bmp')
        self.tail_down = pygame.image.load('images/tail_down.bmp')
        self.tail_left = pygame.image.load('images/tail_left.bmp')
        self.tail_right = pygame.image.load('images/tail_right.bmp')

        self.image_body = pygame.image.load('images/body.bmp')

        self.facing = "right"
        self.initialize()
        
    '''
    S: This function starts the snake at a fixed coordinate and starts it off with three segments to the left of it
(   including the head as one) and a score of zero
    '''

    def initialize(self):
        self.position = [10, 10]#S: changed from 6 to 10 to make it less punishing on start-up
        self.segments = [[10 - i, 10] for i in range(3)]#S: as above
        self.score = 0

    def blit_body(self, x, y, screen):#S: A simple function that visually displays the body of the snake at a given coordinate
        screen.blit(self.image_body, (x, y))

    def blit_head(self, x, y, screen):#S: A simple function that displays the snake head in the same direction it is facing
        if self.facing == "up":
            screen.blit(self.image_up, (x, y))
        elif self.facing == "down":
            screen.blit(self.image_down, (x, y))
        elif self.facing == "left":
            screen.blit(self.image_left, (x, y))
        else:
            screen.blit(self.image_right, (x, y))

    def blit_tail(self, x, y, screen):#S: A simple function that checks the tail's direction and appropriately displays the tail image
        tail_direction = [self.segments[-2][i] -
                          self.segments[-1][i] for i in range(2)]#S: a mathematical algorithm that will return specific results for the direction of the tail

        if tail_direction == [0, -1]:
            screen.blit(self.tail_up, (x, y))
        elif tail_direction == [0, 1]:
            screen.blit(self.tail_down, (x, y))
        elif tail_direction == [-1, 0]:
            screen.blit(self.tail_left, (x, y))
        else:
            screen.blit(self.tail_right, (x, y))

    def blit(self, rect_len, screen):#S: A function that displays every portion of the snake appropriately
        self.blit_head(self.segments[0][0]*rect_len,#S: displays head
                       self.segments[0][1]*rect_len, screen)
        for position in self.segments[1:-1]:#S:ensuring the body does not overlap onto the head or tail displaying
            self.blit_body(position[0]*rect_len, position[1]*rect_len, screen)
        self.blit_tail(self.segments[-1][0]*rect_len,#S: displays tail
                       self.segments[-1][1]*rect_len, screen)

    def update(self):#S: A function that moves the snake in the direction it is facing
        if self.facing == 'right':
            self.position[0] += 1
        if self.facing == 'left':
            self.position[0] -= 1
        if self.facing == 'up':
            self.position[1] -= 1
        if self.facing == 'down':
            self.position[1] += 1
        self.segments.insert(0, list(self.position))#S: moves the position of the segments accordingly with the snake's movement

#S: Below is a class containing the data of the fruit (strawberry) that gives the player points.
class Strawberry():
#S: Below is the initialisation of the fruit, which includes the settings for size, style (which decides the image), and starts the first fruit
    def __init__(self, settings):
        self.settings = settings

        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load(
            'images/food' + str(self.style) + '.bmp')
        self.initialize()

    def random_pos(self, snake):#S: This function gives a random fruit image to the fruit and finds a random coordinate within the boundary 
    #that is not within the snake already, and places the fruit there.
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load(
            'images/food' + str(self.style) + '.bmp')  # edit food photo

        self.position[0] = random.randint(0, self.settings.width-1)
        self.position[1] = random.randint(0, self.settings.height-1)

        self.position[0] = random.randint(9, 19)
        self.position[1] = random.randint(9, 19)

        if self.position in snake.segments:
            self.random_pos(snake)

    def blit(self, screen):
        screen.blit(
            self.image, [p * self.settings.rect_len for p in self.position])#S: A simple function that displays the fruit image

    def initialize(self):#S: starts the first fruit at the same place
        self.position = [15, 10]

#S: A major function that defines the elements of the game and is commonly called in the main function.
class Game:
    """
    S: The game initialises with the settings as initially described, a snake as seen by the snake class, a strawberry with the same settings
    as initially described, and a dictionary variable that transforms the key input into relevant input for determining the directions and moves of the snake.
    """
    def __init__(self):
        self.settings = Settings()
        self.snake = Snake()
        self.strawberry = Strawberry(self.settings)
        self.move_dict = {0: 'up',
                          1: 'down',
                          2: 'left',
                          3: 'right'}

    def restart_game(self):#S: A function to restart the snake and the strawberry completely.
        self.snake.initialize()
        self.strawberry.initialize()
    
    def current_state(self):#S: A function which returns an array that corresponds to the positions of the snake and the strawberries.
    #S: Removing this function has no effect on the game, but there was also no opportunity to implement something with this function, so it has no actual utility.
        state = np.zeros((self.settings.width+2, self.settings.height+2, 2))
        expand = [[0, 1], [0, -1], [-1, 0], [1, 0],
                  [0, 2], [0, -2], [-2, 0], [2, 0]]

        for position in self.snake.segments:
            state[position[1], position[0], 0] = 1

        state[:, :, 1] = -0.5

        state[self.strawberry.position[1],
              self.strawberry.position[0], 1] = 0.5
        for d in expand:
            state[self.strawberry.position[1]+d[0],
                  self.strawberry.position[0]+d[1], 1] = 0.5
        return state

    def direction_to_int(self, direction):#S: A function called in main's human_move() that converts player input into readable input for the dict containing directions
        direction_dict = {value: key for key, value in self.move_dict.items()}
        return direction_dict[direction]

    '''
    S: The below fuction takes the current direction and gets the input direction, and if the direction is possible 
    i.e. if it is a 90 degree turn and not an 180 degree turn, the new direction is the current direction and the snake is updated.
    This function also checks if there is a fruit in the snake's body (inc. head) and adds to the score if so, returning a value 
    that reflects whether there was a fruit eaten or not.
    The function also returns differently if the game has ended via the game end function.    
    '''
    def do_move(self, move):
        move_dict = self.move_dict

        change_direction = move_dict[move]

        if change_direction == 'right' and not self.snake.facing == 'left':
            self.snake.facing = change_direction
        if change_direction == 'left' and not self.snake.facing == 'right':
            self.snake.facing = change_direction
        if change_direction == 'up' and not self.snake.facing == 'down':
            self.snake.facing = change_direction
        if change_direction == 'down' and not self.snake.facing == 'up':
            self.snake.facing = change_direction

        self.snake.update()

        if self.snake.position == self.strawberry.position:
            self.strawberry.random_pos(self.snake)
            reward = 1
            self.snake.score += 1

        else:
            self.snake.segments.pop()
            reward = 0

        if self.game_end():
            return -1

        return reward

    def game_end(self):#S: A simple 'death' function that returns true if the snake has crashed on any wall or any portion of its own body 
        end = False
        if self.snake.position[0] >= self.settings.width or self.snake.position[0] < 0:
            end = True
        if self.snake.position[1] >= self.settings.height or self.snake.position[1] < 0:
            end = True
        if self.snake.segments[0] in self.snake.segments[1:]:
            end = True

        return end

    def blit_score(self, color, screen):#S: A simple function to display the current score of the user.
        font = pygame.font.SysFont(None, 25)
        text = font.render('Score: ' + str(self.snake.score), True, color)
        screen.blit(text, (0, 0))

    def snake_score(self):  # S: Added a function that should return the current snake score as a safe way of doing so.
        return self.snake.score
