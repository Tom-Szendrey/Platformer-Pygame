'''
Contains the sprites for Tom's pygame

I should make all sprities have a parent abstract class which contains
animation(self,amountOfFrames)

To fix bullet problem:
Solution 1) Create a textfile containing numbers, which are
bullet count, magic count, life left, ect. When you go to next level
and you make a new Player Instance, instead of making it default to 2 ect ect
you could make it read the file. Then at the end of the level, open the file,
update the data.
To reset to default at the start of the game, just simply rewrite the textfile on
the tutorial.
Cons: Reading and writing files may take a little bit of time, so it might increase
the loading time between rounds.

'''
import pygame as pg
import os
import random
from Settings import *

game_folder = os.path.dirname(__file__)

class Player(pg.sprite.Sprite):
    def __init__(self,playerX,playerY):
        pg.init()
        pg.sprite.Sprite.__init__(self)

        #for ammo, and later add stance
        self.ammoCount = 20
        self.lastShot = 0
        self.stance = 'Slashing'

        #for frames
        self.walking = False
        self.jumping = False
        #self.repelled = False #this is when you are repelled off of a plat from hitting it from below
        self.shooting = False
        self.slashing = False

        self.currentFrame = 0
        self.lastUpdated = 0
        self.shootingUpdated = 0
        self.slashingUpdate = 0

        #image stuff
        self.player_images()
        self.image = self.walking_r[0]
        self.rect = self.image.get_rect()

        self.grounded = True

        #positioning stuff
        #puts the center of the rect in the center of the screen
        self.rect.midbottom = (width/2,height/2)
        #initalizes the position,veleocity, and acceleration vectors
        self.pos = [playerX,playerY]
        self.vel = [0,0]
        self.acc = [0,0]

        self.height = 60
        self.facing = 'Right' #default to facing right.

    def player_images(self):
        self.walking_r = [pg.image.load(os.path.join(image_folder, 'Player Right_1.png')),
                          pg.image.load(os.path.join(image_folder, 'Player Right_2.png')),
                          pg.image.load(os.path.join(image_folder, 'Player Right_3.png'))]

        self.walking_l = [pg.image.load(os.path.join(image_folder, 'Player Left_1.png')),
                          pg.image.load(os.path.join(image_folder, 'Player Left_2.png')),
                          pg.image.load(os.path.join(image_folder, 'Player Left_3.png'))]

        self.shooting_l = pg.image.load(os.path.join(image_folder, 'Player Left Shooting.png'))
        self.shooting_r = pg.image.load(os.path.join(image_folder, 'Player right Shooting.png'))

        #the reason for the repeates for the last image is because i didnt know how to tell
        #the game to wait 140 miliseconds before turning slashing off... When i figure it out
        #i will improve this solution
        self.slashing_l = [pg.image.load(os.path.join(image_folder, 'player left slashing 1.png')),
                           pg.image.load(os.path.join(image_folder, 'player left slashing 2.png')),
                           pg.image.load(os.path.join(image_folder, 'player left slashing 3.png')),
                           pg.image.load(os.path.join(image_folder, 'player left slashing 3.png'))]

        self.slashing_r = [pg.image.load(os.path.join(image_folder, 'player right slashing 1.png')),
                           pg.image.load(os.path.join(image_folder, 'player right slashing 2.png')),
                           pg.image.load(os.path.join(image_folder, 'player right slashing 3.png')),
                           pg.image.load(os.path.join(image_folder, 'player right slashing 3.png'))]

    def player_animation(self):
        now = pg.time.get_ticks()

        if self.slashing:
            if now - self.slashingUpdate > swordSwingSpeed: #how fast to switch frames
                self.slashingUpdate = now
                self.currentFrame = (self.currentFrame + 1) % len(self.slashing_r)
                if self.facing == 'Right':
                    self.image  = self.slashing_r[self.currentFrame]
                if self.facing == 'Left':
                    self.image = self.slashing_l[self.currentFrame]
                if self.currentFrame == len(self.slashing_r) - 1:
                    self.slashing = False

        elif not self.walking and not self.jumping and not self.shooting:
            if self.facing == 'Right':
                self.image = self.walking_r[0]
            if self.facing == 'Left':
                self.image = self.walking_l[0]

        elif self.walking:
            if now - self.lastUpdated > walkingSpeed: #175: #how fast to switch frames
                self.lastUpdated = now
                self.currentFrame = (self.currentFrame + 1) % len(self.walking_r)
                if self.facing == 'Right':
                    self.image  = self.walking_r[self.currentFrame]
                if self.facing == 'Left':
                    self.image = self.walking_l[self.currentFrame]

        if self.shooting:
            if self.facing == 'Right':
                self.image = self.shooting_r
            if self.facing == 'Left':
                self.image = self.shooting_l
            if now - self.shootingUpdated > 750:
                self.currentFrame = 0
                self.shootingUpdated = now
                self.shooting = False

    def playerMovement(self):
        if self.grounded == False:
            #starts with 0 acceleration in x, and 0.5 downwards
            self.acc = [0,0.5]

        keys = pg.key.get_pressed()

        #player controls
        ###################################################################################################

        #left
        if keys[pg.K_a] and self.grounded:
            self.facing = 'Left'
            self.acc[0] = -player_acc
            #self.acc[1] = 0

        #right
        if keys[pg.K_d] and self.grounded:
            self.facing = 'Right'

            self.acc[0]  = player_acc
            #self.acc[1] =0

        #youre in the air
        if keys[pg.K_a] and self.grounded == False:
            self.facing =  'Left'
            self.acc[0] = -air_acc

        if keys[pg.K_d] and self.grounded == False:
            self.facing = 'Right'
            self.acc[0]  = air_acc

        #jumping
        if keys[pg.K_SPACE] and self.grounded:
            self.vel[1] = player_jump

        #sprinting
        if keys[pg.K_KP8] and self.grounded:
            if keys[pg.K_d]:
                self.acc[0] = sprintAcc
            if keys[pg.K_a]:
                self.acc[0] = -sprintAcc



        #setting self.walking and self.jumping
        if self.vel[0] > 0.8 or self.vel[0] < -0.8:
            #moving fwd, and up/down
            if self.vel[1] > 0.8 or self.vel[1] < -0.8:
                self.jumping = True
            #moving fwd and not up/down
            else:
                self.walking = True
                self.jumping = False

        #not moving fwd
        else:
            if self.vel[1] > 0.8 or self.vel[1] < -0.8:
                self.jumping = True
            else:
                self.jumping = False

            self.walking = False

    def update(self):
        self.playerMovement()
        self.player_animation()

        self.rect = self.image.get_rect() #redefines the players rect as the images change sizes

        #facing images
        ###################################################################################################
        timer = str(pg.time.get_ticks()/1000)

        #physics
        ####################################################################################################
        #if on the ground, calculate the effects of friction
        if self.grounded:
            #applies friction
            self.acc[0] += self.vel[0] * player_friction
            #equations of motion
            self.vel[0] += self.acc[0]
            self.pos[0] += 0.5 * self.acc[0] + self.vel[0]

        #Air pysics
        if self.grounded == False:
            self.vel[1] += self.acc[1]
            self.pos[1] += 0.5 * self.acc[1] + self.vel[1]

            self.acc[0] += self.vel[0] * air_friction
            self.vel[0] += self.acc[0]
            self.pos[0] += 0.5 * self.acc[0] + self.vel[0]


        self.rect.midbottom = self.pos #The position that matters is the center bottom.



