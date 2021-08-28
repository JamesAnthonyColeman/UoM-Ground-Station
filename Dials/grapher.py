#
import pygame
import csv
import datetime
import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
import time

class Graph():
    # Constructor
    def __init__(self, width, height, Data, Data2, Seconds, Title):
        self.width = width
        self.height = height
        self.data1 = Data
        self.data2=Data2
        self.seconds=Seconds
        self.title = Title
        ExactTime = time.time()
        Running_time =int(ExactTime) - int(Seconds)

        if self.title == 900: # 900 is a random numerical name for this condition
            pass
        else:
            # Setting data as a csv file for current
            with open( self.title, 'a', newline='') as f:
                thewriter = csv.writer(f)
                thewriter.writerow([Running_time , self.data1, self.data2])
                f.close()


    def draw(self, screen, x, y, rowx, rowy):
        self.x=x
        self.y=y
        self.rowx=rowx
        self.rowy=rowy
        fig = pylab.figure(figsize=[self.width, self.height], dpi=100) # 100 dots per inch, so the resulting buffer is 400x400 pixels
        ax = fig.gca()
        ax.plot(rowx,rowy)
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        
        size = canvas.get_width_height()
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        screen.blit(surf, (self.x,self.y))
    
