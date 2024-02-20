#Mostly messing around with Pygame
import math
import pygame
from ColourBank import Colour
import random

pygame.init()

#Funtions and Variables
myText = pygame.font.SysFont('helvetica', 30)
circleRadius = 50


def angleCalculator(x,y):
    import math
    if x != 0:
        angle = math.atan((y/x)) * 180/math.pi
        return angle
    else:
        return 90

#Base shapes and screen setup
screen = pygame.display.set_mode([400, 600])
pygame.draw.circle(screen,(Colour().white),(0,600),circleRadius)
pygame.draw.circle(screen,(Colour().black),(0,600),circleRadius - 2)


#Event loop
running = True
lastX = 0
lastY = 0
lastAngle = 0

while running:

    #Allows quiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Angle line
    x,y = pygame.mouse.get_pos()
    if x - lastX > 2 or x -lastX < -2 and x != 0:
        angle = math.atan((600 - y)/x)

        #Draws line only to the circle edge
        newX = 0 + (circleRadius * math.cos(math.atan((600 - y)/x))) - 2
        newY = 600 - (circleRadius * math.sin(math.atan((600 - y)/x))) + 2
        pygame.draw.circle(screen,(Colour().white),(0,600),circleRadius)
        pygame.draw.circle(screen,(Colour().black),(0,600),circleRadius - 2)
        pygame.draw.line(screen,(Colour().white),(0,600),(newX,newY),4)

        #Adds angle text
        angle = angle * 180 / math.pi
        angle = math.floor(angle)
        textSurface = myText.render(str(lastAngle),False,Colour().black)
        screen.blit(textSurface, (lastX + 25, lastY - 25))

        textSurface = myText.render(str(angle),False,Colour().white)
        screen.blit(textSurface, (newX + 25, newY - 25))
        
        lastX = newX
        lastY = newY
        lastAngle = angle

    pygame.display.flip()

pygame.quit()
