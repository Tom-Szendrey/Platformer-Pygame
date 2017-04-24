'''
Settings
'''
import os
import pygame as pg

game_folder = os.path.dirname(__file__)
image_folder = os.path.join(game_folder,"images")


#Window settings
width = 600#480
height = 480#600
FPS = 60
title = "Tom's Pygame"

#player properties
player_acc = 0.25
player_friction = -0.16 #-0.12
player_jump = -12
walkingSpeed = 175
swordSwingSpeed = 140
#ammoCount = 2

#player properties in the air
air_acc = 0.6
air_friction = -0.09
sprintAcc = 0.6

#colours
black = [0,0,0]
white = [255,255,255]
red = [255,0,0]
blue = [0,0,255]
green = [0,255,0]
yellow = [255,255,0]
teal = [10,210,255]
grey = [128,128,128]

#background image
background = pg.image.load(os.path.join(image_folder,'Background.png'))
startScreen = pg.image.load(os.path.join(image_folder,'Start Screen.png'))
endScreen =  pg.image.load(os.path.join(image_folder,'Start Screen.png'))
optionsScreen = pg.image.load(os.path.join(image_folder,'Options Screen.png'))
#background = pg.transform.scale(background,(width,height))

#clocks
clock = pg.time.Clock() #starts the clock
timer = str(pg.time.get_ticks()/1000)

currentLevel = 0
#platforms
levelsList = [[ "                                                      ",
                "L     B                                            E   R",
                "L                                                      R",
                "L                                                T     R",
                "L t                                     PPPPPPPPPP     R",
                "LPPP                        H                          R",
                "L                      PPPPPPPPPPPPP                   R",
                "L                PP                                    R",
                "L  PPPPPPPPPPP     P                 T                 R",
                "L    K               P         PPPPPPPPPPP             R",
                "L                      PP                              R",
                "L                      RL                          D   R",
                "L                      RL                        T     R",
                "LPPPPPPPPP   PPPPPPPPPPPPPP P P    PPPPPPPPPPPPPPPPPPPPR",
                "                                                        ",
                "                                                        ",
                "                                                        ",
                "                                                        ",
                "                                                        ",
                "                          G                             "],

            [ "                                                      ",
                "L     B                                            E   R",
                "L                                                      R",
                "L                                                T     R",
                "L                                       PPPPPPPPPP     R",
                "L                                                      R",
                "L                                                      R",
                "L                      PP                              R",
                "L                      RL             T                R",
                "L      K               RL        PPPPPPPPPPP           R",
                "L     PPPPPPPPPPPPP    RL                              R",
                "Lt                     RL                          D   R",
                "L                      RL                    T         R",
                "LPPPPPPPPPPPPPPPPPPPPPPPPPPPPP   P PPPPPPPPPPPPPPPPPPPPR",
                "                                                        ",
                "                                                        ",
                "                                                        ",
                "                                                        ",
                "                                                        ",
                "                          G                             "],
            

            ]










