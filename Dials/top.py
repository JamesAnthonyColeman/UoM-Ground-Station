''' Right now this class will be a placeholder.'''
# Main function will be to have a top down view showing which actuators are moving

import pygame

class Top():
    # Constructor
    def __init__(self, x, y, scale, x2, y2, scale2):
        self.x = x
        self.y = y
        self.scale = scale
        self.x2 = x2
        self.y2 = y2
        self.scale2 = scale2

        # Calling images
        Top = pygame.image.load('Assets/Top.png').convert() 
        Plane3d = pygame.image.load('Assets/3Dplane.png').convert() 

        #Top plane image
        width = Top.get_width()
        height = Top.get_height()
        self.Top = pygame.transform.scale(Top, (int(width * scale), int(height * scale)))
        #3D plane image
        width = Plane3d.get_width()
        height = Plane3d.get_height()
        self.Plane3d = pygame.transform.scale(Plane3d, (int(width * scale2), int(height * scale2)))



    def draw(self, screen):
        screen.blit(self.Top, (self.x, self.y))
        screen.blit(self.Plane3d, (self.x2, self.y2))