'''
Not sure if i need this class anymore
because ive changed the images to be boxes
I just need to work on taking out the use
of this and redefining the player collision box
in the player class
'''
class PlayerCollision(pg.sprite.Sprite):
    def __init__(self,x,y,facing):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pg.Surface((19,54))
        self.image.fill((red))
        self.rect = self.image.get_rect()
        if facing == 'Right':
            self.rect.x = self.x - 16
            self.rect.y = self.y - 54
        if facing == 'Left':
            self.rect.x = self.x - 3
            self.rect.y = self.y - 54


class Platform(pg.sprite.Sprite):
    #takes platforms x, y cord, then width, height
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(os.path.join(image_folder,'Basic Platforms.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self,playery):
        #print 'here'
        if playery < self.rect.y:
            return(True)
        else:
            return(False)
        
        

class Wall(pg.sprite.Sprite):
    #for Walls
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(os.path.join(image_folder,'Basic Platforms R.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



class Bullets(pg.sprite.Sprite):
    def __init__(self,x,y,direction,typeOfBullet):
        pg.sprite.Sprite.__init__(self)
        self.typeOfBullet = typeOfBullet
        self.direction = direction

        if self.typeOfBullet == 'Player' and self.direction == 'Right':
            self.image = pg.image.load(os.path.join(image_folder,'BulletRight.png'))

        if self.typeOfBullet == 'Player' and self.direction == 'Left':
            self.image = pg.image.load(os.path.join(image_folder, 'BulletLeft.png'))

        if self.typeOfBullet == 'Turret' and self.direction == 'Left':
            self.image = pg.image.load(os.path.join(image_folder,'turret bullet left.png'))

        if self.typeOfBullet == 'Turret' and self.direction == 'Right':
            self.image = pg.image.load(os.path.join(image_folder,'turret bullet right.png'))

        self.rect = self.image.get_rect()
        self.rect.y = y - 30 #gun height

        if self.direction == "Left":
            self.rect.x = x - 50 #these -40 and + 20 need to be edited

        if self.direction == "Right":
           self.rect.x = x + 30

        self.vel = [0,0]

    def update(self):
        self.rect.x += self.vel[0]
        if self.direction == 'Left' and self.typeOfBullet == 'Player':
            self.vel[0] = -7

        if self.direction == 'Right' and self.typeOfBullet == 'Player':
            self.vel[0] = 7

        if self.direction == 'Left' and self.typeOfBullet == 'Turret':
            self.vel[0] = -5

        if self.direction == 'Right' and self.typeOfBullet == 'Turret':
            self.vel[0] = 5

        #kill the bullets as they leave the screen (to not keep track useless data)
        if self.rect.x < -20:
            self.kill()

        if self.rect.x > width + 20:
            self.kill()

#also give __init__ the type of mob, and player x and player y, update will also need
#player x and y
class Mobs(pg.sprite.Sprite):
    def __init__(self, x, y, playerX, playerY, typeOfMob,facing):
        pg.sprite.Sprite.__init__(self)
        self.facing = facing
        self.x = x
        self.y = y
        self.mobFrame = 0

        self.temp = False #this is used to create bullets for the turrets and other mobs, rename?
        self.lastShot = 0
    
        self.playerX = playerX
        self.playerY = playerY
        self.mobType = typeOfMob

        if typeOfMob == 'Turret':
            self.turretInit(x,y)
            
        if typeOfMob == 'humanoid':
            self.humanoidInit(x,y)
        

    def update(self,playerX,playerY,alive):
        if alive == False:
            self.kill()


        if self.mobType == 'Turret':
            self.turretUpdate()

    def turretInit(self,x,y):
        
        self.lastUpdated = pg.time.get_ticks()
        
        if self.facing == 'Left':
            self.turretImages_l = [pg.image.load(os.path.join(image_folder, 'Turret Left_1.png')),
                                    pg.image.load(os.path.join(image_folder, 'Turret Left_2.png')),
                                    pg.image.load(os.path.join(image_folder, 'Turret Left_3.png'))]
            self.image = self.turretImages_l[0]
            
        if self.facing == 'Right':
            self.turretImages_r = [pg.image.load(os.path.join(image_folder, 'Turret Right_1.png')),
                              pg.image.load(os.path.join(image_folder, 'Turret Right_2.png')),
                              pg.image.load(os.path.join(image_folder, 'Turret Right_3.png'))]
            self.image = self.turretImages_r[0]
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def turretUpdate(self):
        self.now = pg.time.get_ticks()

        if self.now - self.lastShot > 1000 and self.facing == 'Left':
            self.temp = Bullets(self.rect.left + 30,self.rect.y + 40,'Left','Turret')
            self.lastShot = self.now
            
        if self.now - self.lastShot > 1000 and self.facing == 'Right':
            self.temp = Bullets(self.rect.right - 30,self.rect.y + 40,'Right','Turret')
            self.lastShot = self.now
            
        if self.now - self.lastUpdated > 1000/3 and self.facing == 'Left':
            self.lastUpdated = self.now
            self.image = self.turretImages_l[self.mobFrame]
            self.mobFrame = (self.mobFrame + 1) % (3)

        if self.now - self.lastUpdated > 1000/3 and self.facing == 'Right':
            self.lastUpdated = self.now
            self.image = self.turretImages_r[self.mobFrame]
            self.mobFrame  = (self.mobFrame + 1) % (3)



    def humanoidInit(self,x,y):        
        if self.facing == 'Left':
            self.turretImages_l = [pg.image.load(os.path.join(image_folder, 'redbox.png')),
                                    pg.image.load(os.path.join(image_folder, 'redbox.png')),
                                    pg.image.load(os.path.join(image_folder, 'redbox.png'))]
            self.image = self.turretImages_l[0]
            
        if self.facing == 'Right':
            self.turretImages_r = [pg.image.load(os.path.join(image_folder, 'redbox.png')),
                              pg.image.load(os.path.join(image_folder, 'redbox.png')),
                              pg.image.load(os.path.join(image_folder, 'redbox.png'))]
            self.image = self.turretImages_r[0]
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    '''
    I think i just want it to walk from the end of the platform its on until the other end
    so i want it to turn around when it starts falling from leaving the platform
    or i want it to turn when it hits a walls
    '''
    def humanoidUpdate(self):
        pass


        
class Sword(pg.sprite.Sprite):
    def __init__(self, playerX, playerY, facing):
        pg.sprite.Sprite.__init__(self)
        self.now = pg.time.get_ticks()
        self.playerX = playerX
        self.playerY = playerY

        self.image = pg.Surface((27,52))
        self.image.fill((yellow))
        self.rect = self.image.get_rect()
        if facing == 'Right':
            self.rect.x = self.playerX - 11
            self.rect.y = self.playerY - 60
        if facing == 'Left':
            self.rect.x = self.playerX - 15
            self.rect.y = self.playerY - 60


    def update(self,playerx,playery,facing):
        self.lastUpdated = pg.time.get_ticks()
        if self.lastUpdated - self.now > (swordSwingSpeed * 3):
            self.kill()
        
        if facing == 'Right':
            if self.lastUpdated - self.now > swordSwingSpeed:
                self.image = pg.Surface((38,26))
                self.rect = self.image.get_rect()
                self.rect.x = playerx - 11
                self.rect.y = playery - 50
            if self.lastUpdated - self.now > swordSwingSpeed * 2:
                self.image = pg.Surface((37,50))
                self.rect = self.image.get_rect()
                self.rect.x = playerx - 11
                self.rect.y = playery - 60

        if facing == 'Left':
            if self.lastUpdated - self.now > swordSwingSpeed:
                self.image = pg.Surface((38,26))
                self.rect = self.image.get_rect()
                self.rect.x = playerx - 25
                self.rect.y = playery - 50
            if self.lastUpdated - self.now > swordSwingSpeed * 2:
                self.image = pg.Surface((37,50))
                self.rect = self.image.get_rect()
                self.rect.x = playerx - 25
                self.rect.y = playery - 60

            #self.rect.x = playerx - 25
            #self.rect.y = playery - 60


class Dropped_Ammo(pg.sprite.Sprite):
    def __init__(self,x,y,alive):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(image_folder,'Dropped Ammo.png'))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if alive == False:
            #add ammo to player, kill the sprite
            self.kill()




'''
Takes name of 1st image,
name of 2nd image
x location
y location

gives you a button there where the 1st image is the default,
and the 2nd is the hovering image.
'''
class Button(pg.sprite.Sprite):
    def __init__(self,orgImage,hoverImage,x,y,screen):
        pg.sprite.Sprite.__init__(self)
        self.pressed = False
        self.hover = False
        #self.screen = screen
        self.orgImage = orgImage
        self.hoverImage = hoverImage
        self.image = pg.image.load(os.path.join(image_folder,self.orgImage))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self,mousePos,mouseClick):
        if self.rect.left < mousePos[0] < self.rect.right and self.rect.top < mousePos[1] < self.rect.bottom: #assume for now the size of rect is 100
            self.image = pg.image.load(os.path.join(image_folder,self.hoverImage))
            self.hover = True
        else:
            self.image = pg.image.load(os.path.join(image_folder,self.orgImage))

        if self.hover and mouseClick == (1,0,0):
            self.pressed = True


'''
Used for the ending level door
'''
class Door(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(image_folder,'door.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y





