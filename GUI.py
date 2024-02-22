#Mostly messing around with Pygame
import math
import pygame
from ColourBank import Colour
import time

pygame.init()

#Variables and functions:
angleText = pygame.font.SysFont('helvetica', 25)
normalText = pygame.font.SysFont('helvetica', 15)
running = True
lastX = 0
lastY = 0
lastAngle = 0
pulling = False
totalVelocity = 0
circleRadius = 200
oldRadius = circleRadius
lastTotalVelocity = 0
firing = False

#Base shapes and screen setup
screen = pygame.display.set_mode([1000, 600])
pygame.draw.circle(screen,(Colour().white),(0,600),circleRadius)
pygame.draw.circle(screen,(Colour().black),(0,600),circleRadius - 2)


#Event loop
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
        pygame.draw.circle(screen,(Colour().black),(0,600),oldRadius)
        pygame.draw.circle(screen,(Colour().white),(0,600),circleRadius)
        pygame.draw.circle(screen,(Colour().black),(0,600),circleRadius - 2)
        pygame.draw.line(screen,(Colour().white),(0,600),(newX,newY),4)
        oldRadius = circleRadius

        #Adds angle text
        angle = angle * 180 / math.pi
        angle = math.floor(angle)
        textSurface = angleText.render(str(lastAngle),False,Colour().black)
        screen.blit(textSurface, (lastX * 1.05, lastY * 1.05 -60))

        textSurface = angleText.render(str(angle),False,Colour().white)
        screen.blit(textSurface, (newX * 1.05, newY * 1.05 - 60 ))
        
        lastX = newX
        lastY = newY
        lastAngle = angle

    #Velocity input based on pull and circle resizing
    if pygame.mouse.get_pressed(num_buttons = 3) == (True,False,False) and pulling is False:
        startX, startY = pygame.mouse.get_pos()
        pulling = True

    elif pygame.mouse.get_pressed(num_buttons = 3) == (True,False,False) and pulling is True:
        endX, endY = pygame.mouse.get_pos()
        horizontalVelocity = startX - endX
        verticalVelocity = startY - endY
        totalVelocity = math.sqrt((horizontalVelocity**2) + (verticalVelocity**2))
        circleRadius = 200 / ((totalVelocity/200) + 1)

        #Adds text
        textSurface = normalText.render(str(f"Input Velocity: {lastTotalVelocity}"),False,Colour().black)
        screen.blit(textSurface, (0,0))

        textSurface = normalText.render(str(f"Input Velocity: {totalVelocity}"),False,Colour().white)
        screen.blit(textSurface, (0,0))
        lastTotalVelocity = totalVelocity

    elif pygame.mouse.get_pressed(num_buttons = 3) == (False,False,False) and pulling is True:
        circleRadius = 200
        pulling = False
        firing = True
        ballColour = Colour().randomiser()
        ballX,ballY = 0,600
    
    if firing is True:

        time.sleep(0.001)
        pygame.draw.circle(screen,Colour().black,(ballX,ballY),15)
        pygame.draw.circle(screen,ballColour,(ballX,ballY),2)
        ballX = ballX + horizontalVelocity / 100
        ballY = ballY + verticalVelocity / 100
        verticalVelocity = verticalVelocity + (9.8 / 20)
        pygame.draw.circle(screen,ballColour,(ballX,ballY),15)

        if ballY > 600:
            verticalVelocity = (verticalVelocity * 0.6) * -1 
            ballY = 599
            horizontalVelocity = horizontalVelocity * 0.8
        
        elif ballY < 0:
            verticalVelocity = (verticalVelocity * 0.6) * -1 
            ballY = 1
            horizontalVelocity = horizontalVelocity * 0.8
            

        elif ballX > 1000:
            horizontalVelocity = (horizontalVelocity * 0.6) * -1
            ballX = 999

        elif ballX < 0:
            horizontalVelocity = (horizontalVelocity * 0.6) * -1
            ballX = 1

        if math.floor(horizontalVelocity) < 3 and math.floor(horizontalVelocity) > -3:
            firing = False
            pygame.draw.rect(screen,Colour().black,(0,0,1000,600))


    pygame.display.flip()

pygame.quit()

