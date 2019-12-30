import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
import time
from pygame.locals import * # Basic pygame imports

# Global Variables for the game
SCREENWIDTH = 320
SCREENHEIGHT = 560
GROUNDY = SCREENHEIGHT * 0.84  #base.png 84% height
GAME_SPRITES = {} #images used in game
GAME_SOUNDS = {}  #sounds used in game

i=2    #initialising the images rendered in the game
class images:
  def __init__(self):
    self.Playerimg=[ 'gallery/sprites/smile1.png','gallery/sprites/smile2.png', 'gallery/sprites/bull-big.png',
                    'gallery/sprites/smile7.png','gallery/sprites/smile3.png']  #list containing avatar images and their base values

  def playerimg_base(self):
    global i
    global BASE
    if i==2:
      BASE=45
    """
    Returns the image of avatar that player chose
    """
    return self.Playerimg[i]
    

img=images()
BASE=60         #the base of the avatar 
PIPE= 'gallery/sprites/pipe.png'

#added queue data structure to points on the basis of FIFO rule
class Point_Queue:
  def __init__(self):
    self.queue=[]

  def __len__(self):
    return len(self.queue)

  def enqueque(self,score):
    """
    Add points to queue list
    """
    self.score=score
    self.queue.append(self.score)

  def dequeue(self):
    """
    Remove points from queue list
    """
    point=self.queue.pop(0)  
    return point

