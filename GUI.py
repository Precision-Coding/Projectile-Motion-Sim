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

def physics_sim(velocity, angle):
    """
    Simulates projectile motion given initial velocity and launch angle.
    
    Parameters:
        velocity (float): Initial velocity of the projectile.
        angle (float): Launch angle of the projectile in degrees.
        
    Returns:
        tuple: Tuple containing the horizontal range and maximum height of the projectile.
    """
    # Convert angle from degrees to radians
    angle_rad = math.radians(angle)
    
    # Calculate horizontal and vertical components of velocity
    x_velocity = velocity * math.cos(angle_rad)
    y_velocity = velocity * math.sin(angle_rad)
    
    # Calculate time of flight
    time_of_flight = (2 * y_velocity) / 9.81
    
    # Calculate horizontal range
    horizontal_range =  x_velocity * time_of_flight
    
    # Calculate maximum height
    max_height = (y_velocity ** 2) / (2 * 9.81)
    
    return horizontal_range, max_height

#Framerate
frameRate = 144
clock = pygame.time.Clock()

#Stuff
windowWidth,windowHeight = 1800,900
radius = 150
circleCentre = windowWidth / 2,windowHeight / 3 * 2
mouseX1,mouseY1 = 0,0
firing = False
inputVelocity = 100
xRange = 0
maxHeight = 0
horizontalVelocity = 0
verticalVelocity = 0
ballInit = False
shooting = False


#Screen Setup
pygame.init()
screen = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption("Projectile Motion Sim 2.0")

#Font
pygame.font.init()
baseFont = pygame.font.SysFont("helvetica",20)

#Base objects and Surfaces

prestonPlanet2 = pygame.image.load("Pesot2.png")

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
    return ballCourt

#Event Loop
while True:
    circleX,circleY = circleCentre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit()

    #Text Bar Changes
    textBar = baseTextBar()
    if firing is not True:
        degreesAngle = math.floor(radiansToDegrees(angleCalculator(circleCentre)))

    angleBox = baseFont.render(f"Firing Angle: {str(degreesAngle)}",True,Colour().white)
    textBar.blit(angleBox,(175,0))

    velocityBox = baseFont.render(f"Input Velocity: {str(math.floor(inputVelocity))}",True,Colour().white)
    textBar.blit(velocityBox,(windowWidth / 4 * 1 + 175,0))
    
    maxHeightBox = baseFont.render(f"Max Height: {str(math.floor(maxHeight))}",True,Colour().white)
    textBar.blit(maxHeightBox,(windowWidth / 4 * 2 + 175,0))

    xRangeBox = baseFont.render(f"Horizontal Range: {str(math.floor(xRange))}",True,Colour().white)
    textBar.blit(xRangeBox,(windowWidth / 4 * 3 + 175,0))

    horizontalVelocityBox = baseFont.render(f"Horizontal Velocity: {str(math.floor(horizontalVelocity))}",True,Colour().white)
    textBar.blit(horizontalVelocityBox,(windowWidth / 4 * 0 + 175,100))

    verticalVelocityBox = baseFont.render(f"Vertical Velocity: {str(math.floor(verticalVelocity))}",True,Colour().white)
    textBar.blit(verticalVelocityBox,(windowWidth / 4 * 1 + 175,100))

    #Circle Changes

    #Line
    circleCourt = baseCircleCourt()
    x,y = angledLineMeetsCircle(degreesAngle/ 180 * math.pi,radius)
    x,y = x + circleX, y + circleY 
    pygame.draw.line(circleCourt,Colour().white,circleCentre,(x,y),3)

    #AngleText
    x,y = angledLineMeetsCircle(degreesAngle/ 180 * math.pi,radius * 1.25)
    x,y = x + circleX, y + circleY 
    angleBox = baseFont.render(str(degreesAngle),True,Colour().white)
    circleCourt.blit(angleBox,(x,y))

    #Click and pull response
        

    if pygame.mouse.get_pressed() == (True,False,False) and not firing:
        mouseX1,mouseY1 = pygame.mouse.get_pos()
        firing = True

    if pygame.mouse.get_pressed() == (False,False,False) and firing:
        mouseX2,mouseY2 = pygame.mouse.get_pos()
        radius = 150
        ballVelocity = inputVelocity
        ballAngle = angle
        firing = False
        ballInit = True

    if pygame.mouse.get_pressed() == (True,False,False):
        mouseX2,mouseY2 = pygame.mouse.get_pos()
        xMove,yMove = mouseX1 - mouseX2, mouseY1 - mouseY2
        inputVelocity = math.sqrt((xMove ** 2) + (yMove ** 2)) / 5
        radius = (150 / (inputVelocity/100 + 1))
        xRange,maxHeight = physics_sim(inputVelocity, degreesAngle)
    
    #ARC drawing
    x,y = circleCentre
    
    angle = degreesAngle/ 180 * math.pi

    if angle >= 0:
        verticalVelocity = inputVelocity * math.sin(degreesAngle/ 180 * math.pi)
        horizontalVelocity = inputVelocity * math.cos(degreesAngle/ 180 * math.pi)

    elif angle < 0:
        verticalVelocity = -1 * inputVelocity * math.sin(degreesAngle/ 180 * math.pi)
        horizontalVelocity = -1 * inputVelocity * math.cos(degreesAngle/ 180 * math.pi)  

    arcVerticalVelocity = verticalVelocity 
    arcHorizontalVelocity = horizontalVelocity

    while (arcHorizontalVelocity > 1 or arcHorizontalVelocity < -1):
        pygame.draw.circle(circleCourt,Colour().white,(x,y),2)
        arcVerticalVelocity -= 9.81
        x += arcHorizontalVelocity
        y -= arcVerticalVelocity
        

        if y > 600:
            y = 599
            arcVerticalVelocity = arcVerticalVelocity * -0.5
            arcHorizontalVelocity = arcHorizontalVelocity * 0.8


    

    if ballInit is True:
        ballVerticalVelocity = verticalVelocity / 10
        ballHorizontalVelocity = horizontalVelocity / 10
        gravity = 9.81 / 100
        ballX = circleX
        ballY = circleY
        shooting = True
        ballInit = False
        

    if shooting is True:
        if ballHorizontalVelocity > 0.5 or ballHorizontalVelocity < -0.5:
            prestonPlanet2 = pygame.transform.scale(prestonPlanet2,(75,75))
            circleCourt.blit(prestonPlanet2,(ballX,ballY))
            ballVerticalVelocity -= gravity 
            ballX += ballHorizontalVelocity
            ballY -= ballVerticalVelocity
            

            if ballY > 600:
                ballY = 599
                ballVerticalVelocity = ballVerticalVelocity * -0.5
                ballHorizontalVelocity = ballHorizontalVelocity * 0.8
    else:
        shooting = False

    #Blitting to screen
    screen.blit(textBar,(0,windowHeight / 3 * 2))
    screen.blit(circleCourt,(0,0))
    

    #Updates and tickrate
    pygame.display.update()
    clock.tick(frameRate)