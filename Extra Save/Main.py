'''
Tom Szendrey
2016/09/18

Game

*********************************************************
Next steps:

for tutorial:
-You always reset to 2 ammo right now and i dont think i want that.
-Think about adding a sprinting feature
-add magic features

to finish everything
-create more levels + mobs + level backgrounds, platform drawings, ect
-finish end screen, draw start screen, make options screen
-add sounds.
-look to make shit more effiecent.


Thinking of making a group called things or something like that
and just use that to scroll everything, because currently scrolling function is a lot messy

Solved, but keep tabs on how it was done:
Falling on Platforms Problem:
To solve the platform problem, you could make a new spritegroup that
updates every update, and only contains the platforms that are below the player's bottom rect
and then use that grp instead of using all the platforms
to do this though youd need to check all the platform's rect.y every single update
which doesnt sound efficent.


Other weird things:
do i make player class take the ammo count, or should i just make it a global var in settings?

***********************************************************
'''
import pygame as pg
import random
import os #this is so if you change operating systems, the file directry still works
from Settings import *
from Sprites import *



class Game:
    #initalizes window, ect
    def __init__(self):
        pg.init() #initalizes pygame
        pg.mixer.init() #this initalizes sounds
        pg.font.init()

        self.screen = pg.display.set_mode((width,height)) #makes the screen
        pg.display.set_caption(title)

        self.backgroundX = 0
        self.backgroundY = 0

        self.running = True

    #creating sprite groups
    #creating all the spawn loctions, and reading the map
    def new(self,platformList):
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.rightWalls = pg.sprite.Group()
        self.leftWalls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mob_group = pg.sprite.Group()
        self.ammo_group = pg.sprite.Group()
        self.sword = pg.sprite.Group()
        self.button_group = pg.sprite.Group()

        self.droppedAmmo = []
        
        self.mob = [0]
        self.all_platforms = []
        
        '''
        the player's position must be define before you can place
        turrets down, so this is loop is the same as the one after it
        but done first and seperately for this reason.
        '''
        x = 0
        y = 0
        for row in platformList:
            for col in row:
                if col == 'K':
                    self.player = Player(x,y)
                    self.all_sprites.add(self.player)

                x += 34
            x = 0
            y += 34



        x = 0
        y = 0
        for row in platformList:
            for col in row:
                if col == 'P':
                    temp = Platform(x,y)
                    self.all_platforms.append(temp)
                    self.all_sprites.add(temp)
                    self.platforms.add(temp)

                if col == 'B':
                    self.left_rect = Platform(x,y)
                    #self.all_sprites.add(self.left_rect)

                if col == 'E':
                    self.right_rect = Platform(x,y)
                    #self.all_sprites.add(self.right_rect)

                if col == 'R':
                    temp = Wall(x,y)
                    self.all_sprites.add(temp)
                    self.rightWalls.add(temp)

                if col == 'L':
                    temp = Wall(x,y)
                    self.all_sprites.add(temp)
                    self.leftWalls.add(temp)

                if col == 'G':
                    self.lowestPoint = Platform(x,y)
                    self.platforms.add(self.lowestPoint) #so i dont need to go to screenMovement and add another 2 lines

                if col == 't':
                    self.mob[len(self.mob)-1] = Mobs(x,y, self.player.pos[0],self.player.pos[1], 'Turret', 'Right')
                    self.all_sprites.add(self.mob[len(self.mob)-1])
                    self.mob_group.add(self.mob[len(self.mob)-1])
                    self.mob.append(0)
                
                if col == 'T':
                    self.mob[len(self.mob)-1] = Mobs(x,y,self.player.pos[0],self.player.pos[1],'Turret','Left')
                    self.all_sprites.add(self.mob[len(self.mob)-1])
                    self.mob_group.add(self.mob[len(self.mob)-1])
                    self.mob.append(0)

                if col == 'D':
                    self.door = Door(x,y)
                    self.all_sprites.add(self.door)
                    #self.door_group.add(self.door)

                if col == 'H':
                    self.mob[len(self.mob)-1] = Mobs(x,y,self.player.pos[0],self.player.pos[1],'humanoid','Left')
                    self.all_sprites.add(self.mob[len(self.mob)-1])
                    self.mob_group.add(self.mob[len(self.mob)-1])
                    self.mob.append(0)

                if col == 'h':
                    self.mob[len(self.mob)-1] = Mobs(x,y,self.player.pos[0],self.player.pos[1],'humanoid','right')
                    self.all_sprites.add(self.mob[len(self.mob)-1])
                    self.mob_group.add(self.mob[len(self.mob)-1])
                    self.mob.append(0)

                x += 34
            x = 0
            y += 34

        self.mob.remove(0)
        self.scrollingSpeed = 3

        self.run()

    #game loop
    def run(self):
        self.playing = True #set playing to true
        while self.playing:
            clock.tick(FPS) #Set the FPS
            #check events, update, draw.
            self.events()
            self.update()
            self.draw()


    #Game loop - Update
    def update(self):
        self.platformsBelowPlayer = []
        self.platformsAbovePlayer = []
        
        #updating the collision rect for the player
        self.PlayerRect = PlayerCollision(self.player.pos[0],self.player.pos[1],self.player.facing)
        if self.PlayerRect.rect.y > self.lowestPoint.rect.y:
            self.gameInstance = 'End'
            self.showGameOverScreen()

        for plat in self.all_platforms:
            if plat.update(self.player.rect.y + 5): #give it 5 extra pixles for error. 
                self.platformsBelowPlayer.append(plat)
            else: 
                self.platformsAbovePlayer.append(plat)
                
        self.bullets.update()
        self.player.update()
        self.sword.update(self.player.pos[0], self.player.pos[1], self.player.facing)
        #self.button_group.update(self.mousePos) #NOT NEEDED RIGHT NOW

        self.mob_group.update(self.player.pos[0],self.player.pos[1],True)
        for i in range(len(self.mob)):
            if self.mob[i].temp:
                self.all_sprites.add(self.mob[i].temp)
                self.bullets.add(self.mob[i].temp)
        self.screenUpdate()
        self.collisionCheck(currentLevel)

    '''
    follow the character as he leaves the screen
    '''
    def screenUpdate(self):
        #if its inbetween the limits, dont do shit
        if (self.player.pos[0] < width * 6/10 and self.player.pos[0] > width * 4/10):
            pass

        #left
        elif self.player.pos[0] > width * 4/10 and self.player.pos[0] > self.left_rect.rect.x and self.player.pos[0] < self.right_rect.rect.x:
            self.player.pos[0] -= abs((0.5 * (self.player.acc[0] + player_friction + 0.2)) + self.player.vel[0])

            #if self.player.pos[0] > self.left_rect.rect.x:
            self.left_rect.rect.x -= 3
            self.right_rect.rect.x -= 3
            for plat in self.platforms:
                plat.rect.x -= self.scrollingSpeed

            for wall in self.leftWalls:
                wall.rect.x -= self.scrollingSpeed

            for wall in self.rightWalls:
                wall.rect.x -= self.scrollingSpeed

            for mobs in self.mob_group:
                mobs.rect.x -= self.scrollingSpeed

            for bullet in self.bullets:
                bullet.rect.x -= self.scrollingSpeed

            for ammo in self.ammo_group:
                ammo.rect.x -= self.scrollingSpeed

            self.door.rect.x -= self.scrollingSpeed

            self.backgroundX -= self.scrollingSpeed #abs(self.player.vel[0])

        #right
        elif self.player.pos[0] < width * 6/10 and self.player.pos[0] > self.left_rect.rect.x and self.player.pos[0] < self.right_rect.rect.x:
            self.player.pos[0] += abs((0.5 * (self.player.acc[0] + player_friction + 0.2)) + self.player.vel[0])

            #if self.player.pos[0] < self.right_rect.rect.x:
            self.left_rect.rect.x += self.scrollingSpeed
            self.right_rect.rect.x += self.scrollingSpeed
            for plat in self.platforms:
                plat.rect.x += self.scrollingSpeed

            for wall in self.leftWalls:
                wall.rect.x += self.scrollingSpeed

            for wall in self.rightWalls:
                wall.rect.x += self.scrollingSpeed

            for mobs in self.mob_group:
                mobs.rect.x += self.scrollingSpeed

            for bullet in self.bullets:
                bullet.rect.x += self.scrollingSpeed

            for ammo in self.ammo_group:
                ammo.rect.x += self.scrollingSpeed

            self.door.rect.x += self.scrollingSpeed
            
            self.backgroundX += self.scrollingSpeed #abs(self.player.vel[0])

        #follow up and down screen
        if self.player.pos[1] < height * 1/4 and self.player.pos[1] > self.left_rect.rect.y:
            pass
        
        elif self.player.pos[1] < height * 1 / 4 and self.player.pos[1] > self.left_rect.rect.y:
            self.player.pos[1] += abs(self.player.vel[1])
            self.left_rect.rect.y += abs(self.player.vel[1])
            self.right_rect.rect.y += abs(self.player.vel[1])

            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel[1])

            for wall in self.leftWalls:
                wall.rect.y += abs(self.player.vel[1])

            for wall in self.rightWalls:
                wall.rect.y += abs(self.player.vel[1])

            for mobs in self.mob_group:
                mobs.rect.y += abs(self.player.vel[1])

            for bullet in self.bullets:
                bullet.rect.y += abs(self.player.vel[1])

            for ammo in self.ammo_group:
                ammo.rect.y += abs(self.player.vel[1])

            self.door.rect.y += abs(self.player.vel[1])

            self.backgroundY += abs(self.player.vel[1])


        #MAYBE CHANGE THE 2/3 TO 1/2 SO IT FOLLOWS YOU AS YOU FALL
        elif self.player.pos[1] > height * 3/4 and self.player.pos[1] > self.left_rect.rect.y: #only need to use left bc they have same height
            self.player.pos[1] -= abs(self.player.vel[1])
            self.left_rect.rect.y -= abs(self.player.vel[1])
            self.right_rect.rect.y -= abs(self.player.vel[1])

            for plat in self.platforms:
                plat.rect.y -= abs(self.player.vel[1])

            for wall in self.leftWalls:
                wall.rect.y -= abs(self.player.vel[1])

            for wall in self.rightWalls:
                wall.rect.y -= abs(self.player.vel[1])


            for mobs in self.mob_group:
                mobs.rect.y -= abs(self.player.vel[1])

            for bullet in self.bullets:
                bullet.rect.y -= abs(self.player.vel[1])

            for ammo in self.ammo_group:
                ammo.rect.y -= abs(self.player.vel[1])

            self.door.rect.y -= abs(self.player.vel[1])

            self.backgroundY -= abs(self.player.vel[1])


    def collisionCheck(self,currentLevel):

        #player vs platform starts
        if self.player.vel[1] > 0: #falling
            self.contactPlat = pg.sprite.spritecollide(self.PlayerRect,self.platformsBelowPlayer,False)
            if self.contactPlat:
                #if self.player.pos[1] > self.contactPlat[0].rect.top:
                self.player.grounded = True
                #self.player.repelled = False
                self.player.vel[1] = 0
                self.player.pos[1] = self.contactPlat[0].rect.top + 1

        elif -11 < self.player.vel[1] < 0: #jumping
            self.contactPlat = pg.sprite.spritecollide(self.PlayerRect,self.platformsAbovePlayer, False)
            if self.contactPlat:
                #if self.player.pos[1] > self.contactPlat[0].rect.top:
                self.player.grounded = False
                #self.player.repelled = True
                self.player.vel[1] = 0
                self.player.pos[1] = self.contactPlat[0].rect.bottom + 45

        else:
            self.player.grounded = False
            #self.player.repelled = False

        #player vs mob
        self.contactOnMobs = pg.sprite.spritecollide(self.PlayerRect,self.mob_group,False)
        if self.contactOnMobs:
            self.gameInstance = 'End'
            self.showGameOverScreen()
            
        #player vs door start and walls
        self.contactOnDoor = pg.sprite.collide_rect(self.PlayerRect,self.door)
        if self.contactOnDoor:
            currentLevel = currentLevel + 1 
            g = Game()
            g.new(levelsList[currentLevel])
            g.showStartScreen()
        
        self.contactRightWall = pg.sprite.spritecollide(self.PlayerRect,self.rightWalls,False)
        if self.contactRightWall and self.player.vel[0] > 0: #youre touching the right wall, and going right
            self.player.pos[0] = self.contactRightWall[0].rect.left +1

        self.contactLeftWall = pg.sprite.spritecollide(self.PlayerRect,self.leftWalls,False)
        if self.contactLeftWall and self.player.vel[0] < 0: #youre touching the right wall, and going left
            self.player.pos[0] = self.contactLeftWall[0].rect.right +1


        #player vs bullets
        self.bulletToPlayer = pg.sprite.spritecollide(self.player,self.bullets,False)
        if self.bulletToPlayer:
            self.gameInstance = 'End'
            self.showGameOverScreen()

        #kills bullets when they hit walls or platforms
        self.bulletToWalls = pg.sprite.groupcollide(self.bullets,self.leftWalls, True,False)
        self.bulletToWalls = pg.sprite.groupcollide(self.bullets,self.rightWalls,True,False)
        self.bulletToWalls = pg.sprite.groupcollide(self.bullets,self.platforms,True,False)

        #mobs and bullets collision checks
        self.bulletCheck = []
        for i in range(len(self.mob_group)):
            self.bulletCheck.append(0)

        for i in range(len(self.mob_group)):
            self.bulletCheck[i] = pg.sprite.spritecollide(self.mob[i],self.bullets,True)

        #self.bulletCheck[0] = pg.sprite.spritecollide(self.mob1,self.bullets,True)
        for i in range(0,len(self.bulletCheck)) :
            if self.bulletCheck[i]:
                #about dropping ammo
                self.dropChance = random.randint(0,9)
                if self.dropChance < 3: #0,1,2
                    self.droppedAmmo.append(Dropped_Ammo(self.mob[i].rect.x,self.mob[i].rect.y,True))
                    self.all_sprites.add(self.droppedAmmo[-1]) #the most recently added part of the list
                    self.ammo_group.add(self.droppedAmmo[-1])

                #about killing mob
                self.mob[i].update(self.player.pos[0],self.player.pos[1],False)
                self.mob.remove(self.mob[i])

        self.swordCheck = []
        for i in range(len(self.mob_group)):
            self.swordCheck.append(0)

        for i in range(len(self.mob_group)):
            self.swordCheck[i] = pg.sprite.spritecollide(self.mob[i], self.sword,True)

        for i in range(len(self.mob_group)):
            if self.swordCheck[i]:
                #about dropping ammo
                self.dropChance = random.randint(0,9)
                if self.dropChance < 3: #0,1,2
                    self.droppedAmmo.append(Dropped_Ammo(self.mob[i].rect.x,self.mob[i].rect.y,True))
                    self.all_sprites.add(self.droppedAmmo[-1]) #the most recently added part of the list
                    self.ammo_group.add(self.droppedAmmo[-1])

                self.mob[i].update(self.player.pos[0],self.player.pos[1],False)
                self.mob.remove(self.mob[i])

        self.playerToAmmo = []
        for i in range(len(self.ammo_group)):
            self.playerToAmmo.append(0)

        for i in range(len(self.ammo_group)):
            self.playerToAmmo[i] = pg.sprite.spritecollide(self.player, self.ammo_group,True)

        for i in range(len(self.playerToAmmo)):
            if self.playerToAmmo[i]:
                self.amountOfAmmo = random.randint(1,2)
                self.player.ammoCount += self.amountOfAmmo
        
    #Game loop - Events
    def events(self):
        now = pg.time.get_ticks()
        self.mousePos = pg.mouse.get_pos()
        for event in pg.event.get():
        #check if user wants to close window
            if event.type == pg.QUIT:
                #if playing is true, set it to false close the game)
                if self.playing:
                    pg.quit()
                    quit()
                #set running to false, meaning tell it to stop reading code.
                self.running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_KP4:
                    #shooting
                    if now - self.player.lastShot > 300 and self.player.ammoCount > 0 and self.player.stance == 'Shooting':
                        self.player.lastShot = now
                        self.player.ammoCount -= 1

                        self.player.shooting = True
                        temp = Bullets(self.player.pos[0],self.player.pos[1],self.player.facing, 'Player')
                        self.all_sprites.add(temp)
                        self.bullets.add(temp)

                    #slashing
                    if now - self.player.lastShot > 500 and self.player.stance == 'Slashing':
                        self.player.lastShot = now

                        self.player.currentFrame = 0 #reset the walking frame to 0, which allows you to use it for slashing
                        self.player.slashing = True

                        self.swordTEMP = Sword(self.player.pos[0], self.player.pos[1], self.player.facing)
                        self.sword.add(self.swordTEMP)

                #maybe instead of doing the 2 if statements you could use + 1 % len(the list)
                if event.key == pg.K_KP5:
                    if self.player.stance == 'Shooting':
                        self.player.stance = 'Slashing'

                    elif self.player.stance == 'Slashing':
                        self.player.stance = 'Shooting'                

    #Game loop - Draw
    def draw(self):
        self.screen.blit(background,(self.backgroundX,self.backgroundY))
        self.all_sprites.draw(self.screen)

        #drawing the hitbox of the player just to see how it fits on him
        #self.screen.blit(self.PlayerRect.image, (self.player.pos[0] - 16, self.player.pos[1] - 64))
        #self.screen.blit(self.PlayerRect.image, (self.player.pos[0] - 3, self.player.pos[1] - 54))
                
        #if self.sword:
        #    self.screen.blit(self.swordTEMP.image,(self.swordTEMP.rect.x,self.swordTEMP.rect.y))
        
        self.ammoBackground = pg.Surface((70,25))
        self.ammoBackground.fill((white)) #replace this w maybe a drawn image or something
        self.rect = self.ammoBackground.get_rect()
        self.screen.blit(self.ammoBackground, (width - 80, height - 30))

        #timer
        timer = str(pg.time.get_ticks()/1000)
        timeFont = pg.font.SysFont("monospace", 15)
        time_text = timeFont.render(timer, 1, (0,0,0))
        self.screen.blit(time_text, (width-30,0))

        ammoFont = pg.font.SysFont('Arial',17,True)
        self.screen.blit(ammoFont.render('Ammo: ',1,(0,0,0)), (width - 80,height - 30))
        self.screen.blit(ammoFont.render(str(self.player.ammoCount),1,(0,0,0)), (width - 30,height - 30))

        if self.player.stance == 'Slashing':
            self.screen.blit(pg.image.load(os.path.join(image_folder,'sword icon.png')),(width - 90, height - 30))

        if self.player.stance == 'Shooting':
            self.screen.blit(pg.image.load(os.path.join(image_folder,'gun icon.png')),(width - 90, height - 30))

        #after drawing everything flip
        pg.display.flip()



