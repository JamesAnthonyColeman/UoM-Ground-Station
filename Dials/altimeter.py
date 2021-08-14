import pygame
import pandas as pd
import math

pygame.init()
Width=300
Height=300

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

writing_font = pygame.font.SysFont('Calibri', 20, True, False)
altimeter_font = pygame.font.SysFont('Calibri', 20, True, False)

noscale1 = pygame.image.load('Assets/RF_Dial_Background.png')
Dial= pygame.transform.scale(noscale1, (Width//3, Height//6))
noscale2=pygame.image.load('Assets/Indicator_Background.png')
Indicator = pygame.transform.scale(noscale2, (Width, Height))

margin_h = margin_w = 60 
r = (Width - margin_w) / 2 # altimeter inside circle radius

ten_thousands_arm_r= r / 2
thousands_arm_r = r* 6 / 10 
hundreds_arm_r = r * 7 / 10 

alt_text_r = r * 8 / 10 # distance of altimeter markings from center
dash_r = 3 #width of dashes
dash_l = 5 #length of dashes

ten_thosands_w = 5 # ten thousand arm width
thousands_w = 5 # thousand arm width
hundreds_w = 5 # hundred arm width

numbers_in_altimeter = 10
ten_thousands=100000
thousands = 10000
hundreds = 1000

c_x=Width / 2
c_y =Height / 2


def any_point(centre, radius, theta):
    return (centre[0] + radius * math.cos(theta),
            centre[1] + radius * math.sin(theta))

def line(screen, centre, radius, theta, color, width):
    point = any_point(centre, radius, theta)
    pygame.draw.line(screen, color, centre, point, width)
    
def angle(unit, total):
    return 2 * math.pi * unit / total - math.pi / 2


class Altitude():
    def __init__(self, x, y, Data):
        black = (0, 0, 0)
        writing_font = pygame.font.SysFont('Calibri', 20, True, False)
        self.data = Data
        self.font = writing_font
        self.colour = black
        self.image = Indicator
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw_text(self, text, font, text_col, x, y, screen):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        c_x, c_y = self.rect.x+Width//2, self.rect.y+Height//2
        screen.blit(Dial, (c_x-Width//6,c_y+Height//12))
        self.draw_text(str(self.data) , self.font, self.colour, c_x-Width//6+15, c_y+Height//7, screen) 
        centre = (c_x, c_y)
        
        ten_thousands_theta= angle(self.data, ten_thousands) 
        thousands_theta = angle(self.data, thousands) 
        hundreds_theta = angle(self.data, hundreds)

        

        for (radius, theta, color, stroke) in (
            (ten_thousands_arm_r, ten_thousands_theta, white, ten_thosands_w),
            (thousands_arm_r, thousands_theta,black, thousands_w),
            (hundreds_arm_r, hundreds_theta, red, hundreds_w),
        ):
            line(screen, centre, radius, theta, color, stroke)

        for number in range(0, numbers_in_altimeter ):
            theta = angle(number, numbers_in_altimeter)
            text = altimeter_font.render(str(number), True, white)
            screen.blit(text, any_point((c_x-5,c_y-5), alt_text_r, theta))

        for number in range(0, 50):
            theta = angle(number, 50)
            p1 = any_point(centre, r - dash_l, theta)
            p2 = any_point(centre, r, theta)
            pygame.draw.line(screen, white, p1, p2, dash_r)

        
        pygame.display.flip() 
