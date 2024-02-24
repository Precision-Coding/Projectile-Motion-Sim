import pygame
from sys import exit
from colourBank import Colour
from physics import physics_sim
import math
import random


colours = Colour()

# Functions
def angleCalculator(circleCentre):
    """
    Calculates the angle between the mouse position and the circle centre.

    Parameters:
    circleCentre (tuple): The coordinates of the circle centre.

    Returns:
    float: The angle in radians.
    """
    x, y = pygame.mouse.get_pos()
    centreX, centreY = circleCentre
    x -= centreX
    y = centreY - y

    if x != 0:
        radAngle = math.atan(y/x)

    else:
        radAngle = math.pi / 2

    return radAngle

def radiansToDegrees(radianAngle):
    return radianAngle * 180 / math.pi

def angledLineMeetsCircle(radianAngle, radius):
    x = radius * math.cos(radianAngle)
    y = radius * math.sin(radianAngle)

    if radianAngle >= 0:
        return x, -y
    else:
        return -x, y


# Framerate
frameRate = 60
clock = pygame.time.Clock()

# Stuff
windowWidth, windowHeight = 1800, 900
radius = 150
circleCentre = windowWidth / 2, windowHeight / 3 * 2
mouseX1, mouseY1 = 0, 0
firing = False
inputVelocity = 0
xRange = 0
maxHeight = 0
horizontalVelocity = 0
verticalVelocity = 0
ballInit = False
shooting = False


# Screen Setup
pygame.init()
screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Projectile Motion Sim 2.0")

# Font
pygame.font.init()
baseFont = pygame.font.SysFont("helvetica", 20)

# Base objects and Surfaces
callum_planet = pygame.image.load("assets/Callum.png")
preston_planet = pygame.image.load("assets/Preston.png")
current_planet = random.choice([callum_planet, preston_planet])


def baseTextBar():
    textBar = pygame.Surface((windowWidth, windowHeight / 3))
    textBar.fill(colours.darkGrey)
    pygame.draw.line(textBar, colours.white, (0, 0, ), (windowWidth, 0), 2)
    return textBar


def baseCircleCourt():
    circleCourt = pygame.Surface((windowWidth, windowHeight / 3 * 2))
    pygame.draw.circle(circleCourt, colours.white, (circleCentre), radius, 2)
    return circleCourt


def baseBallCourt():
    ballCourt = pygame.Surface((windowWidth, windowHeight / 3 * 2))
    return ballCourt


ballYCutoff = 600

