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
from Dials import map_module
from Dials import top
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

# Define longitude and latitude of top left and bottom right corners of map
long1,lat1,long2,lat2=-2.4664,53.5733,-2.4015,53.5459


# Screen setup veriables
clock.tick(FPS)
screen.fill((0, 0, 0))
click = False
Connected = False
Name = 'Empty'




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
    Main()




""" Front screen"""
""" This screen should have links to all screens and handle the connection"""
def Front():
    global Connected
    global click

    mx, my = pygame.mouse.get_pos()
    # Tool bar
    ToolBackground = pygame.Rect(0, 0, 1280, 80)  # Background
    pygame.draw.rect(screen, (130, 130, 130), ToolBackground)
    LogoWidth = logo.get_width()
    LogoHeight = logo.get_height()
    Logoscale = 0.34  # 0.27
    Logo = pygame.transform.scale(logo, (int(LogoWidth * Logoscale), int(LogoHeight * Logoscale)))  # Logo
    screen.blit(Logo, (0, 0))

    # Button border
    border = pygame.Rect(199, 4, 202, 32) # Main border
    pygame.draw.rect(screen, (0, 0, 0), border)
    border = pygame.Rect(419, 4, 202, 32) # Grapher border
    pygame.draw.rect(screen, (0, 0, 0), border)
    border = pygame.Rect(639, 4, 202, 32) # Data border
    pygame.draw.rect(screen, (0, 0, 0), border)
    border = pygame.Rect(199, 44, 202, 32) # Cameras border
    pygame.draw.rect(screen, (0, 0, 0), border)
    border = pygame.Rect(419, 44, 202, 32) # Options border
    pygame.draw.rect(screen, (0, 0, 0), border)
    border = pygame.Rect(639, 44, 202, 32) # Map border
    pygame.draw.rect(screen, (0, 0, 0), border)
    border = pygame.Rect(859, 4, 202, 32) # Connect border
    pygame.draw.rect(screen, (0, 0, 0), border)

    button_1 = pygame.Rect(200, 5, 200, 30)  # Main
    button_2 = pygame.Rect(420, 5, 200, 30)  # Grapher
    button_3 = pygame.Rect(640, 5, 200, 30)  # Data
    button_4 = pygame.Rect(200, 45, 200, 30)  # Cameras
    button_5 = pygame.Rect(420, 45, 200, 30)  # Options
    button_7 = pygame.Rect(640,45,200,30)    #Map
    if button_1.collidepoint((mx, my)):
        if click:
            click = False
            Main()
    if button_2.collidepoint((mx, my)):
        if click:
            click = False
            Grapher()
    if button_3.collidepoint((mx, my)):
        if click:
            click = False
            Data()
    if button_4.collidepoint((mx, my)):
        if click:
            click = False
            Cameras()
    if button_5.collidepoint((mx, my)):
        if click:
            click = False
            Options()
    if button_7.collidepoint((mx, my)):
        if click:
            click = False
            Map()
    font = pygame.font.SysFont('Futura', 30)
    img1 = font.render('Main', True, (0, 0, 0))
    img2 = font.render('Grapher', True, (0, 0, 0))
    img3 = font.render('Data', True, (0, 0, 0))
    img4 = font.render('Camera', True, (0, 0, 0))
    img5 = font.render('Options', True, (0, 0, 0))
    img7 = font.render('Map', True, (0, 0, 0))

    if Name == 'Main':
        pygame.draw.rect(screen, (109, 00, 157), button_1)
        screen.blit(img1, (200, 10))
    else:
        pygame.draw.rect(screen, (200, 200, 200), button_1)
        screen.blit(img1, (200, 10))

    if Name == 'Grapher':
        pygame.draw.rect(screen, (109, 00, 157), button_2)
        screen.blit(img2, (420, 10))
    else:
        pygame.draw.rect(screen, (200, 200, 200), button_2)
        screen.blit(img2, (420, 10))

    if Name == 'Data':
        pygame.draw.rect(screen, (109, 00, 157), button_3)
        screen.blit(img3, (640, 10))
    else:
        pygame.draw.rect(screen, (200, 200, 200), button_3)
        screen.blit(img3, (640, 10))

    if Name == 'Cameras':
        pygame.draw.rect(screen, (109, 00, 157), button_4)
        screen.blit(img4, (200, 50))
    else:
        pygame.draw.rect(screen, (200, 200, 200), button_4)
        screen.blit(img4, (200, 50))

    if Name == 'Options':
        pygame.draw.rect(screen, (109, 00, 157), button_5)
        screen.blit(img5, (420, 50))
    else:
        pygame.draw.rect(screen, (200, 200, 200), button_5)
        screen.blit(img5, (420, 50))

    if Name == 'Map':
        pygame.draw.rect(screen, (109, 00, 157), button_7)
        screen.blit(img7, (640, 50))
    else:
        pygame.draw.rect(screen, (200, 200, 200), button_7)
        screen.blit(img7, (640, 50))

    Connection()
    pygame.display.update()

