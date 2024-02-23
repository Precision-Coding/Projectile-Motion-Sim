#Imports
import pygame
from sys import exit
from ColourBank import Colour
import math

#Functions
def angleCalculator(circleCentre):
    x, y = pygame.mouse.get_pos()
    centreX,centreY = circleCentre
    x = x - centreX
    y = centreY - y

    if x != 0:
        radAngle = math.atan(y/x)

    else:
        radAngle = math.pi / 2
    
    return radAngle

def radiansToDegrees(radianAngle):
    return radianAngle * 180 / math.pi

def angledLineMeetsCircle(radianAngle,radius):
    x = radius * math.cos(radianAngle)
    y = radius * math.sin(radianAngle)

    if radianAngle >= 0:
        return x,-y
    else:
        return -x,y

#Framerate
frameRate = 144
clock = pygame.time.Clock()

#Stuff
windowWidth,windowHeight = 1200, 600
radius = 150
circleCentre = windowWidth / 2,windowHeight / 3 * 2

#Screen Setup
pygame.init()
screen = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption("Projectile Motion Sim 2.0")

#Font
pygame.font.init()
baseFont = pygame.font.SysFont("helvetica",20)

#Base objects and Surfaces
prestonPlanet1 = pygame.image.load("Pesot1.webp")
prestonPlanet2 = pygame.image.load("Pesot2.webp")

def baseTextBar():
    textBar = pygame.Surface((windowWidth,windowHeight / 3))
    textBar.fill(Colour().darkGrey)
    pygame.draw.line(textBar,Colour().white,(0,0,),(windowWidth,0),2,)
    return textBar


def baseCircleCourt():
    circleCourt = pygame.Surface((windowWidth,windowHeight / 3 * 2))
    pygame.draw.circle(circleCourt,Colour().white,(circleCentre),radius,2)
    return circleCourt

def baseBallCourt():
    ballCourt = pygame.Surface((windowWidth,windowHeight / 3 * 2))

#Event Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit()

    #Text Bar Changes
    textBar = baseTextBar()
    degreesAngle = math.floor(radiansToDegrees(angleCalculator(circleCentre)))
    angleBox = baseFont.render(f"Firing Angle: {str(degreesAngle)}",True,Colour().white)
    textBar.blit(angleBox,(0,0))

    #Circle Changes

    #Line
    circleCourt = baseCircleCourt()
    circleX,circleY = circleCentre
    x,y = angledLineMeetsCircle(angleCalculator(circleCentre),radius)
    x,y = x + circleX, y + circleY 
    pygame.draw.line(circleCourt,Colour().white,circleCentre,(x,y))

    #AngleText
    x,y = angledLineMeetsCircle(angleCalculator(circleCentre),radius * 1.25)
    x,y = x + circleX, y + circleY 
    angleBox = baseFont.render(str(degreesAngle),True,Colour().white)
    circleCourt.blit(angleBox,(x,y))





    screen.blit(textBar,(0,windowHeight / 3 * 2))
    screen.blit(circleCourt,(0,0))
    ballCourt = pygame.Surface((windowWidth,windowHeight / 3 * 2))








    pygame.display.update()
    clock.tick(frameRate)


