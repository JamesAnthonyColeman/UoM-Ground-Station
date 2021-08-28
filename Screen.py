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

# Variables
WIDTH, HEIGHT = 1280, 720 #1003, 600 # 1280, 720
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
logo = pygame.image.load('Assets/TAB_col_background.png').convert_alpha()


# Screen setup veriables
clock.tick(FPS)
screen.fill((0, 0, 0))
click = False




"""Intro"""
"""This will have the 5-10 second intro and can be used to collect assets"""
def Intro():
    screen.fill((255, 255, 255))
    screen.blit(intro1, (360, 220))
    pygame.display.update()
    pygame.time.delay(3000)
    screen.fill((255, 255, 255))

    font = pygame.font.SysFont('Futura', 200)
    img = font.render('UAV', True, (0, 0, 0))
    screen.blit(img, (225, 200))

    font2 = pygame.font.SysFont('Futura', 120)
    img2 = font2.render('Ground Station', True, (0, 0, 0))
    screen.blit(img2, (225, 350))

    pygame.display.update()
    pygame.time.delay(2000)
    Front()




""" Front screen"""
""" This screen should have links to all screens and handle the connection"""
def Front():
    screen.fill((0, 0, 0))
    global Connected
    Connected = False
    run = True
    while run:
        screen.blit(frontpic, (0, 0))
        mx, my = pygame.mouse.get_pos()

        # Tool bar
        ToolBackground = pygame.Rect(0, 0, 1280, 80) # Background
        pygame.draw.rect(screen, (255, 0, 0), ToolBackground)
        LogoWidth = logo.get_width()
        LogoHeight = logo.get_height()
        Logoscale = 0.34 #0.27
        Logo = pygame.transform.scale(logo, (int(LogoWidth * Logoscale), int(LogoHeight * Logoscale))) # Logo
        screen.blit(Logo, (0, 0))
        # Ground station text

        button_1 = pygame.Rect(50, 200, 200, 50) # Main
        button_2 = pygame.Rect(50, 300, 200, 50) # Grapher
        button_3 = pygame.Rect(50, 400, 200, 50) # Data
        button_4 = pygame.Rect(400, 300, 200, 50) # Cameras
        button_5 = pygame.Rect(400, 400, 200, 50) # Options
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

        #Connect button
        if Connected == False:
            button_6 = pygame.Rect(750, 300, 200, 50) # Connect button
            if button_6.collidepoint((mx, my)):
                if click:
                    Connected = True
                    # Establishing a connection
                    global vehicle 
                    vehicle = connect('com7', wait_ready=True, baud=9600)
                    print("Connecting to vehicle")
            pygame.draw.rect(screen, (255, 0, 0), button_6)
            img6 = font.render('Connect', True, (0, 0, 0))
            screen.blit(img6, (750, 300))
            global Launch_in_seconds
            Launch_in_seconds=time.time()
            global fname
            fname = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S.csv')
        else:
            button_6 = pygame.Rect(750, 300, 200, 50) # Connect button
            if button_6.collidepoint((mx, my)):
                if click:
                    Connected = False
                    vehicle.close()
            pygame.draw.rect(screen, (255, 0, 0), button_6)
            img6 = font.render('Connected', True, (0, 0, 0))
            screen.blit(img6, (750, 300))
            data = math.degrees(vehicle.attitude.pitch)
            data_altitude=vehicle.location.global_frame.alt
            Graph = grapher.Graph(3, 3, data, data_altitude, Launch_in_seconds, fname)


        pygame.display.update()
        click = False
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()





