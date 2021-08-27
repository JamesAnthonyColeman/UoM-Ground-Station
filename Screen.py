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
Launch_in_seconds=time.time()
fname = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S.csv')

# Variables
WIDTH, HEIGHT = 1003, 600
FPS = 60
clock = pygame.time.Clock()

# Main surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ground control")

# Define images for background and size
bg = pygame.image.load('Assets/grey.png').convert_alpha()
bg = pygame.transform.scale(bg, (int(WIDTH), int(HEIGHT)))
frontpic = pygame.image.load('Assets/CS_15.jpg').convert_alpha()
#frontpic = pygame.transform.scale(frontpic, (int(WIDTH), int(Height)))
intro1 = pygame.image.load('Assets/UOM_White_bg.jpg').convert_alpha()

# Screen setup veriables
clock.tick(FPS)
screen.fill((0, 0, 0))
click = False




"""Intro"""
"""This will have the 5-10 second intro and can be used to collect assets"""
def Intro():
    screen.fill((255, 255, 255))
    screen.blit(intro1, (230, 200))
    pygame.display.update()
    pygame.time.delay(3000)
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont('Futura', 40)
    img = font.render('UoM UAV Ground Station', True, (0, 0, 0))
    screen.blit(img, (200, 200))
    img2 = font.render('Credits: James Coleman, Ildem Baymaz, Jazib Imran', True, (0, 0, 0))
    screen.blit(img2, (100, 500))
    pygame.display.update()
    pygame.time.delay(3000)
    Front()




""" Front screen"""
""" This screen should have links to all screens and handle the connection"""
def Front():
    screen.fill((0, 0, 0))
    run = True
    while run:
        screen.blit(frontpic, (0, 0))
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50, 200, 200, 50)
        button_2 = pygame.Rect(50, 300, 200, 50)
        button_3 = pygame.Rect(50, 400, 200, 50)
        button_4 = pygame.Rect(400, 300, 200, 50)
        button_5 = pygame.Rect(400, 400, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                Main()
        if button_2.collidepoint((mx, my)):
            if click:
                Grapher()
        if button_3.collidepoint((mx, my)):
            if click:
                Data()
        if button_4.collidepoint((mx, my)):
            if click:
                Cameras()
        if button_5.collidepoint((mx, my)):
            if click:
                Options()
        font = pygame.font.SysFont('Futura', 30)
        img1 = font.render('Main', True, (0, 0, 0))
        img2 = font.render('Grapher', True, (0, 0, 0))
        img3 = font.render('Data', True, (0, 0, 0))
        img4 = font.render('Camera', True, (0, 0, 0))
        img5 = font.render('Options', True, (0, 0, 0))        
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        screen.blit(img1, (50, 200))
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        screen.blit(img2, (50, 300))
        pygame.draw.rect(screen, (255, 0, 0), button_3)
        screen.blit(img3, (50, 400))
        pygame.draw.rect(screen, (255, 0, 0), button_4)
        screen.blit(img4, (400, 300))
        pygame.draw.rect(screen, (255, 0, 0), button_5)
        screen.blit(img5, (400, 400))

        click = False
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            else:
                pygame.display.update()




""" Main screen"""
"""This screen will have all the main dials on"""
def Main():
    # Establishing a connection
    vehicle = connect('com7', wait_ready=True, baud=9600)
    print("Connecting to vehicle")
    
    run = True
    while run:
        screen.blit(bg, (0,0))

        # Get vehicle attributes
        # For now the attribute will be pitch in degrees
        data = math.degrees(vehicle.attitude.pitch)
        data_altitude=vehicle.location.global_frame.alt


        # Dials defined
        airspeed_dial = airspeed_indicator.Airspeed( 0, 0, 1, data, 0.4, -5, 0.185,0.125)
        horizon = artificial_horizon.Horizon(103,0)
        altimeter_dial = altimeter.Altitude(402, 0, data_altitude)
        compass_dial = compass.Compass(103, 300, 1, data)
        Graph = grapher.Graph(3, 3, data, data_altitude, Launch_in_seconds, fname)
        sample_data = pd.read_csv(fname)
        X = sample_data.iloc[:,0]
        Y = sample_data.iloc[:,1]
        Z = sample_data.iloc[:,2]

        
        # Used for locating things on the page
        #pos = pygame.mouse.get_pos() 
        #print(pos)

        # Draw dials
        
        compass_dial.draw(screen)
        Graph.draw(screen,403, 300,X,Y)
        Graph.draw(screen,703, 300,X,Z)
        airspeed_dial.draw(screen)
        horizon.update(screen,math.degrees(vehicle.attitude.roll) , math.degrees(vehicle.attitude.pitch))
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




""" Graph analysis screen"""
""" This screen will have a bunch of graphs on"""
def Grapher():
    running = True
    while running:
        screen.fill((0, 155, 0))
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




""" Data screen"""
""" This screen will have the incomming data packets and information about actuators and more"""
def Data():
    running = True
    while running:
        screen.fill((155, 155, 0))
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




""" Cameras screen"""
""" This screen will handle camera feeds"""
def Cameras():
    running = True
    while running:
        screen.fill((0, 155, 155))
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




""" Options screen"""
""" This screen will have a bunch of Options on"""
def Options():
    running = True
    while running:
        screen.fill((155, 155, 155))
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



# This is where the loop starts and then when the loop ends it closes.

Intro()

vehicle.close()
pygame.quit()

