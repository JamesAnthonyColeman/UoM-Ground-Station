# Program will be a class that will be imported.
# Takes log data in and returns the printed image.
import pygame


class Airspeed():
    # Constructor
    def __init__(self, x, y, scale, Data, scale2, ymod, scale3, scale4):

        # Images and sizing
        AirspeedDial = pygame.image.load('Assets/IAS2.png').convert_alpha() 
        IASBG = pygame.image.load('Assets/IASBG2.png').convert_alpha() 
        ScrollLine = pygame.image.load('Assets/ScrollLine2.png').convert_alpha()

        WHITE = (255, 255, 255)
        font = pygame.font.SysFont('Futura', 22)
        font2 = pygame.font.SysFont('Futura', 16)

        width = AirspeedDial.get_width()
        self.width = width
        height = AirspeedDial.get_height()
        self.height = height
        self.data = Data
        self.font = font
        self.colour = WHITE
        self.font2 = font2
        self.imagedial = pygame.transform.scale(AirspeedDial, (int(width * scale), int(height * scale)))
        self.rect = self.imagedial.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ymod = ymod

        width2 = ScrollLine.get_width()
        self.width2 = width2
        height2 = ScrollLine.get_height()
        self.height2 = height2
        self.scroll = pygame.transform.scale(ScrollLine, (int(width2 * scale2), int(height2 * scale2)))

        width3 = ScrollLine.get_width()
        self.width3 = width3
        height3 = ScrollLine.get_height()
        self.height3 = height3
        self.IASBG = pygame.transform.scale(IASBG, (int(width3 * scale3), int(height3 * scale4)))


    def draw_text(self, text, font, text_col, x, y, screen):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))


    def draw(self, screen):
        self.image = self.imagedial
        self.image2 = self.IASBG

        screen.blit(self.image2, (self.rect.x, self.rect.y + self.ymod))

        Cropped_area = (40, 1126-(self.data*24), (self.width), (self.height-30)) # First two are x and y coords. change where the image is in the cropped box
        # second two are width and height. Cropped area of image.
        screen.blit(self.scroll, (self.rect.x,self.rect.y), Cropped_area)
        
        
        screen.blit(self.image, (self.rect.x, self.rect.y))
        self.draw_text(str(round(self.data,4)) , self.font, self.colour, (self.rect.x + 15), (self.rect.y + 200), screen) 
        self.draw_text( 'TAS :' + str(round(self.data,4)) , self.font2, self.colour, (self.rect.x + 13), (self.rect.y + 425), screen) 


        