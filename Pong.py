import pygame,sys,time
from pygame.locals import *
from random import *

class Ball():
    def __init__(self,width,height):
        ''' This class represents the puck/ball object '''
        self.xValue = randint(0,width-20)
        self.yValue = randint(0,height-20)
        #start with blue color, and change every time it hits a wall
        self.color = [0,0,255]
        self.speedX = -1
        self.speedY = 1
        self = Rect(self.xValue,self.yValue,10,10)

pygame.init()
(width,height) = 300,300
screen = pygame.display.set_mode((width,height),0,32)
pygame.display.set_caption('Pong')

white = (255,255,255)
black = (0,0,0)
pink = (255,105,180)
red = (255,0,0)

PlayerRect = Rect(10,10,20,50)
OpponnentRect = Rect(250,10,20,50)
BallRect = Ball(width,height)

playerScore = 0
opponnentScore = 0

pygame.font.init()
myfont = pygame.font.SysFont('sans-serif',60)

#draw initial window values
txtPlayerScore = myfont.render(str(playerScore),False,white)
txtOpponnentScore = myfont.render(str(opponnentScore),False,white)

pygame.draw.rect(screen,pink,PlayerRect,0)
pygame.draw.rect(screen,pink,OpponnentRect,0)

pygame.display.update()

def drawRect(color,xValue,yValue):
    pygame.draw.rect(screen,color,[xValue,yValue,10,10])
    
def withinWindow(value,total):
    return (value > (total-10) or value < 0)

def updateScore(square):
    global playerScore
    global opponnentScore

    if(square.xValue < 0):
        playerScore += 1
    elif(square.xValue > width+10):
        opponnentScore += 1

def bounce(square,player,player2):    
    #if it hits a wall go in opposite direction, and change color
    if(withinWindow(square.yValue,height)):
        square.speedY *= -1
        square.color = [randint(20,255),randint(20,255),randint(20,255)]

    #if it hits a rect go in opposite direction and change color
    if(player.colliderect([square.xValue,square.yValue,10,10]) or
       player2.colliderect([square.xValue,square.yValue,10,10]) ):

        square.speedX *= -1
        square.color = [randint(20,255),randint(20,255),randint(20,255)]

    #if it goes outside the screen, update the score
    updateScore(square)

    #if it goes outside the screen, redraw the moving square
    if(withinWindow(square.xValue,width+20)):      
        drawRect(black,square.xValue,square.yValue) 
        square.xValue = 175
        square.yValue = 50
        drawMovingSquare(square,player,player2)

def drawMovingSquare(square,player,player2):
    #draw over the old square, and then draw a new one
    drawRect(black,square.xValue,square.yValue) 
    square.xValue += square.speedX
    square.yValue += square.speedY
    drawRect(square.color,square.xValue,square.yValue)

    bounce(square,player,player2)

def move(rectangle,move):
    pygame.draw.rect(screen,black,[rectangle.x,rectangle.y,20,50],0)
    rectangle.y += move
    pygame.draw.rect(screen,pink,[rectangle.x,rectangle.y,20,50],0)

def drawText():
    global txtPlayerScore
    global txtOpponnentScore
    global playerScore
    global opponnentScore

    txtPlayerScore = myfont.render(str(playerScore-1),1,black)
    screen.blit(txtPlayerScore,(115,0))
    txtPlayerScore = myfont.render(str(playerScore),1,white)
    screen.blit(txtPlayerScore,(115,0))

    txtOpponnentScore = myfont.render(str(opponnentScore-1),1,black)
    screen.blit(txtOpponnentScore,(160,0))
    txtOpponnentScore = myfont.render(str(opponnentScore),1,white)
    screen.blit(txtOpponnentScore,(160,0))
    
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    drawMovingSquare(BallRect,PlayerRect,OpponnentRect)
    
    if(event.type == pygame.KEYDOWN):
        #player 1
        if(event.key == pygame.K_s):
            move(PlayerRect,3)
        if(event.key == pygame.K_w):
            move(PlayerRect,-3)

        #player 2
        if(event.key == pygame.K_DOWN):
            move(OpponnentRect,3)
        if(event.key == pygame.K_UP):
            move(OpponnentRect,-3)

    #draw the scores
    drawText()

    #draw the middle line in the screen
    pygame.draw.line(screen,white,(150,0),(150,300),5)
    
    pygame.time.Clock().tick(60)
    pygame.display.update()

pygame.exitonclose()
