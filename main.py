import pygame
from sys import exit
from colourBank import Colour
from physics import physics_sim
import math
import random


# Functions

def infoBarCreate(windowWidth, windowHeight):
    # Constant
    infoBarWidth = int(windowWidth)
    infoBarHeight = int(windowHeight / 3)
    infoBar = pygame.Surface((infoBarWidth, infoBarHeight))
    infoBar.fill(colours.darkGrey)
    borderLine = pygame.draw.line(infoBar, colours.white, (0, 0), (infoBarWidth, 0), 2)
    scaleLineLength = 30

    # Makes the scale
    for multiplier in range(1, int(windowWidth / 100)):
        lineXpos = infoBarWidth * multiplier / (windowWidth / 100)
        scaleLine = pygame.draw.line(infoBar, colours.white, (lineXpos, 0), (lineXpos, scaleLineLength), 2)
        measurement = (multiplier - int(windowWidth / 200)) * 10
        scaleTextBox = baseFont.render(f"{str(measurement)} m", False, colours.white)
        scaleTextBoxRect = scaleTextBox.get_rect(midtop = (lineXpos, scaleLineLength + 10))
        infoBar.blit(scaleTextBox, scaleTextBoxRect)
    

    # Text subject to change
    textOffSet = 100
    angleBox = baseFont.render(f"Firing Angle:  Degrees", True, colours.white)
    angleBoxRect = angleBox.get_rect(midtop = (infoBarWidth / 6 * 1 , 0 + textOffSet))
    infoBar.blit(angleBox, angleBoxRect)

    velocityBox = baseFont.render(f"Input Velocity: m/s", True, colours.white)
    velocityBoxRect = velocityBox.get_rect(midtop = (infoBarWidth / 6 * 3 , 0 + textOffSet))
    infoBar.blit(velocityBox, velocityBoxRect)

    maxHeightBox = baseFont.render(f"Max Height: m", True, colours.white)
    maxHeightBoxRect = maxHeightBox.get_rect(midtop = (infoBarWidth / 6 * 5 , 0 + textOffSet))
    infoBar.blit(maxHeightBox, maxHeightBoxRect)

    xRangeBox = baseFont.render(f"Horizontal Range: m", True, colours.white)
    xRangeBoxRect = xRangeBox.get_rect(midtop = (infoBarWidth / 6 * 1 , 100 + textOffSet))
    infoBar.blit(xRangeBox, xRangeBoxRect)

    hvBox = baseFont.render(f"Horizontal Velocity: m/s", True, colours.white)
    hvBoxRect = hvBox.get_rect(midtop = (infoBarWidth / 6 * 3 , 100 + textOffSet))
    infoBar.blit(hvBox, hvBoxRect)

    vvBox = baseFont.render(f"Vertical Velocity: m/s", True, colours.white)
    vvBoxRect = vvBox.get_rect(midtop = (infoBarWidth / 6 * 5 , 100 + textOffSet))
    infoBar.blit(vvBox, vvBoxRect)

    return infoBar

def courtCreate(windowWidth, windowHeight, radius,radAngle):
    lineXOffSet, lineYOffSet = angleToCircumference(mouseAngle(circleCenter), radius)
    # Court
    courtWidth = int(windowWidth)
    courtHeight = int(windowHeight * 2 / 3)
    court = pygame.Surface((courtWidth, courtHeight))
    court.fill(colours.darkDarkGrey)

    # AngleCircle
    circleSurf = pygame.Surface((radius * 4, radius * 4))
    circleSurf.fill(colours.darkDarkGrey)
    pygame.draw.circle(circleSurf, colours.white, (radius * 2, radius * 2), radius,2)
    pygame.draw.line(circleSurf, colours.white, (radius * 2,radius * 2),((radius * 2) + lineXOffSet, (radius * 2) - lineYOffSet ),2)

    # Angle text
    degAngle = math.floor(radAngle * 180 / math.pi)
    degAngleBox = baseFont.render(str(degAngle),False,colours.white)
    degAngleBoxRect = degAngleBox.get_rect(center = ((radius * 2 + lineXOffSet * 1.2), (radius * 2 - lineYOffSet * 1.2)))
    circleSurf.blit(degAngleBox, degAngleBoxRect)

    #Final Court blit
    circleSurfRect = circleSurf.get_rect(center = (courtWidth / 2, courtHeight))
    court.blit(circleSurf, (circleSurfRect))




    return court

def mouseAngle(circleCenter):
    cursorX, cursorY = pygame.mouse.get_pos()
    centerX, centerY = circleCenter
    respectiveX = cursorX - centerX
    respectiveY = centerY - cursorY

    if respectiveY < 0:
        radAngle = 0
    
    else:
        if respectiveX == 0:
            radAngle = math.pi / 2

        elif respectiveX < 0:
            radAngle = math.pi + math.atan(respectiveY / respectiveX)

        elif respectiveX > 0:
            radAngle = math.atan(respectiveY / respectiveX)

    return radAngle

def angleToCircumference(radAngle, radius):
    y = radius * math.sin(radAngle)
    x = radius * math.cos(radAngle)
    print(x,y)
    return x, y

# Framerate
frameRate = 60
clock = pygame.time.Clock()

# Stuff
colours = Colour()
windowWidth, windowHeight = 1800, 900
circleCenter = (windowWidth / 2, windowHeight * 2 / 3)
radius = 150

# Screen Setup
pygame.init()
screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Projectile Motion Sim 3")

# Font
pygame.font.init()
baseFont = pygame.font.SysFont("helvetica", 20)

# Base objects and Surfaces
callum_planet = pygame.image.load("assets/Callum.png").convert_alpha()
preston_planet = pygame.image.load("assets/Preston.png").convert_alpha()
current_planet = random.choice([callum_planet, preston_planet])

# Event Loop
while True:
    # Game ender
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    infoBar = infoBarCreate(windowWidth, windowHeight)
    court = courtCreate(windowWidth, windowHeight, radius,mouseAngle(circleCenter))

    # Blitting to screen
    
    screen.blit(infoBar, (0, windowHeight * 2 / 3))
    screen.blit(court, (0, 0))

    # Updates and tickrate
    pygame.display.update()
    clock.tick(frameRate)
