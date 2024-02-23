#Imports
import pygame
from sys import exit
from ColourBank import Colour
import math

#Functions
def textBar(font):
    underTextSurface = pygame.Surface((windowWidth,windowHeight / 3 * 1))
    pygame.draw.rect(underTextSurface,Colour().white,(0,0,1200,1),1,)
    return underTextSurface

def angleCircle(radius,windowWidth,windowHeight):
    #Draws Circle
    angleCircleSurface = pygame.Surface((windowWidth,windowHeight))
    pygame.draw.circle(angleCircleSurface,Colour().white,(windowWidth / 2, windowHeight / 3 * 2),radius,3)
    angle = angleFinder()

    #Draws
    pygame.draw.line(angleCircleSurface,Colour().white,(windowWidth / 2, windowHeight / 3 * 2),(pointRelay(radius,angle,windowWidth,windowHeight)),3)

    #Converts angle
    degreesAngle = angle * 180 / math.pi
    degreesAngle = math.floor(degreesAngle)
    
    #Renders
    angleText = pygame.Surface((windowWidth,windowHeight))
    angleText = baseFont.render(str(degreesAngle),False,Colour().white)
    angleCircleSurface.blit(angleText,(pointRelay(radius * 1.25,angle,windowWidth,windowHeight)))

    return angleCircleSurface

def angleFinder():
    #Gets Mouse position
    mouseX, mouseY = pygame.mouse.get_pos()
    mouseX = (mouseX - windowWidth / 2)
    mouseY = -1 * (mouseY - windowHeight / 3 * 2)

    #Calculates Angle
    if mouseX != 0:
        angle = math.atan(mouseY/mouseX)

    else:
        angle = math.pi

    return angle

def pointRelay(radius,angle,windowWidth,windowHeight):
    #Relays to point on circle
    circleX,circleY = (radius * math.cos(angle)),(radius * math.sin(angle))
    if angle <= 0:
        circleX = -circleX
        circleY = circleY

    elif angle > 0:
        circleX = circleX
        circleY = -circleY

    return (circleX + windowWidth / 2) - 3,(circleY + windowHeight / 3 * 2) + 3

def trajectory(inputVelocity,angle,windowWidth,windowHeight):
    trajectorySurface = pygame.Surface((windowWidth,windowHeight))
    verticalVelocity = inputVelocity * math.sin(angle)
    horizontalVelocity = inputVelocity * math.cos(angle)
    objectX = windowWidth / 2
    objectY =  windowHeight / 3 * 2
    bounces = 0

    while bounces < 10:
        print(angle,objectX,objectY)
        if angle > 0:
            pygame.draw.circle(trajectorySurface,Colour().purple,(objectX,objectY),5)

        else:
            pygame.draw.circle(trajectorySurface,Colour().purple,(-objectX,objectY),5)

        verticalVelocity -= 9.81
        objectX += horizontalVelocity
        objectY -= verticalVelocity

        if objectY < 0:
            objectY = 1
            horizontalVelocity = horizontalVelocity * 0.8
            verticalVelocity = verticalVelocity * -0.7
            bounces +=1

        if objectY > windowHeight / 3 * 2:
            objectY = windowHeight / 3 * 2
            horizontalVelocity = horizontalVelocity * 0.8
            verticalVelocity = verticalVelocity * -0.7
            bounces +=1

        if objectX < 0:
            objectX = 1
            horizontalVelocity = horizontalVelocity * -0.7
            verticalVelocity = verticalVelocity *0.8
            bounces +=1

        if objectX > windowWidth:
            objectX = windowWidth -1
            horizontalVelocity = horizontalVelocity * -0.7
            verticalVelocity = verticalVelocity *0.8
            bounces +=1

    return trajectorySurface


#Variable initialising
windowWidth,windowHeight = 1200, 600

#Screen Setup
pygame.init()
screen = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption("Projectile Motion Sim 2.0")

#Framerate
frameRate = 144
clock = pygame.time.Clock()

#Base objects and Surfaces
prestonPlanet1 = pygame.image.load("Pesot1.webp")
prestonPlanet2 = pygame.image.load("Pesot2.webp")
baseFont = pygame.font.Font(None,20)
radius = 150

#Event Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit()

    screen.blit(angleCircle(radius,windowWidth, windowHeight),(0,0))
    screen.blit(textBar(baseFont),(0, windowHeight/ 3 * 2))
    screen.blit(trajectory(100,angleFinder(),windowWidth,windowHeight),(0,0))


    pygame.display.update()
    clock.tick(frameRate)