class Buffalo_Wing:
  scorequeue=Point_Queue()
  def __init__(self):
    self.BACKGROUNDlist=['gallery/sprites/bg1.png','gallery/sprites/bg2.png','gallery/sprites/bg3.png'] #list of different backgrounds
    self.BACKGROUND= 'gallery/sprites/background.png'
    self.PLAYER= img.playerimg_base()
    self.crash_avatar=['gallery/sprites/smile5.png','gallery/sprites/smile4.png']
    self.FPS = 32   #frames per second
    self.SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))  #initialise screen
    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/message.png').convert_alpha()
    #This will be the main point from where game will start
    pygame.init() #Initialize all pygame's modules
    self.FPSCLOCK = pygame.time.Clock() #to control fps 
    pygame.display.set_caption('BUFFALO WINGS')
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

    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha())   #two elements in tuple, to rotate the pipe
    GAME_SPRITES['background'] = pygame.image.load(self.BACKGROUND).convert_alpha()
    GAME_SPRITES['player'] = pygame.image.load(self.PLAYER).convert_alpha()

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

    self.playerx = int(SCREENWIDTH/5) #adds the avatar at the 1/5th of screen self.width
    self.playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2) #makes the avatar centre position, (total height- avatar pic height)/2
    self.messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    self.messagey = int(SCREENHEIGHT*0.01)
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
    """
    The main game function
    """
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
    self.playerVelY = -9 #velocity of avatar falling down
    self.playerMaxVelY = 10 #max up arrow/space velocity
    self.playerMinVelY = -8
    self.playerAccY = 1 #acceleration while falling

    self.playerFlapAccv = -8 #acceleration while flapping
    self.playerFlapped = False # It is true only when the avatar is flapping

    #game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if self.playery > 0: #avatar is above ground
                    self.playerVelY = self.playerFlapAccv #avatar goes up
                    self.playerFlapped = True
                    GAME_SOUNDS['wing'].play()  #plays sound

        #This function will return true if the player is crashed
        self.crashTest = self.isCollide(self.playerx, self.playery, self.upperPipes, self.lowerPipes) 
        if self.crashTest:
            Buffalo_Wing.scorequeue.enqueque(self.score)
            print(f"Your score is {self.score}")
            return     

        #check for score
        self.playerMidPos = self.playerx + GAME_SPRITES['player'].get_width()/2 #getting birdy centre position
        #if birdy centre passes pipe == point + 1
        for pipe in self.upperPipes:
            self.pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if self.pipeMidPos<= self.playerMidPos < self.pipeMidPos +4:
                self.score +=1
                print(self.score)
                GAME_SOUNDS['point'].play()
                if self.score>5:
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
    """
    To increase the speed with respect to increasing score
    """
    if self.score>=6 and self.score<=10:
      self.BACKGROUND=self.BACKGROUNDlist[0]
      GAME_SPRITES['background'] = pygame.image.load(self.BACKGROUND).convert()
      self.SCREEN.blit(GAME_SPRITES['background'], (0, 0))
      pygame.display.update()
      self.FPS = 32+5   #frames per second
    elif self.score>10 and self.score<15:
      self.BACKGROUND=self.BACKGROUNDlist[1]
      GAME_SPRITES['background'] = pygame.image.load(self.BACKGROUND).convert()
      self.SCREEN.blit(GAME_SPRITES['background'], (0, 0))
      pygame.display.update()
      self.FPS = 32+7
    else:
      if (self.score%5)==0:
        self.BACKGROUND=random.choice(self.BACKGROUNDlist)
        GAME_SPRITES['background'] = pygame.image.load(self.BACKGROUND).convert()
        self.SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        pygame.display.update()
        self.FPS=self.FPS+1
    return


  def isCollide(self,playerx, playery, upperPipes, lowerPipes):
    """
    Collison conditions with ground and obstacles
    """
    self.playerx=playerx
    self.playery=playery
    self.upperPipes=upperPipes
    self.lowerPipes=lowerPipes
    if self.playery> GROUNDY - BASE  or self.playery<0:
        GAME_SOUNDS['hit'].play()
        if BASE != 45 :
          self.PLAYER='gallery/sprites/smile6.png' 
          GAME_SPRITES['player'] = pygame.image.load(self.PLAYER).convert_alpha()
          self.SCREEN.blit(GAME_SPRITES['player'], (self.playerx, self.playery))
          pygame.display.update()
          time.sleep(1)
        self.SCREEN.blit(GAME_SPRITES['message'], (self.messagex,self.messagey))       
        pygame.display.update()  #runs all the blits
        return True
    
    for pipe in self.upperPipes:
        self.pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(self.playery < self.pipeHeight + pipe['y'] and abs(self.playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            if BASE != 25 and BASE != 45 :
              self.PLAYER=random.choice(self.crash_avatar)
              GAME_SPRITES['player'] = pygame.image.load(self.PLAYER).convert_alpha()
              self.SCREEN.blit(GAME_SPRITES['player'], (self.playerx, self.playery))
              pygame.display.update()
              time.sleep(1)
            self.SCREEN.blit(GAME_SPRITES['message'], (self.messagex,self.messagey))       
            pygame.display.update()  #runs all the blits
            return True

    for pipe in self.lowerPipes:
        if (self.playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(self.playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            if BASE != 25 and BASE != 45 :
              self.PLAYER=random.choice(self.crash_avatar)
              GAME_SPRITES['player'] = pygame.image.load(self.PLAYER).convert_alpha()
              self.SCREEN.blit(GAME_SPRITES['player'], (self.playerx, self.playery))
              pygame.display.update()
              time.sleep(1)
            self.SCREEN.blit(GAME_SPRITES['message'], (self.messagex,self.messagey))       
            pygame.display.update()  #runs all the blits
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
          {'x': self.pipeX, 'y': self.y2}    #lower Pipe
      ]
      return self.pipe


'''This class displays the total score to the user'''
class Score:
    def __init__(self):
        pygame.init()
        self.window =pygame.display.set_mode((600,500))
        self.Font=pygame.font.SysFont('snapITC',20)
        self.play_again=Button((202,0,0),180,420,90,30,'PLAY AGAIN')
        self.close=Button((202,0,0),320,420,60,30,'CLOSE')
        self.home=Button((150,223,178),15,15,55,55)
        self.depends=str()
        self.statement=str()
        self.score= 0
        self.scoreque=Buffalo_Wing.scorequeue
        self.condition()
        
    '''this function holding conditions on the basis of score'''
    def condition(self):
        self.L=[]
        for rounds in range(self.scoreque.__len__()):
          indiv_score = self.scoreque.dequeue()
          self.score=self.score+indiv_score
          self.statement= 'The score of round '+str(rounds+1)+' is: '+str(indiv_score)+'!'
          self.L.append(self.statement)
          print(self.score)
          
        if self.score>=25:
          self.depends="WELL PLAYED! with a great total score of "+str(self.score)
        elif self.score>=20:
            self.depends="Nicely played! with a total score of " + str(self.score)
        elif self.score>=15:
            self.depends="Good! your total score is "+ str(self.score)
        elif self.score>=10:
            self.depends="Average! your total score is "+ str(self.score)
        elif self.score>=1:
            self.depends="Poorly played! your total score is "+ str(self.score)
        else:
          self.depends="Pathetically played! You scored nothing!"
        print(self.L)
    def endwin(self):
        self.window.fill((255,255,255))
        self.image = pygame.image.load('gallery/sprites/bg.png').convert_alpha()
        self.window.blit(self.image,(0,0))
        self.play_again.draw(self.window,10,(249,248,194))
        self.homeimg = pygame.image.load('gallery/sprites/home.png').convert_alpha()
        
        self.home.draw(self.window,(150,223,178))
        self.window.blit(self.homeimg,(15,15))
        self.close.draw(self.window,10,(249,248,194))
        self.name=pygame.image.load('gallery/sprites/name.png').convert_alpha()
        self.window.blit( self.name,[150,10])
        self.surfacefont0=self.Font.render(self.L[0],True,(255,255,255))
        self.surfacer0=self.surfacefont0.get_rect()
        self.surfacer0.center=(300,152)
        self.window.blit(self.surfacefont0,self.surfacer0)
        self.surfacefont=self.Font.render(self.L[0],True,(255,16,0))
        self.surfacer=self.surfacefont.get_rect()
        self.surfacer.center=(300,150)
        self.window.blit(self.surfacefont,self.surfacer)
        self.surfacefont__1=self.Font.render(self.L[1],True,(255,255,255))
        self.surfacer__1=self.surfacefont__1.get_rect()
        self.surfacer__1.center=(300,202)
        self.window.blit(self.surfacefont__1,self.surfacer__1)
        self.surfacefont_1=self.Font.render(self.L[1],True,(255,16,0))
        self.surfacer_1=self.surfacefont_1.get_rect()
        self.surfacer_1.center=(300,200)
        self.window.blit(self.surfacefont_1,self.surfacer_1)
        self.surfacefont__2=self.Font.render(self.L[2],True,(255,255,255))
        self.surfacer__2=self.surfacefont__2.get_rect()
        self.surfacer__2.center=(300,252)
        self.window.blit(self.surfacefont__2,self.surfacer__2)
        self.surfacefont_2=self.Font.render(self.L[2],True,(255,16,0))
        self.surfacer_2=self.surfacefont_2.get_rect()
        self.surfacer_2.center=(300,250)
        self.window.blit(self.surfacefont_2,self.surfacer_2)
        self.surfacefont__3=self.Font.render(self.L[3],True,(255,255,255))
        self.surfacer__3=self.surfacefont__3.get_rect()
        self.surfacer__3.center=(300,302)
        self.window.blit(self.surfacefont__3,self.surfacer__3)
        self.surfacefont_3=self.Font.render(self.L[3],True,(255,16,0))
        self.surfacer_3=self.surfacefont_3.get_rect()
        self.surfacer_3.center=(300,300)
        self.window.blit(self.surfacefont_3,self.surfacer_3)
        self.surfacefont_t=self.Font.render(self.depends,True,(255,255,255))
        self.surfacer_t=self.surfacefont_t.get_rect()
        self.surfacer_t.center=(300,352)
        self.window.blit(self.surfacefont_t,self.surfacer_t)
        self.surfacefont_T=self.Font.render(self.depends,True,(255,16,0))
        self.surfacer_T=self.surfacefont_T.get_rect()
        self.surfacer_T.center=(300,350)
        self.window.blit(self.surfacefont_T,self.surfacer_T)
        
        
        
    def while_loop(self):
        
        x=True
        while x:
            self.endwin()
            for event in pygame.event.get():
                pos=pygame.mouse.get_pos()
                if event.type==pygame.QUIT:
                    run=False
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if self.play_again.IsOver(pos):
                        pygame.mixer.Sound(GAME_SOUNDS['click'])
                        print("clicked!!!")
                        Obj=Buffalo_Wing()
                        stages()
                    if self.home.IsOver(pos):
                        pygame.mixer.Sound(GAME_SOUNDS['click'])
                        print("clicked!!!")
                        import FINAL
                    if self.close.IsOver(pos):
                        pygame.mixer.Sound.play(GAME_SOUNDS['click'])
                        print("clicked!!!")
                        run=False
                        pygame.quit()
                        sys.exit()
                        pygame.display.update()
                if 180+90>pos[0]> 180 and 420+30>pos[1]> 420: 
                   self.play_again=Button((77,226,13),180,420,90,30,'PLAY AGAIN')
                else:
                    self.play_again=Button((255,0,0),180,420,90,30,'PLAY AGAIN')
                if 320+60>pos[0]>320 and 420+30>pos[1]>420:
                    self.close=Button((77,226,13),320,420,60,30,'CLOSE')
                else:
                    self.close=Button((255,0,0),320,420,60,30,'CLOSE')
            pygame.display.update()
BACKGROUNDlist=[('gallery/sprites/bg1.png'),('gallery/sprites/bg2.png'),('gallery/sprites/bg3.png')] #list of different backgrounds
def stages():
  """
  Generate 5 chances of the player
  """
  chances=0
  while chances <3 :
    if obj.crashTest==True:
      chances+=1
      objB=Buffalo_Wing()
  else:
    Obj=Score()
    Obj.while_loop()
    
pygame.init()
win =pygame.display.set_mode((500,500))
GAME_SOUNDS['click']=pygame.mixer.Sound('gallery/audio/groove.wav')
GAME_SOUNDS['play_btn']=pygame.mixer.Sound('gallery/audio/play_btn.wav')
GAME_SOUNDS['bull']=pygame.mixer.Sound('gallery/audio/bull.wav')
GAME_SOUNDS['evil']=pygame.mixer.Sound('gallery/audio/evil.wav')
GAME_SOUNDS['cartoon']=pygame.mixer.Sound('gallery/audio/cartoon.wav')
GAME_SOUNDS['star']=pygame.mixer.Sound('gallery/audio/star.wav')

class Button:
    def __init__(self,color,x,y,width,height,text=''):
        self.color=color
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.text=text
    def draw(self,win,fontsize=None,outline=None):
        self.fontsize=fontsize
        if outline:
            pygame.draw.rect(win,outline,(self.x-2,self.y-2,self.width+4,self.height+4),0)
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))
        if self.text!='':
            font=pygame.font.SysFont('snapITC',self.fontsize)
            text=font.render(self.text,0,(249,248,194))
            win.blit(text,(self.x+5,self.y+2))
    def IsOver(self,pos):
        if pos[0]>self.x and pos[0]<self.x +self.width:
            if pos[1]>self.y and pos[1]<self.y+self.height:
                return True
        return False
run=True
back=Button((240,192,84),65,370,55,55)
button=Button((77,226,13),100,400,70,20,'GO')
htp=Button((77,226,13),250,400,125,50,'HELP!')
smily_btn_1=Button((128,201,236),65,250,50,50)
smily_btn_2=Button((128,201,236),135,250,50,50)
smily_btn_3=Button((128,201,236),215,240,70,70)
smily_btn_4=Button((128,201,236),309,250,50,50)
smily_btn_5=Button((128,201,236),380,250,50,50)
forward=Button((240,192,84),470,370,55,55)
def redrawWindow():
    win.fill((255,255,255))
    img = pygame.image.load('gallery/sprites/message1.png').convert_alpha()
    win.blit(img,(0,0))
    smile_1=pygame.image.load('gallery/sprites/smile1.png').convert_alpha()
    smily_btn_1.draw(win)
    win.blit( smile_1,[64,250])
    smile_2=pygame.image.load('gallery/sprites/smile2.png').convert_alpha()
    smily_btn_2.draw(win)
    win.blit( smile_2,[135,250])
    smile_3=pygame.image.load('gallery/sprites/bull_main.png').convert_alpha()
    smily_btn_3.draw(win)
    win.blit( smile_3,[213,240])
    smile_4=pygame.image.load('gallery/sprites/smile7.png').convert_alpha()
    smily_btn_4.draw(win)
    win.blit( smile_4,[310,250])
    smile_5=pygame.image.load('gallery/sprites/smile3.png').convert_alpha()
    smily_btn_5.draw(win)
    win.blit( smile_5,[380,250])
    button.draw(win,40,(249,248,194))
    htp.draw(win,29,(249,248,194))
class HOW:
  def __init__(self):
        pygame.init()
        self.window =pygame.display.set_mode((600,500))
        self.Font=pygame.font.SysFont('Ariel',23)
        self.window.fill((255,255,255))
        self.img=pygame.image.load('gallery/sprites/bg.png').convert_alpha()
        self.window.blit(self.img,(0,0))
        self.name=pygame.image.load('gallery/sprites/name.png').convert_alpha()
        self.window.blit( self.name,[150,10])
        backimg=pygame.image.load('gallery/sprites/back.png').convert_alpha()
        back.draw(self.window)
        if __name__ == "__main__":
            self.window.blit( backimg,[65,370])
        fwd=pygame.image.load('gallery/sprites/forward.png').convert_alpha()
        forward.draw(self.window)
        self.window.blit( fwd,[470,370])
        pygame.display.update()
        self.text="Each game consists of FOUR rounds.\nThe difficulty level of each round increases with the passage of time.\nAvoid collision with the ground and pipes.\nAt the end you will be shown your total and the individual scores of each round."

  def render_multi_line(self):
        lines = self.text.splitlines()
        for i, l in enumerate(lines):
            self.t=self.Font.render(l,True, (255,255,255))
            self.t1=self.t.get_rect()
            self.t1.center=(300,202+i*30)
            self.window.blit(self.t,self.t1)
            pygame.display.update()
        for i, l in enumerate(lines):
            self.t=self.Font.render(l,True, (128,64,0))
            self.t1=self.t.get_rect()
            self.t1.center=(300,200+i*30)
            self.window.blit(self.t,self.t1)
            pygame.display.update()
        

val=0
run = True
while run:
    redrawWindow()
    BASE=60
    for event in pygame.event.get():
        pos=pygame.mouse.get_pos()
        if event.type==pygame.QUIT:
            run=False
            pygame.quit()
            sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            if htp.IsOver(pos):
                pygame.mixer.Sound.play(GAME_SOUNDS['click'])
                object1=HOW()
                object1.render_multi_line()
                done =True
                run=False
            
            if button.IsOver(pos):
                print("clicked!!!")
                pygame.mixer.Sound.play(GAME_SOUNDS['click'])
                obj=Buffalo_Wing()
                stages()
            if smily_btn_1.IsOver(pos):
              i=0
              Buffalo_Wing.PLAYER=img.playerimg_base()
              pygame.mixer.Sound.play(GAME_SOUNDS['star'])
              val=i+1
              print("SMILe 1 ")
            elif smily_btn_2.IsOver(pos):
              pygame.mixer.Sound.play(GAME_SOUNDS['play_btn'])
              i=1
              val=i+1
              Buffalo_Wing.PLAYER=img.playerimg_base()
              print("SMILe 2 ")
            elif smily_btn_3.IsOver(pos):
              pygame.mixer.Sound.play(GAME_SOUNDS['bull'])
              i=2
              val=i+1
              Buffalo_Wing.PLAYER=img.playerimg_base()       
              print("SMILe 3 ")
              
            elif smily_btn_4.IsOver(pos):
              pygame.mixer.Sound.play(GAME_SOUNDS['evil'])
              i=3
              val=i+1
              Buffalo_Wing.PLAYER=img.playerimg_base()
              print("SMILe 3 ")
            elif smily_btn_5.IsOver(pos):
              pygame.mixer.Sound.play(GAME_SOUNDS['cartoon'])
              i=4
              val=i+1
              Buffalo_Wing.PLAYER=img.playerimg_base()
              print("SMILe 4 ")
            else:
              i=2
              Buffalo_Wing.PLAYER=img.playerimg_base()
        if 250+125>pos[0]>250 and 400+50>pos[1]>400:
            htp=Button((77,226,13),250,400,125,50,'HELP!')
        else:
            htp=Button((214,37,33),250,400,125,50,'HELP!')
        if 100+100>pos[0]> 100 and 400+50>pos[1]> 400:
            button=Button((77,226,13),100,400,100,50,'GO!')
        else:
            button=Button((214,37,33),100,400,100,50,'GO!')
        if 65+50>pos[0]>65 and 250+50>pos[1]>250:
            smily_btn_1=Button((215,234,239),65,250,50,50)
        else:
            smily_btn_1=Button((128,201,236),65,250,50,50)
            
        if 135+50>pos[0]>135 and 250+50>pos[1]>250:
            smily_btn_2=Button((215,234,239),135,250,50,50)
        else:
            smily_btn_2=Button((128,201,236),135,250,50,50)
            
        if 215+70>pos[0]>215 and 240+70>pos[1]>240:
           smily_btn_3=Button((215,234,239),215,240,75,70)
        else:
           smily_btn_3=Button((128,201,236),215,240,70,70)
           
        if 309+50>pos[0]>309 and 250+50>pos[1]>250:
           smily_btn_4=Button((215,234,239),309,250,50,50)
        else:
           smily_btn_4=Button((128,201,236),309,250,50,50)
           
        if 380+50>pos[0]>380 and 250+50>pos[1]>250:
           smily_btn_5=Button((215,234,239),380,250,50,50)
        else:
          smily_btn_5=Button((128,201,236),380,250,50,50)
    if val==1 and run == True:
      select_btn=Button((0,128,0),350,360,145,30,'Avatar  1  selected')
      select_btn.draw(win,12,(249,248,194))
    elif val ==2and run == True:
      select_btn=Button((0,128,0),350,360,145,30,'Avatar  2  selected')
      select_btn.draw(win,12,(249,248,194))
    elif val==3and run == True:
      select_btn=Button((0,128,0),350,360,145,30,'Avatar  3  selected')
      select_btn.draw(win,12,(249,248,194))
    elif val==4and run == True:
      select_btn=Button((0,128,0),350,360,145,30,'Avatar  4  selected')
      select_btn.draw(win,12,(249,248,194))
    elif val==5and run == True:
      select_btn=Button((0,128,0),350,360,145,30,'Avatar  5  selected')
      select_btn.draw(win,12,(249,248,194))
    pygame.display.update()

while not run:
  for event in pygame.event.get():
          pos=pygame.mouse.get_pos()
          if event.type==pygame.QUIT:
              run=False
              pygame.quit()
              sys.exit()
          if event.type==pygame.MOUSEBUTTONDOWN:
            if back.IsOver(pos):
              run=True
              pygame.mixer.Sound.play(GAME_SOUNDS['click'])
              import FINAL
            if forward.IsOver(pos):
               run=True
               pygame.mixer.Sound.play(GAME_SOUNDS['click'])
               obj=Buffalo_Wing()
               stages()
