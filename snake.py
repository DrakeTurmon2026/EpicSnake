import pygame
import numpy
import math
from random import *

#this code has been kindly yoinked from https://realpython.com/
pygame.init()
screen = pygame.display.set_mode([500, 500])

clock = pygame.time.Clock()
resettime = 0.135
movetimer = resettime

pygame.display.set_caption("DTier's Snake")

diesound = pygame.mixer.Sound("hitHurt.wav")
scoresound = pygame.mixer.Sound("pickupCoin.wav")
portalsound = pygame.mixer.Sound("Portal.wav")
juicyoffset = [0,0]

timer = 15

def lerp2(vec, goalvec, f):
    x = (vec[0] * (1  - f)) + (goalvec[0] * f)
    y = (vec[1] * (1  - f)) + (goalvec[1] * f)
    return [x,y]

class snake:
    def __init__(self,color,length,position):
        self.color = color
        self.length = length
        self.position = position
        hist = []
        for i in range(length):
            hist.append(position)
        self.history = hist
        self.dir = 0
        self.inputque = []
        self.perished = False
    def move(self):
        global dirlist

        if len(self.inputque) > 0:
            self.dir = self.inputque.pop(0)

        nextpos = numpy.add(self.position,dirlist[self.dir])

        if nextpos[0] > 24 or nextpos[0] < 0:
            self.perished = True
            pygame.mixer.Sound.play(diesound)
            return
        #seperating x and y so it is easier to do things
        if nextpos[1] > 24 or nextpos[1] < 0:
            self.perished = True
            pygame.mixer.Sound.play(diesound)
            return

        self.position = nextpos

        for num, pos in enumerate(self.history):
            if pos[0] == self.position[0] and pos[1] == self.position[1] and num != len(self.history) - 1:
                self.perished = True
                pygame.mixer.Sound.play(diesound)
                return

        #update pos history
        if self.length == 1:
            self.history = [self.position]
        else:
            self.history.insert(0,self.position)
            self.history.pop()
    def extend(self):
        self.length += 1
        toappend = self.history[len(self.history) - 1]
        self.history.append(toappend)

class apple:
    def __init__(self):
        self.Position = (randint(0,24), randint(0,24))
    def respawn(self):
        self.Position = (randint(0,24), randint(0,24))

class portal:
    def __init__(self, positon, color) -> None:
        self.position = positon
        self.Connected = None
        self.color = color
    def connect(self, other):
        self.Connected = other

plr = snake((0,255,0),2,[12,12])
appl = apple()
dirlist = [(0,-1),(1,0),(0,1),(-1,0)] #north,east,south,west

font = pygame.font.Font('ARCADECLASSIC.ttf', 100)
text = font.render("Game Over", False, (255,0,0))
smallfont = pygame.font.Font('ARCADECLASSIC.ttf', 30)
restarttext = smallfont.render("Press R to restart", False, (255,255,255))

RedPortal = portal([-1,-1], (250, 202, 42))
BluePortal = portal([-1,-1], (41, 130, 255))

RedPortal.connect(BluePortal)
BluePortal.connect(RedPortal)

textrect = text.get_rect()
textrect.center = (250,250)
rectstart = restarttext.get_rect()
rectstart.center = (250,300)

# Run until the user asks to quit
running = True
while running:
    dt = clock.tick(60)/1000

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if (plr.dir != 2 or len(plr.inputque) > 0) and plr.dir != 0:
                    plr.inputque.append(0)
            if event.key == pygame.K_RIGHT:
                if (plr.dir != 3 or len(plr.inputque) > 0) and plr.dir != 1:
                    plr.inputque.append(1)
            if event.key == pygame.K_DOWN:
                if (plr.dir != 0 or len(plr.inputque) > 0) and plr.dir != 2:
                    plr.inputque.append(2)
            if event.key == pygame.K_LEFT:
                if  (plr.dir != 1 or len(plr.inputque) > 0) and plr.dir != 3:
                    plr.inputque.append(3)
            if event.key == pygame.K_r:
                if plr.perished:
                    appl.respawn()
                    plr = snake((0,255,0),2,(12,12))

                    RedPortal = portal([-1,-1], (250, 202, 42))
                    BluePortal = portal([-1,-1], (41, 130, 255))

                    RedPortal.connect(BluePortal)
                    BluePortal.connect(RedPortal)

                    

    #JUICE
    juicyoffset = lerp2(juicyoffset,[0,0],0.2)
    
    #schmove man
    movetimer -= dt
    if movetimer <= 0 and not plr.perished:
        plr.move()
        movetimer = resettime

    #putting collision here makes it so you can graze your tail

    if plr.position[0] == appl.Position[0] and plr.position[1] == appl.Position[1]:
        appl.respawn()
        pygame.mixer.Sound.play(scoresound)
        plr.extend()
        
    if plr.position[0] == RedPortal.position[0] and plr.position[1] == RedPortal.position[1]:
        plr.position = RedPortal.Connected.position
    elif plr.position[0] == BluePortal.position[0] and plr.position[1] == BluePortal.position[1]:
        plr.position = BluePortal.Connected.position
    # Fill the background with white
    screen.fill((0, 0, 0))
    
    if not plr.perished:
        #render the apple
        pygame.draw.rect(screen, (255,0,0), pygame.rect.Rect(appl.Position[0]*20 + 1 + juicyoffset[0],appl.Position[1]*20 + 1 + juicyoffset[1],18,18))
        pygame.draw.rect(screen, RedPortal.color, pygame.rect.Rect(RedPortal.position[0]*20 + 1 + juicyoffset[0],RedPortal.position[1]*20 + 1 + juicyoffset[1],18,18))
        pygame.draw.rect(screen, BluePortal.color, pygame.rect.Rect(BluePortal.position[0]*20 + 1 + juicyoffset[0],BluePortal.position[1]*20 + 1 + juicyoffset[1],18,18))

        #render the snek
        for nu, pos in enumerate(plr.history):
            pygame.draw.rect(screen, plr.color, pygame.rect.Rect(pos[0]*20 + 1 + juicyoffset[0],pos[1]*20 + 1 + juicyoffset[1],18,18))

        #funny powerups thing
        if plr.length > 4:
            timer -= dt
            timertext = smallfont.render(str(math.ceil(timer)), False, (255,255,255))
            timerrect = timertext.get_rect()
            timerrect.center = (250, 30)
            screen.blit(timertext, timerrect)
            if timer <= 0:
                timer = 15
                RedPortal.position = [randint(0,24), randint(0,24)]
                BluePortal.position = [randint(0,24), randint(0,24)]
                pygame.mixer.Sound.play(portalsound)
                #do funny powerup stuff here
    else:
        screen.blit(text,textrect)
        screen.blit(restarttext,rectstart)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