""" Main screen"""
"""This screen will have all the main dials on"""
def Main():

    run = True
    while run:
        screen.fill((170, 170, 170))

        # Get vehicle attributes
        if Connected == True:
            data = math.degrees(vehicle.attitude.pitch)
            data2 = math.degrees(vehicle.attitude.roll)
            data_altitude=vehicle.location.global_frame.alt
            Graph = grapher.Graph(3, 3, data, data_altitude, Launch_in_seconds, fname)
        else:
            data = 0
            data2 = 0
            data_altitude = 0
            Graph = grapher.Graph(3, 3, data, data_altitude, 0, 900)


        # Dials defined
        airspeed_dial = airspeed_indicator.Airspeed( 0, 0, 1, data, 0.4, -5, 0.185,0.125)
        horizon = artificial_horizon.Horizon(103,0)
        altimeter_dial = altimeter.Altitude(402, 0, data_altitude)
        compass_dial = compass.Compass(103, 300, 1, data)
        
        # Used for locating things on the page
        #pos = pygame.mouse.get_pos() 
        #print(pos)

        # Draw dials
        
        compass_dial.draw(screen)
        airspeed_dial.draw(screen)
        horizon.update(screen, data2, data)
        altimeter_dial.draw(screen)

        pygame.display.update()

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()




""" Graph analysis screen"""
""" This screen will have a bunch of graphs on"""
def Grapher():
    running = True
    while running:
        screen.fill((0, 155, 0))
       if Connected == True:
            data = math.degrees(vehicle.attitude.pitch)
            data2 = math.degrees(vehicle.attitude.roll)
            data_altitude=vehicle.location.global_frame.alt
            Graph = grapher.Graph(3, 3, data, data_altitude, Launch_in_seconds, fname)
            sample_data = pd.read_csv(fname)
            X = sample_data.iloc[:,0]
            Y = sample_data.iloc[:,1]
            Z = sample_data.iloc[:,2]
        else:
            data = 0
            data2 = 0
            data_altitude = 0
            X = 0
            Y = 0
            Z = 0
            Graph = grapher.Graph(3, 3, data, data_altitude, 0, 900)
        
        Graph.draw(screen,403, 300,X,Y)
        Graph.draw(screen,703, 300,X,Z)
        
        
        pygame.display.update()
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()





""" Data screen"""
""" This screen will have the incomming data packets and information about actuators and more"""
def Data():
    running = True
    while running:
        screen.fill((170, 170, 170))
        if Connected == True:
            data = math.degrees(vehicle.attitude.pitch)
            data2 = math.degrees(vehicle.attitude.roll)
            data_altitude=vehicle.location.global_frame.alt
            Graph = grapher.Graph(3, 3, data, data_altitude, Launch_in_seconds, fname)
        else:
            data = 0
            data2 = 0
            data_altitude = 0
            Graph = grapher.Graph(3, 3, data, data_altitude, 0, 900)
        
        pygame.display.update()
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()





""" Cameras screen"""
""" This screen will handle camera feeds"""
def Cameras():
    running = True
    while running:
        screen.fill((170, 170, 170))
        if Connected == True:
            data = math.degrees(vehicle.attitude.pitch)
            data2 = math.degrees(vehicle.attitude.roll)
            data_altitude=vehicle.location.global_frame.alt
            Graph = grapher.Graph(3, 3, data, data_altitude, Launch_in_seconds, fname)
        else:
            data = 0
            data2 = 0
            data_altitude = 0
            Graph = grapher.Graph(3, 3, data, data_altitude, 0, 900)

        border = pygame.Rect(4, 199, 632, 482)
        pygame.draw.rect(screen, (0, 0, 0), border)
        border = pygame.Rect(639, 199, 632, 482)
        pygame.draw.rect(screen, (0, 0, 0), border)
        border = pygame.Rect(39, 99, 1202, 82)
        pygame.draw.rect(screen, (0, 0, 0), border)

        fpvfeed = pygame.Rect(5, 200, 630, 480)
        pygame.draw.rect(screen, (200, 200, 200), fpvfeed)
        wififeed = pygame.Rect(640, 200, 630, 480)
        pygame.draw.rect(screen, (200, 200, 200), wififeed)
        toolbox = pygame.Rect(40, 100, 1200, 80)
        pygame.draw.rect(screen, (200, 200, 200), toolbox)

        font = pygame.font.SysFont('Futura', 50)
        anafeed = font.render('5.8 GHz', True, (0, 0, 0))
        screen.blit(anafeed, (50, 300))
        anafeed = font.render('Analogue camera feed', True, (0, 0, 0))
        screen.blit(anafeed, (50, 350))
        font = pygame.font.SysFont('Arial', 20)
        anafeed = font.render('Connection not established', True, (0, 0, 0))
        screen.blit(anafeed, (50, 400))

        font = pygame.font.SysFont('Futura', 50)
        anafeed = font.render('2.4 GHz', True, (0, 0, 0))
        screen.blit(anafeed, (690, 300))
        anafeed = font.render('Digital camera feed', True, (0, 0, 0))
        screen.blit(anafeed, (690, 350))
        font = pygame.font.SysFont('Arial', 20)
        anafeed = font.render('Connection not established', True, (0, 0, 0))
        screen.blit(anafeed, (690, 400))

        pygame.display.update()
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()