def Connection():
    #Connect button
        global Connected
        global click
        mx, my = pygame.mouse.get_pos()
        font = pygame.font.SysFont('Futura', 30)
        if Connected == False:
            button_6 = pygame.Rect(860, 5, 200, 30) # Connect button
            if button_6.collidepoint((mx, my)):
                if click:
                    try:
                        Connected = True
                        # Establishing a connection
                        global vehicle 
                        vehicle = connect('com7', wait_ready=True, baud=9600)
                        #print("Connecting to vehicle")
                    except:
                        Connected = False
            pygame.draw.rect(screen, (200, 200, 200), button_6)
            img6 = font.render('Connect', True, (0, 0, 0))
            screen.blit(img6, (860, 10))
            global Launch_in_seconds
            Launch_in_seconds=time.time()
            global fname
            fname = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S.csv')
        else:
            button_6 = pygame.Rect(860, 5, 200, 30) # Connect button
            if button_6.collidepoint((mx, my)):
                if click:
                    Connected = False
                    vehicle.close()
            pygame.draw.rect(screen, (200, 200, 200), button_6)
            img6 = font.render('Connected', True, (0, 0, 0))
            screen.blit(img6, (860, 10))
            data = math.degrees(vehicle.attitude.pitch)
            data_altitude=vehicle.location.global_frame.alt
            Graph = grapher.Graph(6, 4, data, data_altitude, Launch_in_seconds, fname)