#during these two functions you need to check for closing game, and for
#the user pressing the start, or restart button.

    #The starting screen
    '''
    soooo im kinda making a game loop inside of showStartScreen, and i have already made a game loop for
    the game itself, so why not use some portions of my game's gameloop instead of remaking it?
    '''
    def showStartScreen(self):
        self.gameInstance = 'Start'

        self.startButton = Button('startButton1.png','startButton2.png',width/2,2*height/3,self.screen)
        self.optionsButton = Button('optionsButton1.png','optionsButton2.png',width/2, height/3, self.screen)                    
        self.screen.blit(startScreen,(0,0))

        while self.startButton.pressed == False and self.running: # the exit button is clicked, bc thats still important.            
            #events section
            for event in pg.event.get():
                #check if user wants to close window
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.startButton.pressed = True

            if self.optionsButton.pressed:
                self.showOptionsScreen()
                
            self.startButton.update(pg.mouse.get_pos(),pg.mouse.get_pressed())
            self.optionsButton.update(pg.mouse.get_pos(),pg.mouse.get_pressed())
            self.screen.blit(self.startButton.image,(self.startButton.rect.x,self.startButton.rect.y))
            self.screen.blit(self.optionsButton.image,(self.optionsButton.rect.x,self.optionsButton.rect.y))
            pg.display.flip()
        #self.screen.blit(pg.image.load(os.path.join(image_folder,'gun icon.png')),(width - 90, height - 30))
        #pg.display.flip()



    #the Endind game screen
    def showGameOverScreen(self):
        self.screen.blit(endScreen,(0,0))
        self.endButton = Button('startButton1.png','startButton2.png',width/2,2*height/3,self.screen)

        while self.gameInstance == 'End':
            for event in pg.event.get():
                #check if user wants to close window
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.endButton.pressed = True
            self.endButton.update(pg.mouse.get_pos(),pg.mouse.get_pressed())
            if self.endButton.pressed == True:
                currentLevel = 0 
                g = Game()
                g.new(levelsList[currentLevel]) 
            self.screen.blit(self.endButton.image,(self.endButton.rect.x,self.endButton.rect.y))
            pg.display.flip()

    def showOptionsScreen(self):
        self.screen.blit(optionsScreen,(0,0))
        self.optionsToStartButton = Button('back1.png','back2.png',3*width/4,height/8,self.screen)
        while self.optionsToStartButton.pressed == False:
            #events section
            for event in pg.event.get():
                #check if user wants to close window
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                
            self.optionsToStartButton.update(pg.mouse.get_pos(),pg.mouse.get_pressed())
            self.screen.blit(self.optionsToStartButton.image,(self.optionsToStartButton.rect.x,self.optionsToStartButton.rect.y))
            pg.display.flip()

        self.showStartScreen()
        
        

g = Game()
g.showStartScreen()
while g.running:
    g.new(levelsList[currentLevel])
    g.showGameOverScreen()

pg.quit()
quit()