""" Options screen"""
""" This screen will have a bunch of Options on"""
def Options():
    running = True
    while running:
        screen.fill((170, 170, 170))
        if Connected == True:
            data = math.degrees(vehicle.attitude.pitch)
            data2 = math.degrees(vehicle.attitude.roll)
            data_altitude=vehicle.location.global_frame.alt
            Graph = grapher.Graph(3, 3, data, data_altitude, Launch_in_seconds, fname)
        else:
            data = 0
            data2 = 0
            data_altitude = 0
            Graph = grapher.Graph(3, 3, data, data_altitude, 0, 900)
        
        border = pygame.Rect(39, 99, 592, 602)
        pygame.draw.rect(screen, (0, 0, 0), border)
        border = pygame.Rect(639, 99, 602, 302)
        pygame.draw.rect(screen, (0, 0, 0), border)

        resbox = pygame.Rect(40, 100, 590, 600)
        pygame.draw.rect(screen, (200, 200, 200), resbox)
        creditbox = pygame.Rect(640, 100, 600, 300)
        pygame.draw.rect(screen, (200, 200, 200), creditbox)

        LogoWidth = logo.get_width()
        LogoHeight = logo.get_height()
        Logoscale = 0.5
        Logo = pygame.transform.scale(logo, (int(LogoWidth * Logoscale), int(LogoHeight * Logoscale))) # Logo
        screen.blit(Logo, (800, 500))

        font = pygame.font.SysFont('Futura', 50)
        Resolutiontext = font.render('Resolution: 1280 x 720', True, (0, 0, 0))
        screen.blit(Resolutiontext, (60, 120))
        credittext = font.render('Credits', True, (0, 0, 0))
        screen.blit(credittext, (660, 120))
        connectiontext = font.render('Connection settings', True, (0, 0, 0))
        screen.blit(connectiontext, (60, 370))

        font = pygame.font.SysFont('Arial', 20)
        nametext = font.render('James Coleman', True, (0, 0, 0))
        screen.blit(nametext, (660, 170))
        nametext = font.render('Ildem Baymaz', True, (0, 0, 0))
        screen.blit(nametext, (660, 190))
        nametext = font.render('Jazib Imran', True, (0, 0, 0))
        screen.blit(nametext, (660, 210))
        nametext = font.render('Open source Software produced for the University of Manchester 2021', True, (0, 0, 0))
        screen.blit(nametext, (660, 250))
        nametext = font.render('Summer Internship Program. ', True, (0, 0, 0))
        screen.blit(nametext, (660, 270))

        restext = font.render('1024 x 576', True, (0, 0, 0))
        screen.blit(restext, (60, 170))
        restext = font.render('1152 x 648', True, (0, 0, 0))
        screen.blit(restext, (60, 200))
        restext = font.render('1280 x 720', True, (0, 0, 0))
        screen.blit(restext, (60, 230))
        restext = font.render('1366 x 768', True, (0, 0, 0))
        screen.blit(restext, (60, 260))
        restext = font.render('1600 x 900', True, (0, 0, 0))
        screen.blit(restext, (60, 290))
        restext = font.render('1920 x 1080', True, (0, 0, 0))
        screen.blit(restext, (60, 320))

        comtext = font.render('Com port: 7', True, (0, 0, 0))
        screen.blit(comtext, (60, 410))
        comtext = font.render('Baud: 9600', True, (0, 0, 0))
        screen.blit(comtext, (60, 440))


        pygame.display.update()
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()




# This is where the loop starts and then when the loop ends it closes.

Intro()

vehicle.close()
pygame.quit()

