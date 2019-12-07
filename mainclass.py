import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports

# Global Variables for the game
SCREENWIDTH = 289
SCREENHEIGHT = 511
GROUNDY = SCREENHEIGHT * 0.8  #base.png 80% height
GAME_SPRITES = {} #images used in game
GAME_SOUNDS = {}  #sounds used in game
#initialising the images rendered in the game
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'



class Buffalo_Wing:
  def __init__(self):
    self.FPS = 32   #frames per second
    self.SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))  #initialise screen
    #This will be the main point from where game will start
    pygame.init() #Initialize all pygame's modules
    self.FPSCLOCK = pygame.time.Clock() #to control fps 
    pygame.display.set_caption('Flappy Bird by HibJehZay')
    #adding keys values to dictionary
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
      )  #key-value pair with tuple as the value
          #conv alpha = optimises images for faster blitting

    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    ) #two elements in tuple, to rotate the pipe
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

      # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    self.welcomeScreen() #Shows welcome screen to the user until a button is pressed
    self.mainGame() #This is the main game function 

  def welcomeScreen(self):
    """
    Shows welcome images on the screen
    """

    self.playerx = int(SCREENWIDTH/5) #adds the bird at the 1/5th of screen self.width
    self.playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2) #makes the bird centre position, (total height- bird pic height)/2
    self.messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    self.messagey = int(SCREENHEIGHT*0.13)
    self.basex = 0 #the base image is always on 0 of x
    while True:
        for event in pygame.event.get():  #monitors all button clicks
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE): #eiter clicks on cross or esc key
                pygame.quit()
                sys.exit()
            #KEYDOWN refers to a keyboard key pressed
            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return   #according to func call, return will start game
            else:
                self.SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                self.SCREEN.blit(GAME_SPRITES['player'], (self.playerx, self.playery))    
                self.SCREEN.blit(GAME_SPRITES['message'], (self.messagex,self.messagey))    
                self.SCREEN.blit(GAME_SPRITES['base'], (self.basex, GROUNDY))    
                pygame.display.update()  #runs all the blits
                self.FPSCLOCK.tick(self.FPS)

  def mainGame(self):
    self.score = 0
    #adjusting inital position of birdy
    self.playerx = int(SCREENWIDTH/5)
    self.playery = int(SCREENWIDTH/2)
    self.basex = 0

    # Create 2 pipes for blitting on the screen
    #the pipes move, the bird doesn't (illusion)
    self.newPipe1 = self.getRandomPipe()
    self.newPipe2 = self.getRandomPipe()

    #List of upper pipes
    self.upperPipes = [
        {'x': SCREENWIDTH+200, 'y':self.newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':self.newPipe2[0]['y']},
    ]
    #List of lower pipes
    self.lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':self.newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':self.newPipe2[1]['y']},
    ]

    self.pipeVelX = -4 #velocity of pipes moving backwards

    self.playerVelY = -9 #velocity of bird falling down
    self.playerMaxVelY = 10 #max up arrow/space velocity
    self.playerMinVelY = -8
    self.playerAccY = 1 #acceleration while falling

    self.playerFlapAccv = -8 #velocity while flapping
    self.playerFlapped = False # It is true only when the bird is flapping

    #game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if self.playery > 0: #birdy is above ground
                    self.playerVelY = self.playerFlapAccv #birdy goes up
                    self.playerFlapped = True
                    GAME_SOUNDS['wing'].play()  #plays sound

        #This function will return true if the player is crashed
        self.crashTest = self.isCollide(self.playerx, self.playery, self.upperPipes, self.lowerPipes) 
        if self.crashTest:
            return     

        #check for score
        self.playerMidPos = self.playerx + GAME_SPRITES['player'].get_width()/2 #getting birdy centre position
        #if birdy centre passes pipe == point + 1
        for pipe in self.upperPipes:
            self.pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if self.pipeMidPos<= self.playerMidPos < self.pipeMidPos +4:
                self.score +=1
                print(f"Your score is {self.score}") 
                GAME_SOUNDS['point'].play()
                self.incSpeed()


        if self.playerVelY <self.playerMaxVelY and not self.playerFlapped:
            self.playerVelY += self.playerAccY

        #if user clicks up/space once, then crashes lateron
        if self.playerFlapped:
            self.playerFlapped = False            
        self.playerHeight = GAME_SPRITES['player'].get_height()
        self.playery = self.playery + min(self.playerVelY, GROUNDY - self.playery - self.playerHeight) #the min returns 0, so the birdy stays on ground

        #move pipes to the left
        for upperPipe , lowerPipe in zip(self.upperPipes, self.lowerPipes): #zip creates subsets of two values from each list (x,y)
            upperPipe['x'] += self.pipeVelX
            lowerPipe['x'] += self.pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<self.upperPipes[0]['x']<5:
            self.newpipe = self.getRandomPipe()
            self.upperPipes.append(self.newpipe[0])
            self.lowerPipes.append(self.newpipe[1])

        # if the pipe is out of the screen, remove it
        if self.upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            self.upperPipes.pop(0)
            self.lowerPipes.pop(0)
        
        # Lets blit our sprites now
        self.SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(self.upperPipes, self.lowerPipes):
            self.SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            self.SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        self.SCREEN.blit(GAME_SPRITES['base'], (self.basex, GROUNDY))
        self.SCREEN.blit(GAME_SPRITES['player'], (self.playerx, self.playery))
        self.myDigits = [int(x) for x in list(str(self.score))]
        self.width = 0
        for digit in self.myDigits:
            self.width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - self.width)/2

        for digit in self.myDigits:
            self.SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        self.FPSCLOCK.tick(self.FPS)

  def incSpeed(self):
    if self.score>6 and self.score<10:
      self.FPS = 32+10   #frames per second
    elif self.score>10 and self.score<15:
      self.FPS = 32+15
    elif self.score>15 and self.score<20:
      self.FPS = 32+20
    elif self.score>20:
      self.FPS = 32+25
    return


  def isCollide(self,playerx, playery, upperPipes, lowerPipes):
    self.playerx=playerx
    self.playery=playery
    self.upperPipes=upperPipes
    self.lowerPipes=lowerPipes
    if self.playery> GROUNDY - 25  or self.playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in self.upperPipes:
        self.pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(self.playery < self.pipeHeight + pipe['y'] and abs(self.playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in self.lowerPipes:
        if (self.playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(self.playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

  def getRandomPipe(self):
      """
      Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
      """
      self.pipeHeight = GAME_SPRITES['pipe'][0].get_height() #accessing 0th index of tuple value from dict
      self.offset = SCREENHEIGHT/3 #space for bird to pass
      self.y2 = self.offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *self.offset)) #generates a random # between specified range
      self.pipeX = SCREENWIDTH + 10
      self.y1 = self.pipeHeight - self.y2 + self.offset
      self.pipe = [
          {'x': self.pipeX, 'y': -self.y1}, #upper Pipe, neg because inverted
          {'x': self.pipeX, 'y': self.y2} #lower Pipe
      ]
      return self.pipe

def stages():
  x=0
  while x < 6:
    if obj.crashTest==True:
      x+=1
      objB=Buffalo_Wing()

obj=Buffalo_Wing()
stages()



