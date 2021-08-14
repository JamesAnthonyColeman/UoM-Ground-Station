# This program will include the pygame run sequence and host the dials.
# Program will also handle data from logs

# Importing
import csv
import math
import pygame
import pandas as pd
from Dials import airspeed_indicator
from Dials import artificial_horizon
from Dials import altimeter
from Dials import compass
from dronekit import connect, VehicleMode
import time

pygame.init()

# Establishing a connection
vehicle = connect('com7', wait_ready=True, baud=9600)
print("Connecting to vehicle")

# Variables
WIDTH, HEIGHT = 900, 600
FPS = 60
clock = pygame.time.Clock()

# Main surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ground control")

# Define images for background and size
bg = pygame.image.load('Assets/grey.png').convert_alpha()
bg = pygame.transform.scale(bg, (int(WIDTH), int(HEIGHT)))


# Program loop
run = True
while run:
    clock.tick(FPS)
    screen.blit(bg, (0,0))

    # Get vehicle attributes
    # For now the attribute will be pitch in degrees
    data = math.degrees(vehicle.attitude.pitch)

    # Dials defined
    airspeed_dial = airspeed_indicator.Airspeed( 0, 0, 1, data, 0.4, -5, 0.185,0.125)
    horizon = artificial_horizon.Horizon(103,0)
    altimeter_dial = altimeter.Altitude(402, 0, data)
    compass_dial = compass.Compass(103, 300, 1, data)
    
    # Used for locating things on the page
    #pos = pygame.mouse.get_pos() 
    #print(pos)

    # Draw dials
    airspeed_dial.draw(screen)
    horizon.update(screen,10 , 10)
    altimeter_dial.draw(screen)
    compass_dial.draw(screen)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

vehicle.close()
pygame.quit()