""" Main screen"""
"""This screen will have all the main dials on"""
def Main():
    global click
    global Name
    Name = 'Main'
    run = True
    while run:
        screen.fill((170, 170, 170))

        # Get vehicle attributes
        if Connected == True:
            data = math.degrees(vehicle.attitude.pitch)
            data2 = math.degrees(vehicle.attitude.roll)
            data_altitude=vehicle.location.global_frame.alt
            Graph = grapher.Graph(6, 4, data, data_altitude, Launch_in_seconds, fname)
        else:
            data = 0
            data2 = 0
            data_altitude = 0
            Graph = grapher.Graph(6, 4, data, data_altitude, 0, 900)


        # Dials defined
        airspeed_dial = airspeed_indicator.Airspeed( 0, 100, 1, data, 0.4, -5, 0.185,0.125)
        horizon = artificial_horizon.Horizon(103,100)
        altimeter_dial = altimeter.Altitude(402, 100, data_altitude)
        compass_dial = compass.Compass(103, 400, 1, data)
        topdown = top.Top(402, 400, 0.5, 800, 120, 0.35)
        
        # Used for locating things on the page
        #pos = pygame.mouse.get_pos() 
        #print(pos)

        # Draw dials
        
        compass_dial.draw(screen)
        airspeed_dial.draw(screen)
        horizon.update(screen, data2, data)
        altimeter_dial.draw(screen)
        topdown.draw(screen)
        Front()

        #Connection()
        pygame.display.update()
        click = False
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
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
    global click
    global Name
    Name = 'Grapher'
    while running:
        screen.fill((170, 170, 170))
        if Connected == True:
            data = math.degrees(vehicle.attitude.pitch)
            data2 = math.degrees(vehicle.attitude.roll)
            data_altitude=vehicle.location.global_frame.alt
            Graph = grapher.Graph(6, 4, data, data_altitude, Launch_in_seconds, fname)
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
            Graph = grapher.Graph(6, 4, data, data_altitude, 0, 900)
        
        Graph.draw(screen,0, 100,X,Y,'Pitch (degrees)')
        Graph.draw(screen,602, 100,X,Z,'Altitude (m)')
        Front()
        
        #Connection()
        pygame.display.update()
        click = False
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
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
    global click
    global Name
    Name = 'Data'
    while running:
        screen.fill((170, 170, 170))
        if Connected == True:
            data = math.degrees(vehicle.attitude.pitch)
            data2 = math.degrees(vehicle.attitude.roll)
            data_altitude=vehicle.location.global_frame.alt
            Graph = grapher.Graph(6, 4, data, data_altitude, Launch_in_seconds, fname)
        else:
            data = 0
            data2 = 0
            data_altitude = 0
            Graph = grapher.Graph(6, 4, data, data_altitude, 0, 900)
        

        border = pygame.Rect(39, 99, 592, 602)
        pygame.draw.rect(screen, (0, 0, 0), border)
        border = pygame.Rect(639, 99, 607, 302)
        pygame.draw.rect(screen, (0, 0, 0), border)

        resbox = pygame.Rect(40, 100, 590, 600)
        pygame.draw.rect(screen, (200, 200, 200), resbox)
        creditbox = pygame.Rect(640, 100, 605, 300)
        pygame.draw.rect(screen, (200, 200, 200), creditbox)

        # This is where the data is written and included on the page
        if Connected == True:
            font = pygame.font.SysFont('Futura', 25)
            text = 'Last heartbeat (Last response from UAV): ' + str(vehicle.last_heartbeat) 
            Heartbeat = font.render(text , True, (0, 0, 0))
            screen.blit(Heartbeat, (50, 110))

            text = 'Battery Voltage, V: ' + str(vehicle.battery.voltage) + ' V'
            Batvolt = font.render(text , True, (0, 0, 0))
            screen.blit(Batvolt, (50, 140))

            text = 'Battery Current, A: ' + str(vehicle.battery.current) + ' A'
            Batcurr = font.render(text , True, (0, 0, 0))
            screen.blit(Batcurr, (50, 170))

            text = 'Battery Level: ' + str(vehicle.battery.level)
            Batcurr = font.render(text , True, (0, 0, 0))
            screen.blit(Batcurr, (50, 200))

            text = 'Velocity (x, y, z), ms^-1: ' + str(vehicle.velocity)
            Velo = font.render(text , True, (0, 0, 0))
            screen.blit(Velo, (50, 230))

            text = 'Attitude (pitch, yaw, roll), degrees: ' + str(round(math.degrees(vehicle.attitude.pitch),4)) + '  ' + str(round(math.degrees(vehicle.attitude.yaw),4)) + '  ' + str(round(math.degrees(vehicle.attitude.roll),4)) 
            Velo = font.render(text , True, (0, 0, 0))
            screen.blit(Velo, (50, 260))

            text = 'Armed: ' + str(vehicle.armed)
            Armed = font.render(text , True, (0, 0, 0))
            screen.blit(Armed, (50, 290))

            text = 'Is armable: ' + str(vehicle.is_armable)
            armable = font.render(text , True, (0, 0, 0))
            screen.blit(armable, (50, 320))

            text = 'System Status: ' + str(vehicle.system_status)
            stat = font.render(text , True, (0, 0, 0))
            screen.blit(stat, (50, 350))

            text = 'Heading: ' + str(vehicle.heading)
            heading = font.render(text , True, (0, 0, 0))
            screen.blit(heading, (50, 380))

            text = 'Ground speed: ' + str(vehicle.groundspeed)
            heading = font.render(text , True, (0, 0, 0))
            screen.blit(heading, (50, 410))

            text = 'Airspeed: ' + str(vehicle.airspeed)
            airspeed = font.render(text , True, (0, 0, 0))
            screen.blit(airspeed, (50, 440))

            text = 'Channels: '
            channels = font.render(text , True, (0, 0, 0))
            screen.blit(channels, (50, 470))

            text = str(vehicle.channels)
            fontnew = pygame.font.SysFont('Futura', 20)
            channels = fontnew.render(text , True, (0, 0, 0))
            screen.blit(channels, (50, 500))

            text = 'Home Location: ' + str(vehicle.home_location)
            home = font.render(text , True, (0, 0, 0))
            screen.blit(home, (50, 530))

            text = 'GPS satellites visible: ' + str(vehicle.gps_0.satellites_visible)
            Satvis = font.render(text , True, (0, 0, 0))
            screen.blit(Satvis, (50, 560))

            text = 'GPS fix type: ' + str(vehicle.gps_0.fix_type)
            GPSfix = font.render(text , True, (0, 0, 0))
            screen.blit(GPSfix, (50, 590))

            text = 'GPS Altitude (global frame): ' + str(vehicle.location.global_frame.alt)
            GPSaltgf = font.render(text , True, (0, 0, 0))
            screen.blit(GPSaltgf, (50, 620))

            text = 'GPS Altitude (global relative frame): ' + str(vehicle.location.global_relative_frame.alt)
            GPSaltgf = font.render(text , True, (0, 0, 0))
            screen.blit(GPSaltgf, (50, 6200))

            #Red background
            ch1 = pygame.Rect(645, 105, 70, 290)
            pygame.draw.rect(screen, (255, 0, 0), ch1)
            text = 'ch1 ' 
            ch = font.render(text , True, (0, 0, 0))
            screen.blit(ch, (660, 250))

            ch2 = pygame.Rect(720, 105, 70, 290)
            pygame.draw.rect(screen, (255, 0, 0), ch2)
            text = 'ch2 ' 
            ch = font.render(text , True, (0, 0, 0))
            screen.blit(ch, (735, 250))

            ch3 = pygame.Rect(795, 105, 70, 290)
            pygame.draw.rect(screen, (255, 0, 0), ch3)
            text = 'ch3 ' 
            ch = font.render(text , True, (0, 0, 0))
            screen.blit(ch, (810, 250))

            ch4 = pygame.Rect(870, 105, 70, 290)
            pygame.draw.rect(screen, (255, 0, 0), ch4)
            text = 'ch4 ' 
            ch = font.render(text , True, (0, 0, 0))
            screen.blit(ch, (885, 250))

            ch5 = pygame.Rect(945, 105, 70, 290)
            pygame.draw.rect(screen, (255, 0, 0), ch5)
            text = 'ch5 ' 
            ch = font.render(text , True, (0, 0, 0))
            screen.blit(ch, (960, 250))

            ch6 = pygame.Rect(1020, 105, 70, 290)
            pygame.draw.rect(screen, (255, 0, 0), ch6)
            text = 'ch6 ' 
            ch = font.render(text , True, (0, 0, 0))
            screen.blit(ch, (1035, 250))

            ch7 = pygame.Rect(1095, 105, 70, 290)
            pygame.draw.rect(screen, (255, 0, 0), ch7)
            text = 'ch7 ' 
            ch = font.render(text , True, (0, 0, 0))
            screen.blit(ch, (1110, 250))

            ch8 = pygame.Rect(1170, 105, 70, 290)
            pygame.draw.rect(screen, (255, 0, 0), ch8)
            text = 'ch8 ' 
            ch = font.render(text , True, (0, 0, 0))
            screen.blit(ch, (1185, 250))
            #Grey overlay
            Height = (data/90) * 290
            ch1 = pygame.Rect(645, 105, 70, Height)
            pygame.draw.rect(screen, (200, 200, 200), ch1)
            ch2 = pygame.Rect(720, 105, 70, Height)
            pygame.draw.rect(screen, (200, 200, 200), ch2)
            ch3 = pygame.Rect(795, 105, 70, Height)
            pygame.draw.rect(screen, (200, 200, 200), ch3)
            ch4 = pygame.Rect(870, 105, 70, Height)
            pygame.draw.rect(screen, (200, 200, 200), ch4)
            ch5 = pygame.Rect(945, 105, 70, Height)
            pygame.draw.rect(screen, (200, 200, 200), ch5)
            ch6 = pygame.Rect(1020, 105, 70, Height)
            pygame.draw.rect(screen, (200, 200, 200), ch6)
            ch7 = pygame.Rect(1095, 105, 70, Height)
            pygame.draw.rect(screen, (200, 200, 200), ch7)
            ch8 = pygame.Rect(1170, 105, 70, Height)
            pygame.draw.rect(screen, (200, 200, 200), ch8)
        else:
            font = pygame.font.SysFont('Futura', 70)
            text = 'Connection not made '
            Heartbeat = font.render(text , True, (0, 0, 0))
            screen.blit(Heartbeat, (80, 210))
            screen.blit(Heartbeat, (680, 210))
            text = 'No Data to display '
            Heartbeat = font.render(text , True, (0, 0, 0))
            screen.blit(Heartbeat, (100, 410))
            

        
        Front()
        #Connection()
        pygame.display.update()
        click = False
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
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
    global click
    global Name
    Name = 'Cameras'
    while running:
        screen.fill((170, 170, 170))
        if Connected == True:
            data = math.degrees(vehicle.attitude.pitch)
            data2 = math.degrees(vehicle.attitude.roll)
            data_altitude=vehicle.location.global_frame.alt
            Graph = grapher.Graph(6, 4, data, data_altitude, Launch_in_seconds, fname)
        else:
            data = 0
            data2 = 0
            data_altitude = 0
            Graph = grapher.Graph(6, 4, data, data_altitude, 0, 900)

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

        Front()
        #Connection()
        pygame.display.update()
        click = False
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
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
    global click
    global Name
    Name = 'Options'
    while running:
        screen.fill((170, 170, 170))
        if Connected == True:
            data = math.degrees(vehicle.attitude.pitch)
            data2 = math.degrees(vehicle.attitude.roll)
            data_altitude=vehicle.location.global_frame.alt
            Graph = grapher.Graph(6, 4, data, data_altitude, Launch_in_seconds, fname)
        else:
            data = 0
            data2 = 0
            data_altitude = 0
            Graph = grapher.Graph(6, 4, data, data_altitude, 0, 900)
        
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

        Front()

        #Connection()
        pygame.display.update()
        click = False
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
def Map():

    global click
    global Name
    Name = 'Map'

    running=True
    while running:

        if Connected == True:
            heading=vehicle.heading
            map = map_module.Map(long1, lat1, long2, lat2, WIDTH, HEIGHT, 360 - heading)
            map.draw(screen, vehicle.location)
        else:
            map=map_module.Map(long1, lat1, long2, lat2, WIDTH, HEIGHT, 0)
            map.default_draw(screen)



        Front()
        # Connection()
        pygame.display.update()
        click = False
        # event handler
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
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

