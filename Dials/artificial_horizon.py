
# note - see end to adjust pitch and roll

import math
import serial
import pygame
from pygame.locals import *
pygame.init()
import sys
import csv

# create dial class
class Dial:
   """
   Generic dial type.
   """
   def __init__(self, image, frameImage, x=0, y=0, w=0, h=0):
       """
       x,y = coordinates of top left of dial.
       w,h = Width and Height of dial.
       """
       self.x = x 
       self.y = y
       self.image = image
       self.frameImage = frameImage

       # can do self.anything to create any attribute that is not defined in input for class at top
       self.dial = pygame.Surface(self.frameImage.get_rect()[2:4])
       self.dial.fill(0xFFFF00)
       if(w==0):
          w = self.frameImage.get_rect()[2]
       if(h==0):
          h = self.frameImage.get_rect()[3]
       self.w = w
       self.h = h
       self.pos = self.dial.get_rect()
       self.pos = self.pos.move(x, y)




   def position(self, x, y):
       """
       Reposition top,left of dial at x,y.
       """
       self.x = x 
       self.y = y
       self.pos[0] = x 
       self.pos[1] = y 

   def position_center(self, x, y):
       """
       Reposition centre of dial at x,y.
       """
       self.x = x
       self.y = y
       self.pos[0] = x - self.pos[2]/2
       self.pos[1] = y - self.pos[3]/2

   def rotate(self, image, angle):
       """
       Rotate supplied image by "angle" degrees.
       This rotates round the centre of the image. 
       If you need to offset the centre, resize the image using self.clip.
       This is used to rotate dial needles and probably doesn't need to be used externally.
       """
       tmpImage = pygame.transform.rotate(image ,angle)
       imageCentreX = tmpImage.get_rect()[0] + tmpImage.get_rect()[2]/2
       imageCentreY = tmpImage.get_rect()[1] + tmpImage.get_rect()[3]/2

       targetWidth = tmpImage.get_rect()[2]
       targetHeight = tmpImage.get_rect()[3]

       imageOut = pygame.Surface((targetWidth, targetHeight))
       imageOut.fill(0xFFFF00)
       imageOut.set_colorkey(0xFFFF00)
       imageOut.blit(tmpImage,(0,0), pygame.Rect( imageCentreX-targetWidth/2,imageCentreY-targetHeight/2, targetWidth, targetHeight ) )
       return imageOut

   def clip(self, image, x=0, y=0, w=0, h=0, oX=0, oY=0):
       """
       Cuts out a part of the needle image at x,y position to the correct size (w,h).
       This is put on to "imageOut" at an offset of oX,oY if required.
       This is used to centre dial needles and probably doesn't need to be used externally.       
       """
       if(w==0):
           w = image.get_rect()[2]
       if(h==0):
           h = image.get_rect()[3]
       needleW = w + 2*math.sqrt(oX*oX)
       needleH = h + 2*math.sqrt(oY*oY)
       imageOut = pygame.Surface((needleW, needleH))
       imageOut.fill(0xFFFF00)
       imageOut.set_colorkey(0xFFFF00)
       imageOut.blit(image, (needleW/2-w/2+oX, needleH/2-h/2+oY), pygame.Rect(x,y,w,h))
       return imageOut

   def overlay(self, image, x, y, r=0):
       """
       Overlays one image on top of another using 0xFFFF00 (Yellow) as the overlay colour.
       """
       x -= (image.get_rect()[2] - self.dial.get_rect()[2])/2
       y -= (image.get_rect()[3] - self.dial.get_rect()[3])/2
       image.set_colorkey(0xFFFF00)
       self.dial.blit(image, (x,y))




# create artificial horizon class
class Horizon(Dial):
   """
   Artificial horizon dial.
   """
   def __init__(self, x=0, y=0, w=0, h=0):
       """
       Initialise dial at x,y.
       Default size of 300px can be overidden using w,h.
       """
       self.image = pygame.image.load('Assets/Horizon_GroundSky.png').convert()
       self.frameImage = pygame.image.load('Assets/Horizon_Background.png').convert()
       self.maquetteImage = pygame.image.load('Assets/Maquette_Avion.png').convert()
       Dial.__init__(self, self.image, self.frameImage, x, y, w, h)
   def update(self, screen, angleX, angleY):
       """
       Called to update an Artificial horizon dial.
       "angleX" and "angleY" are the inputs.
       "screen" is the surface to draw the dial on.
       """
       angleX %= 360
       angleY %= 360
       if (angleX > 180):
           angleX -= 360 
       if (angleY > 90)and(angleY < 270):
           angleY = 180 - angleY 
       elif (angleY > 270):
           angleY -= 360
       tmpImage = self.clip(self.image, 0, (59-angleY)*720/180, 250, 250)
       tmpImage = self.rotate(tmpImage, angleX)
       self.overlay(tmpImage, 0, 0)
       self.overlay(self.frameImage, 0,0)
       self.overlay(self.maquetteImage, 0,0)
       self.dial.set_colorkey(0xFFFF00)
       screen.blit( pygame.transform.scale(self.dial,(self.w,self.h)), self.pos )

