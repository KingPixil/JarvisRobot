# IMPORT ALL THE STUFF
import pigpio
import pygame
import time
import math

# Declare some variables
input_pin_1 = 22
input_pin_2 = 17
input_pin_3 = 18
input_pin_4 = 24
freq = 100
dutycycle1 = 100
dutycycle2 = 100
speed=100
accel = 10
DIFFERENCE=75
VERSION = "0.2.0"
direction = "C"
pig = pigpio.pi()
# All of the outputs
pig.set_mode(input_pin_1, pigpio.OUTPUT)
pig.set_mode(input_pin_2, pigpio.OUTPUT)
pig.set_mode(input_pin_3, pigpio.OUTPUT)
pig.set_mode(input_pin_4, pigpio.OUTPUT)
# Set all of the frequencies
pig.set_PWM_frequency(input_pin_1, freq)
pig.set_PWM_frequency(input_pin_2, freq)
pig.set_PWM_frequency(input_pin_3, freq)
pig.set_PWM_frequency(input_pin_4, freq)
# Set the dutycycles
pig.set_PWM_dutycycle(input_pin_1, dutycycle1)
pig.set_PWM_dutycycle(input_pin_2, dutycycle2)
pig.set_PWM_dutycycle(input_pin_3, dutycycle1)
pig.set_PWM_dutycycle(input_pin_4, dutycycle2)
pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE  = (39, 174, 96)
control = 0
running = True
print ("JARVIS VERSION " + VERSION + " HAS BEEN SETUP SUCCESSFULLY")
pygame.display.set_caption("JARVIS")
WINDOWWIDTH = 400
WINDOWHEIGHT = 300
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
windowSurface.fill(BLACK)
DISPLAYSURF.fill(BLACK)
fontObj = pygame.font.Font('freesansbold.ttf' , 32)
textSurfaceObj = fontObj.render(direction + " JARVIS " + str(255 - speed), True, BLUE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (200, 150)
DISPLAYSURF.blit(textSurfaceObj, textRectObj)
pygame.display.update()
try:
    while running:
        windowSurface.fill(BLACK)
        DISPLAYSURF.fill(BLACK)
        fontObj = pygame.font.Font('freesansbold.ttf' , 32)
        textSurfaceObj = fontObj.render(direction + " JARVIS " + str(255 - speed) , True, BLUE)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (200, 150)
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)
        pygame.display.update()
        pig.set_PWM_dutycycle(22, dutycycle2) 
        pig.set_PWM_dutycycle(17, dutycycle1)
        pig.set_PWM_dutycycle(18, dutycycle2)
        pig.set_PWM_dutycycle(24, dutycycle1)
        events = pygame.event.get()
        for event in events:
            # Loop For Controlling the Robot
            if (event.type == pygame.KEYDOWN):
                #print ("JARVIS RECIEVED THE COMMAND:")
                if event.key == pygame.K_SPACE:
                    # STOP JARVIS
                    direction="Q"
                elif event.key == pygame.K_c:
                    # TEMPORARILY STOP JARVIS
                    direction="C"
                elif event.key == pygame.K_r:
                    # REBOOT JARVIS
                    direction="R" 
                elif event.key == pygame.K_a and pygame.K_i:
                    direction="AI"
                elif event.key == pygame.K_o and pygame.K_p:
                    # ACTIATE SPEED MODE
                    direction="OP"
                elif event.key == pygame.K_UP:
                    # GO FORWARD
                    direction = "F"
                elif event.key == pygame.K_DOWN:
                    # GO BACKWARDS
                    direction = "B"
                elif event.key == pygame.K_z:
                    # SLOW DOWN
                    direction = "SD"
                elif event.key == pygame.K_x:
                    # SPEED UP
                    direction = "SU"
                elif event.key == pygame.K_LEFT:
                    # TURN LEFT
                    direction = "L"
                elif event.key == pygame.K_RIGHT:
                    # TURN RIGHT
                    direction = "R"
                elif event.key == pygame.K_a:
                    # DRIFT LEFT
                    direction = "DL"
                elif event.key == pygame.K_d:
                    # DRIFT RIGHT
                    direction = "DR"


            # DETECTING DIRECTION AND TAKE ACTION
            if direction=="Q":
                #print ("STOPPING JARVIS")
                pig.write(input_pin_1, pigpio.LOW)
                pig.write(input_pin_2, pigpio.LOW)
                pig.write(input_pin_3, pigpio.LOW)
                pig.write(input_pin_4, pigpio.LOW)
                running = False
            if direction=="C":
                #print ("CUTTING JARVIS MOTORS")
                pig.write(input_pin_1, pigpio.LOW)
                pig.write(input_pin_2, pigpio.LOW)
                pig.write(input_pin_3, pigpio.LOW)
                pig.write(input_pin_4, pigpio.LOW)
            if direction=="OP":
                #print ("JARVIS IS GOING INTO OP MODE")
                pig.write(input_pin_1, pigpio.HIGH)
                pig.write(input_pin_2, pigpio.HIGH)
                pig.write(input_pin_3, pigpio.HIGH)
                pig.write(input_pin_4, pigpio.HIGH)
                speed = 255
                dutycycle1 = 255
                dutycycle2 = 255
            if direction=="F":
                if speed < 256:
                    dutycycle2=0
                    pig.write(input_pin_1, pigpio.HIGH)
                    pig.write(input_pin_2, pigpio.HIGH)
                    pig.write(input_pin_3, pigpio.HIGH)
                    pig.write(input_pin_4, pigpio.HIGH)
                    control=0
                    dutycycle1=speed
                    #print("JARVIS IS GOING FORWARDS")                  
            elif direction=="B":
                if speed > 0:
                    pig.write(input_pin_1, pigpio.HIGH)
                    pig.write(input_pin_2, pigpio.HIGH)
                    pig.write(input_pin_3, pigpio.HIGH)
                    pig.write(input_pin_4, pigpio.HIGH)
                    dutycycle1=0
                    control=1
                    dutycycle2=speed
                    #print ("JARVIS IS GOING BACKWARDS")
            elif direction=="SU":
                if speed < 256:
                    if dutycycle1 > 11 and control == 0:
                        speed -= accel
                        dutycycle1 = speed
                    if dutycycle2 > 11 and control == 1:
                        speed -= accel
                        dutycycle2 = speed
                #print ("JARVIS IS SPEEDING UP")
            elif direction=="SD":
                if speed > 0:
                    if dutycycle1 < 244 and control == 0:
                        speed += accel
                        dutycycle1 = speed
                    if dutycycle2 < 244 and control == 1:
                        speed += accel
                        dutycycle2 = speed
                #print ("JARVIS IS SLOWING DOWN")
            elif direction=="L":
                pig.write(input_pin_1, pigpio.HIGH)
                pig.write(input_pin_2, pigpio.HIGH)
                pig.write(input_pin_3, pigpio.LOW)
                pig.write(input_pin_4, pigpio.LOW)
                control=0
                #print ("JARVIS IS TURNING LEFT")
            elif direction=="R":
                pig.write(input_pin_1, pigpio.LOW)
                pig.write(input_pin_2, pigpio.LOW)
                pig.write(input_pin_3, pigpio.HIGH)
                pig.write(input_pin_4, pigpio.HIGH)
                control=0
                #print ("JARVIS IS TURNING RIGHT")
            elif direction=="DL":
                if dutycycle1 < 244:
                    dutycycle2=0
                    pig.write(input_pin_1, pigpio.HIGH)
                    pig.write(input_pin_2, pigpio.HIGH)
                    pig.write(input_pin_3, pigpio.HIGH)
                    pig.write(input_pin_4, pigpio.HIGH)
                    control=0
                    dutycycle1=speed - DIFFERENCE
            elif direction=="DR":
                if dutycycle1 < 244:
                    dutycycle2=0
                    pig.write(input_pin_1, pigpio.HIGH)
                    pig.write(input_pin_2, pigpio.HIGH)
                    pig.write(input_pin_3, pigpio.HIGH)
                    pig.write(input_pin_4, pigpio.HIGH)
                    control=0
                    dutycycle1=speed + DIFFERENCE
except KeyboardInterrupt:
    print("Quit")
    pig.stop()

# CHANGELOG
"""
    0.1.0
        Initial Version, Robot can do basic commands
        Such as Forward, Backward, Left, Right, Drift Left, Drift Right
        Temporarily Stop, and stop
    0.1.1
        A couple of bug fixes:
            * Check Speed Every Time in Loop to prevent Max/Min Speed
            * Attempted to fix Drifting
            * Added Accelaration to make more realistic
            * Changed dutycycle1/2 to speed variable for efficiency
    0.1.2
        More bug fixes
            * Add Optional Acceleration
            * Add OP Mode ALPHA

    0.2.0
        Take Out Enable Pins
            * Enable Pin's are not Needed
            * C Toggles instead of temporarily stopping
            * Add GUI
            * Remove Checkspeed (Doesn't Work)
"""
