import pygame



class Map():
    def __init__(self,long1,lat1,long2,lat2,width,height,heading):
        self.map=pygame.image.load("Assets/map (1).png")

        self.arrow=pygame.image.load("Assets/arrow.png")
        self.arrow=pygame.transform.rotate(pygame.transform.scale(self.arrow,(15,15)),45)
        self.long1=long1
        self.lat1 = lat1
        self.long2 = long2
        self.lat2 = lat2
        self.width = width
        self.height = height
        self.map = pygame.transform.scale(self.map, (self.width, self.height))
        self.heading=heading



    def calc_location(self,long3, lat3, w, h):
        x = int(((long3 - self.long1) / (self.long2 - self.long1)) * (w))
        y = int(((lat3 - self.lat1) / (self.lat2 - self.lat1)) * (h))
        return x, y



    def draw(self,screen,location):
        screen.blit(self.map, (0, 0))


        longitude = location._lon
        latitude = location._lat


        x, y = self.calc_location(longitude,latitude,self.width,self.height)
        arrow = pygame.transform.rotate(pygame.transform.scale(self.arrow,(15,15)),self.heading)
        screen.blit(arrow,(x,y))
        pygame.display.update()
    def default_draw(self,screen):
        screen.blit(self.map,(0,0))




