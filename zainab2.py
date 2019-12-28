import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports
def endwindow():
    pygame.init()
    window =pygame.display.set_mode((600,500))
    sound=pygame.mixer.Sound('gallery/audio/groove.wav')
    Font=pygame.font.SysFont('snapITC',18)
    surfacefont=Font.render('your Score of round',False,(255,16,0))
    surfacer=surfacefont.get_rect()
    surfacer.center=(200,200)
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
                font=pygame.font.SysFont('snapITC',10)
                text=font.render(self.text,0,(249,248,194))
                win.blit(text,(self.x+5,self.y+2
                               ))
        def IsOver(self,pos):
            if pos[0]>self.x and pos[0]<self.x +self.width:
                if pos[1]>self.y and pos[1]<self.y+self.height:
                    return True
            return False
    play_again=Button((204,16,0),180,420,90,30,'PLAY AGAIN')
    close=Button((204,16,0),320,420,60,30,'CLOSE')
    def image():
        window.fill((255,255,255))
        image = pygame.image.load('gallery/sprites/bg.png').convert_alpha()
        window.blit(image,(0,0))
        play_again.draw(window,(249,248,194))
        close.draw(window,(249,248,194))
        name=pygame.image.load('gallery/sprites/name.png').convert_alpha()
        window.blit( name,[150,10])
        window.blit(surfacefont,surfacer)
    x=True
    while x:
        image()
        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if play_again.IsOver(pos):
                    pygame.mixer.Sound('gallery/audio/groove.wav')
                    print("clicked!!!")
                    pygame.mixer.Sound.play(sound)
                    import mainclass
                if close.IsOver(pos):
                    pygame.mixer.Sound('gallery/audio/groove.wav')
                    print("clicked!!!")
                    pygame.mixer.Sound.play(sound)
                    run=False
                    pygame.quit()
                    sys.exit()
                    pygame.display.update()
            if 180+90>pos[0]> 180 and 420+30>pos[1]> 420: 
               play_again=Button((214,37,30),180,420,90,30,'PLAY AGAIN')
            else:
                play_again=Button((204,16,0),180,420,90,30,'PLAY AGAIN')
            if 320+60>pos[0]>320 and 420+30>pos[1]>420:
                close=Button((214,37,30),320,420,60,30,'CLOSE')
            else:
                close=Button((204,16,0),320,420,60,30,'CLOSE')


        pygame.display.update()
endwindow()
