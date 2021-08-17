#
import pygame
import csv
import datetime
import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab

class Graph():
    # Constructor
    def __init__(self, x, y, width, height, Data, Date):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.data = Data
        self.date = Date
        self.title = str(Date.strftime("%Y-%m-%d-%H-%M-%S")) + ".csv"
        ExactTime = datetime.datetime.now()
        Running_time =int(ExactTime.strftime("%S")) - int(Date.strftime("%S"))

        # Setting data as a csv file for current
        with open( self.title, 'a', newline='') as f:
            thewriter = csv.writer(f)
            thewriter.writerow([Running_time , self.data])


    def draw(self, screen):
        sample_data = pd.read_csv(self.title)
        X = sample_data.iloc[:,0]
        Y = sample_data.iloc[:,1]
        fig = pylab.figure(figsize=[self.width, self.height], dpi=100) # 100 dots per inch, so the resulting buffer is 400x400 pixels
        ax = fig.gca()
        ax.plot(Y)
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        
        size = canvas.get_width_height()
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        screen.blit(surf, (self.x,self.y))
    