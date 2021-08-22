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
#vehicle = connect('com7', wait_ready=True, baud=9600)
#print("Connecting to vehicle")

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
frontpic = pygame.image.load('Assets/CS_15.jpg').convert_alpha()
#frontpic = pygame.transform.scale(frontpic, (int(WIDTH), int(HEIGHT)))

# Screen setup variables
clock.tick(FPS)
screen.fill((0,0,0))
click = False

# Front screen
# Handles open up sequence and leads to a menu
def Front():
    run = True
    while run:
        screen.blit(frontpic, (0,0))
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50, 200, 200, 50)
        button_2 = pygame.Rect(50, 300, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                Main()
        if button_2.collidepoint((mx, my)):
            if click:
                FlightData()
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)

        click = False
        #event handler
        for event in pygame.event.get() :
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            else:
                pygame.display.update()

# Main screen
def Main():
    # Establishing a connection
    """ this will be handled differently but for now this will do"""
    """ yeah this implementation is buggy as hell lmao"""
    vehicle = connect('com7', wait_ready=True, baud=9600)
    print("Connecting to vehicle")

    run = True
    while run:
        # Get vehicle attributes
        # For now the attribute will be pitch in degrees
        data = math.degrees(vehicle.attitude.pitch)
        
        screen.blit((bg), (0,0))

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    vehicle.close()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            else:
                pygame.display.update()

# data analysis screen
def FlightData():
    running = True
    while running:
        screen.fill((0,155,0))
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            else:
                pygame.display.update()
        





Front()

vehicle.close()
pygame.quit()
