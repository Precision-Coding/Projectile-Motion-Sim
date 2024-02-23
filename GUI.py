import math
import pygame
from ColourBank import Colour
from physics import physics_sim  # Importing physics simulation function

pygame.init()

# Variables and functions:
myText = pygame.font.SysFont('helvetica', 25)
running = True
lastX = 0
lastY = 0
lastAngle = 0
pulling = False
totalVelocity = 0
circleRadius = 200
oldRadius = circleRadius

# Base shapes and screen setup
screen = pygame.display.set_mode([1000, 600])
pygame.draw.circle(screen, Colour.white, (0, 600), circleRadius)
pygame.draw.circle(screen, Colour.black, (0, 600), circleRadius - 2)

# Event loop
while running:

    # Allows quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Angle line
    x, y = pygame.mouse.get_pos()
    if abs(x - lastX) > 2 or abs(x - lastX) < -2 and x != 0:
        angle = math.atan((600 - y) / x)

        # Draws line only to the circle edge
        newX = 0 + (circleRadius * math.cos(math.atan((600 - y) / x))) - 2
        newY = 600 - (circleRadius * math.sin(math.atan((600 - y) / x))) + 2
        pygame.draw.circle(screen, Colour.black, (0, 600), oldRadius)
        pygame.draw.circle(screen, Colour.white, (0, 600), circleRadius)
        pygame.draw.circle(screen, Colour.black, (0, 600), circleRadius - 2)
        pygame.draw.line(screen, Colour.white, (0, 600), (newX, newY), 4)
        oldRadius = circleRadius

        # Adds angle text
        angle = angle * 180 / math.pi
        angle = math.floor(angle)
        textSurface = myText.render(str(lastAngle), False, Colour.black)
        screen.blit(textSurface, (lastX * 1.05, lastY * 1.05 - 60))

        textSurface = myText.render(str(angle), False, Colour.white)
        screen.blit(textSurface, (newX * 1.05, newY * 1.05 - 60))

        lastX = newX
        lastY = newY
        lastAngle = angle

    # Velocity input based on pull
    if pygame.mouse.get_pressed(num_buttons=3) == (True, False, False) and not pulling:
        startX, startY = pygame.mouse.get_pos()
        pulling = True

    elif pygame.mouse.get_pressed(num_buttons=3) == (True, False, False) and pulling:
        endX, endY = pygame.mouse.get_pos()
        xMovement = startX - endX
        yMovement = startY - endY
        totalVelocity = math.sqrt((xMovement ** 2) + (yMovement ** 2))
        circleRadius = 200 / ((totalVelocity / 200) + 1)

    elif pygame.mouse.get_pressed(num_buttons=3) == (False, False, False) and pulling:
        circleRadius = 200
        pulling = False
        print(totalVelocity)

    # Updates screen
    pygame.display.flip()

pygame.quit()