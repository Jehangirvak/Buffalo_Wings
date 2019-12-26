import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports

pygame.init()
win =pygame.display.set_mode((500,500))
win.fill((255,255,255))
sound=pygame.mixer.Sound('gallery/audio/groove.wav')
class Button:
    def __init__(self,color,x,y,width,height,text=''):
        self.color=color
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.text=text
    def draw(self,win,outline=None):
        if outline:
            pygame.draw.rect(win,outline,(self.x-2,self.y-2,self.width+4,self.height+4),0)
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))
        if self.text!='':
            font=pygame.font.SysFont('snapITC',40)
            text=font.render(self.text,0,(249,248,194))
            win.blit(text,(self.x+5,self.y+2
                           ))
    def IsOver(self,pos):
        if pos[0]>self.x and pos[0]<self.x +self.width:
            if pos[1]>self.y and pos[1]<self.y+self.height:
                return True
        return False
run=True
button=Button((204,16,0),200,400,70,20,'GO')
smily_btn_1=Button((255,255,255),65,250,50,50)
smily_btn_2=Button((255,255,255),135,250,50,50)
smily_btn_3=Button((255,255,255),218,240,70,70)
smily_btn_4=Button((255,255,255),310,250,50,50)
smily_btn_5=Button((255,255,255),380,250,50,50)
def redrawWindow():
    win.fill((255,255,255))
    img = pygame.image.load('gallery/sprites/message1.png').convert_alpha()
    win.blit(img,(0,0))
    smile_1=pygame.image.load('gallery/sprites/smile1.png').convert_alpha()
    smily_btn_1.draw(win,(255,255,255))
    win.blit( smile_1,[64,250])
    smile_2=pygame.image.load('gallery/sprites/smile2.png').convert_alpha()
    smily_btn_2.draw(win,(255,255,255))
    win.blit( smile_2,[135,250])
    smile_3=pygame.image.load('gallery/sprites/bull_main.png').convert_alpha()
    smily_btn_3.draw(win,(255,255,255))
    win.blit( smile_3,[213,240])
    smile_4=pygame.image.load('gallery/sprites/smile7.png').convert_alpha()
    smily_btn_4.draw(win,(255,255,255))
    win.blit( smile_4,[310,250])
    smile_5=pygame.image.load('gallery/sprites/smile3.png').convert_alpha()
    smily_btn_5.draw(win,(255,255,255))
    win.blit( smile_5,[380,250])
    button.draw(win,(249,248,194))
while run:
    redrawWindow()
    for event in pygame.event.get():
        pos=pygame.mouse.get_pos()
        if event.type==pygame.QUIT:
            run=False
            pygame.quit()
            quit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            if button.IsOver(pos):
                pygame.mixer.Sound('gallery/audio/groove.wav')
                print("clicked!!!")
                pygame.mixer.Sound.play(sound)
                import mainclass
            if smily_btn_1.IsOver(pos):
                print("SMILe 1 ")
            if smily_btn_2.IsOver(pos):
                print("SMILe 2 ")
            if smily_btn_3.IsOver(pos):
                print("SMILe 3 ")
            if smily_btn_4.IsOver(pos):
                print("SMILe 4 ")
            if smily_btn_5.IsOver(pos):
                print("SMILe 5 ")
        if 200+100>pos[0]> 200 and 400+50>pos[1]> 400:
            button=Button((204,16,0),200,400,100,50,'GO!')
        else:
            button=Button((214,37,33),200,400,100,50,'GO!')
    pygame.display.update()
