# IMPORT ALL THE STUFF
import pigpio
import pygame
import time
import math
# Declare some variables
enable_pin = 4
enable_pin_2 = 23
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
pig.set_mode(enable_pin, pigpio.OUTPUT)
pig.set_mode(enable_pin_2, pigpio.OUTPUT)
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
pygame.display.set_mode((300, 200))
control = 0
running = True
print ("JARVIS VERSION " + VERSION + " HAS BEEN SETUP SUCCESSFULLY")
try:
    def checkSpeed(speed):
        if speed >= 255:
            print ("WARNING: JARVIS HAS REACHED MAX SPEED")
            speed = 255
            return 255
        elif speed <= 0:
            print ("WARNING: JARVIS IS AT MINIMUM SPEED")
            speed = 0
            return 0
        else:
            return speed
    while running:
        checkSpeed(speed)
        pig.set_PWM_dutycycle(22, dutycycle2) 
        pig.set_PWM_dutycycle(17, dutycycle1)
        pig.set_PWM_dutycycle(18, dutycycle2)
        pig.set_PWM_dutycycle(24, dutycycle1)
        events = pygame.event.get()
        for event in events:
            # Loop For Controlling the Robot
            if (event.type == pygame.KEYDOWN):
                print ("JARVIS RECIEVED THE COMMAND:")
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
                    checkSpeed(speed)
                elif event.key == pygame.K_DOWN:
                    # GO BACKWARDS
                    direction = "B"
                    checkSpeed(speed)
                elif event.key == pygame.K_z:
                    # SLOW DOWN
                    direction = "SD"
                    checkSpeed(speed)
                elif event.key == pygame.K_x:
                    # SPEED UP
                    direction = "SU"
                    checkSpeed(speed)
                elif event.key == pygame.K_LEFT:
                    # TURN LEFT
                    direction = "L"
                    checkSpeed(speed)
                elif event.key == pygame.K_RIGHT:
                    # TURN RIGHT
                    direction = "R"
                    checkSpeed(speed)
                elif event.key == pygame.K_a:
                    # DRIFT LEFT
                    direction = "DL"
                    checkSpeed(speed)
                elif event.key == pygame.K_d:
                    # DRIFT RIGHT
                    checkSpeed(speed)
                    direction = "DR"


            # DETECTING DIRECTION AND TAKE ACTION
            if direction=="Q":
                print ("STOPPING JARVIS")
                pig.write(input_pin_1, pigpio.LOW)
                pig.write(input_pin_2, pigpio.LOW)
                pig.write(input_pin_3, pigpio.LOW)
                pig.write(input_pin_4, pigpio.LOW)
                running = False
            if direction=="C":
                print ("CUTTING JARVIS MOTORS")
                pig.write(input_pin_1, pigpio.LOW)
                pig.write(input_pin_2, pigpio.LOW)
                pig.write(input_pin_3, pigpio.LOW)
                pig.write(input_pin_4, pigpio.LOW)
            if direction=="R":
                print ("REBOOTING JARVIS")
                pig.write(input_pin_1, pigpio.HIGH)
                pig.write(input_pin_2, pigpio.HIGH)
                pig.write(input_pin_3, pigpio.HIGH)
                pig.write(input_pin_4, pigpio.HIGH)
                running = True
            if direction=="OP":
                print ("JARVIS IS GOING INTO OP MODE")
                pig.write(input_pin_1, pigpio.HIGH)
                pig.write(input_pin_2, pigpio.HIGH)
                pig.write(input_pin_3, pigpio.HIGH)
                pig.write(input_pin_4, pigpio.HIGH)
                speed = 253
                checkSpeed(speed)
            if direction=="F":
                if speed < 255:
                    accel += 1
                    dutycycle2=0
                    pig.write(input_pin_1, pigpio.HIGH)
                    pig.write(input_pin_2, pigpio.HIGH)
                    pig.write(input_pin_3, pigpio.HIGH)
                    pig.write(input_pin_4, pigpio.HIGH)
                    control=0
                    dutycycle1=speed
                    checkSpeed(speed)
                    print("JARVIS IS GOING FORWARDS")                  
            elif direction=="B":
                if speed > 0:
                    accel -= 1
                    pig.write(input_pin_1, pigpio.HIGH)
                    pig.write(input_pin_2, pigpio.HIGH)
                    pig.write(input_pin_3, pigpio.HIGH)
                    pig.write(input_pin_4, pigpio.HIGH)
                    dutycycle1=0
                    control=1
                    dutycycle2=speed
                    checkSpeed(speed)
                    print ("JARVIS IS GOING BACKWARDS")
            elif direction=="SU":
                if dutycycle1 > 11 and control == 0:
                    speed -= accel
                    dutycycle1 = speed
                if dutycycle2 > 11 and control == 1:
                    speed -= accel
                    dutycycle2 = speed
                checkSpeed(speed)
                print ("JARVIS IS SPEEDING UP")
            elif direction=="SD":
                if dutycycle1 < 244 and control == 0:
                    speed += accel
                    dutycycle1 = speed
                if dutycycle2 < 244 and control == 1:
                    speed += accel
                    dutycycle2 = speed
                checkSpeed(speed)
                print ("JARVIS IS SLOWING DOWN")
            elif direction=="L":
                pig.write(input_pin_1, pigpio.HIGH)
                pig.write(input_pin_2, pigpio.HIGH)
                pig.write(input_pin_3, pigpio.LOW)
                pig.write(input_pin_4, pigpio.LOW)
                control=0
                checkSpeed(speed)
                print ("JARVIS IS TURNING LEFT")
            elif direction=="R":
                pig.write(input_pin_1, pigpio.LOW)
                pig.write(input_pin_2, pigpio.LOW)
                pig.write(input_pin_3, pigpio.HIGH)
                pig.write(input_pin_4, pigpio.HIGH)
                control=0
                print ("JARVIS IS TURNING RIGHT")
            elif direction=="DL":
                if dutycycle1 < 244:
                    dutycycle2=0
                    pig.write(input_pin_1, pigpio.HIGH)
                    pig.write(input_pin_2, pigpio.HIGH)
                    pig.write(input_pin_3, pigpio.HIGH)
                    pig.write(input_pin_4, pigpio.HIGH)
                    control=0
                    dutycycle1=speed - DIFFERENCE
                else:
                    checkSpeed(speed)
                print ("JARVIS IS DRIFTING LEFT")
            elif direction=="DR":
                if dutycycle1 < 244:
                    dutycycle2=0
                    pig.write(input_pin_1, pigpio.HIGH)
                    pig.write(input_pin_2, pigpio.HIGH)
                    pig.write(input_pin_3, pigpio.HIGH)
                    pig.write(input_pin_4, pigpio.HIGH)
                    control=0
                    dutycycle1=speed + DIFFERENCE
                else:
                    checkSpeed(speed)
                print ("JARVIS IS DRIFTING RIGHT")
except KeyboardInterrupt:
    print("Quit")
    pig.write(enable_pin, pigpio.LOW)
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
"""