# Event Loop
while True:
    circleX, circleY = circleCentre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # background_color = colours.green  # Green background
    # screen.fill(background_color)

    # Text Bar Changes
    textBar = baseTextBar()
    if firing is not True:
        degreesAngle = math.floor(radiansToDegrees(angleCalculator(circleCentre)))

    angleBox = baseFont.render(f"Firing Angle: {str(degreesAngle)} Degrees", True, colours.white)
    textBar.blit(angleBox, (175, 0))

    velocityBox = baseFont.render(f"Input Velocity: {str(math.floor(inputVelocity))} m/s", True, colours.white)
    textBar.blit(velocityBox, (windowWidth / 4 * 1 + 175, 0))

    maxHeightBox = baseFont.render(f"Max Height: {str(math.floor(maxHeight))} m", True, colours.white)
    textBar.blit(maxHeightBox, (windowWidth / 4 * 2 + 175, 0))

    xRangeBox = baseFont.render(f"Horizontal Range: {str(math.floor(math.sqrt(math.pow(xRange, 2))))} m", True, colours.white)
    textBar.blit(xRangeBox, (windowWidth / 4 * 3 + 175, 0))

    horizontalVelocityBox = baseFont.render(f"Horizontal Velocity: {str(math.floor(math.sqrt(math.pow(horizontalVelocity, 2))))} m/s", True, colours.white)
    textBar.blit(horizontalVelocityBox, (windowWidth / 4 * 0 + 175, 100))

    verticalVelocityBox = baseFont.render(f"Vertical Velocity: {str(math.floor(math.sqrt(math.pow(verticalVelocity, 2))))} m/s", True, colours.white)
    textBar.blit(verticalVelocityBox, (windowWidth / 4 * 1 + 175, 100))

    screen.blit(textBar, (0, (windowHeight * 2 / 3)))

    # Circle Changes

    # Line
    circleCourt = baseCircleCourt()
    x, y = angledLineMeetsCircle(degreesAngle/ 180 * math.pi, radius)
    x, y = x + circleX, y + circleY
    pygame.draw.line(circleCourt, colours.white, circleCentre, (x, y), 3)

    # AngleText
    x, y = angledLineMeetsCircle(degreesAngle / 180 * math.pi, radius * 1.25)
    x, y = x + circleX, y + circleY
    angleBox = baseFont.render(str(degreesAngle), True, colours.white)
    circleCourt.blit(angleBox, (x, y))

    # Click and pull response
    if pygame.mouse.get_pressed() == (True, False, False) and not firing:
        mouseX1, mouseY1 = pygame.mouse.get_pos()
        firing = True

    if pygame.mouse.get_pressed() == (False, False, False) and firing:
        mouseX2, mouseY2 = pygame.mouse.get_pos()
        radius = 150
        ballVelocity = inputVelocity
        ballAngle = angle
        firing = False
        ballInit = True
        current_planet = random.choice([callum_planet, preston_planet])  # Selecting a random planet when firing

    if pygame.mouse.get_pressed() == (True, False, False):
        mouseX2, mouseY2 = pygame.mouse.get_pos()
        xMove, yMove = mouseX1 - mouseX2, mouseY1 - mouseY2
        inputVelocity = math.sqrt((xMove ** 2) + (yMove ** 2)) / 5 
        radius = (150 / (inputVelocity/150 + 1))
        xRange, maxHeight = physics_sim(inputVelocity, degreesAngle)

    # ARC drawing
    x, y = circleCentre

    angle = degreesAngle/ 180 * math.pi

    if angle >= 0:
        verticalVelocity = inputVelocity * math.sin(degreesAngle/ 180 * math.pi)
        horizontalVelocity = inputVelocity * math.cos(degreesAngle/ 180 * math.pi)

    elif angle < 0:
        verticalVelocity = -1 * inputVelocity * math.sin(degreesAngle/ 180 * math.pi)
        horizontalVelocity = -1 * inputVelocity * math.cos(degreesAngle/ 180 * math.pi)

    arcVerticalVelocity = verticalVelocity
    arcHorizontalVelocity = horizontalVelocity

    while (arcHorizontalVelocity > 0.1 or arcHorizontalVelocity < -0.1):
        pygame.draw.circle(circleCourt, colours.white, (x, y), 2)
        arcVerticalVelocity -= 9.81
        x += arcHorizontalVelocity
        y -= arcVerticalVelocity

        if y > ballYCutoff:
            y = ballYCutoff - 1
            arcVerticalVelocity = arcVerticalVelocity * -0.5
            arcHorizontalVelocity = arcHorizontalVelocity * 0.8

    # Ball initialiser
    if ballInit is True:
        ballVerticalVelocity = verticalVelocity / math.sqrt(frameRate) 
        ballHorizontalVelocity = horizontalVelocity / math.sqrt(frameRate)
        gravity = (9.81) / frameRate
        ballX = circleX
        ballY = circleY
        shooting = True
        ballInit = False

    # Makes the ball move
    if shooting is True:
        if ballHorizontalVelocity > 0.01 or ballHorizontalVelocity < -0.01:
            current_planet = pygame.transform.scale(current_planet, (24, 24))
            circleCourt.blit(current_planet, (ballX - 24, ballY - 24))
            ballVerticalVelocity -= gravity
            ballX += ballHorizontalVelocity
            ballY -= ballVerticalVelocity
            if ballY > ballYCutoff:
                ballY = ballYCutoff - 1
                ballVerticalVelocity = ballVerticalVelocity * -0.5
                ballHorizontalVelocity = ballHorizontalVelocity * 0.8
    else:
        shooting = False

    # Blitting to screen
    screen.blit(circleCourt, (0, 0))

    # Updates and tickrate
    pygame.display.update()
    clock.tick(frameRate)
