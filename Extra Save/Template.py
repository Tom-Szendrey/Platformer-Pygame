'''
First save
Just the template/basics that are required
with comments

2016/04/14
'''

import pygame #duh
import random #this is letting us use random stuff 
#if i did import settings, id need to do things like settings.FPS
#so instead we use
from Settings import *


'''
initalizes shit
'''
pygame.init() #initalizes pygame
pygame.mixer.init() #this initalizes sounds
screen = pygame.display.set_mode((width,height)) #makes the screen
pygame.display.set_caption(title)
clock = pygame.time.Clock() #starts the clock

'''
Game Loop
'''
running = True
while running:
    '''
    keep this loop running at the right speed
    '''
    clock.tick(FPS)
    
    '''
    process input (events)
    '''
    
    #this has to be constantly running, if a user clicks something
    #during the update, that something still has to be recorded as an input
    for event in pygame.event.get():
        #check if user wants to close window
        if event.type == pygame.QUIT:
            running = False
            

    
    '''
    update
    '''
    
    '''
    draw/render
    '''
    screen.fill([20,134,107])
    #after drawing everything flip
    pygame.display.flip() #think double buffering. The back side is ready, the front is now being replaced
    
pygame.quit() #closes everything
