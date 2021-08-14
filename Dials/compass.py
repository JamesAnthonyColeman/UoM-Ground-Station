# Program will be a class that will be imported.
# Program outputs a compass dial

import pygame


class Compass():
    # Constructor
    def __init__(self, x, y, scale, Data):

        # Calling images
        DialBG = pygame.image.load('Assets/HeadingIndicator_Background.png').convert() 
        Headingwheel = pygame.image.load('Assets/HeadingWeel.png').convert() 
        headingindictorAircraft = pygame.image.load('Assets/HeadingIndicator_Aircraft.png').convert() 

        #Dial background
        width = DialBG.get_width()
        self.width = width
        height = DialBG.get_height()
        self.height = height
        self.DialBG = pygame.transform.scale(DialBG, (int(width * scale), int(height * scale)))

        #Heading Wheel
        width2 = Headingwheel.get_width()
        self.width2 = width2
        height2 = Headingwheel.get_height()
        self.height2 = height2
        self.Headingwheel = pygame.transform.scale(Headingwheel, (int(width2 * scale), int(height2 * scale)))
        #self.Headingwheel = pygame.transform.rotate(self.Headingwheel, Data)

        #Heading indicator Aircraft
        width3 = headingindictorAircraft.get_width()
        self.width3 = width3
        height3 = headingindictorAircraft.get_height()
        self.height3 = height3
        self.headingindictorAircraft = pygame.transform.scale(headingindictorAircraft, (int(width3 * scale), int(height3 * scale)))
        
        self.data = Data
        self.rect = self.DialBG.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.scale = scale


    def draw(self, screen):
        self.image = self.DialBG
        self.image.set_colorkey(0xFFFF00)
        self.image2 = self.Headingwheel
        self.image2.set_colorkey(0xFFFF00)
        self.image3 = self.headingindictorAircraft
        self.image3.set_colorkey(0xFFFF00)

        screen.blit(self.image, (self.rect.x, self.rect.y))
        #screen.blit(self.image2, ((self.rect.x + (13*self.scale)), (self.rect.y + (13*self.scale))))
        pos = (253, 445)
        
        # calcaulate the axis aligned bounding box of the rotated image
        w, h       = self.image2.get_size()
        box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(self.data) for p in box]
        min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
        originPos = (135,135)

        # calculate the translation of the pivot 
        pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate(self.data)
        pivot_move   = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

        # get a rotated image
        rotated_image = pygame.transform.rotate(self.image2, self.data)

        # rotate and blit the image
        screen.blit(rotated_image, origin)

        #self.blitRotate( self.image3, pos, (w/2, h/2), self.data)
        screen.blit(self.image3, ((self.rect.x + (70*self.scale)), (self.rect.y + (40*self.scale))))
    