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
from Dials import grapher
from dronekit import connect, VehicleMode
import time
import datetime

# Begin script
pygame.init()
Launch_time = datetime.datetime.now() # Date for starting the scrip. Used for data collection

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





# Main screen
#Should be of the dials that we have done as far and maby some more info/dials
def Main():
    run = True
    while run:
        # Get vehicle attributes
        # For now the attribute will be pitch in degrees
        data = math.degrees(vehicle.attitude.pitch)

        # Dials defined
        airspeed_dial = airspeed_indicator.Airspeed( 0, 0, 1, data, 0.4, -5, 0.185,0.125)
        horizon = artificial_horizon.Horizon(103,0)
        altimeter_dial = altimeter.Altitude(402, 0, data)
        compass_dial = compass.Compass(103, 300, 1, data)
        Graph = grapher.Graph(703, 0, 2, 2, data, Launch_time)
        
        # Used for locating things on the page
        #pos = pygame.mouse.get_pos() 
        #print(pos)

        # Draw dials

        compass_dial.draw(screen)
        Graph.draw(screen)
        airspeed_dial.draw(screen)
        horizon.update(screen,10 , 10)
        altimeter_dial.draw(screen)
        
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            else:
                pygame.display.update()







# Program loop
run = True
while run:
    clock.tick(FPS)
    screen.blit(bg, (0,0))

    Main()

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

vehicle.close()
pygame.quit()

# Different windows are written as functions here

# Front screen
#Should include window resize, connect to mavlink, connection to different screen. by Esc key




#Graphing monitor page 1
#Should have a few graphs at a time taking in data.data

