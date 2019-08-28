import os, time, datetime, threading, random, sys, string
import numpy as np
from cortix import Module
from cortix import Network
from cortix import Cortix
import matplotlib.pyplot as plt
import matplotlib

import matplotlib.image as mpimg
import matplotlib.animation as animation
import pandas as pd

class Particle_Plot(Module):
    def __init__(self, shape,modules=5,runtime=None):
        super().__init__()
        self.filetime = str(datetime.datetime.now())[:10]
        self.fps = 60
        self.length = modules
        self.shape = shape
        self.timestamp=str(datetime.datetime.now())
        self.bndry = []
        self.colordic = dict()
        
    def run(self):
        print('start plot')
        self.dic = {}
        c = 0
        
        writer = animation.FFMpegFileWriter(fps=self.fps)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        x,y = [f[0] for f in self.shape],[f[1] for f in self.shape]
        ax.plot(x,y,'black')
        ax.axis('off')
        ax.autoscale()
        ax.set_aspect( 'equal', adjustable='datalim')
        ax.relim()
        
        modcount,self.oe=0,0
        self.linedic = {}
        tempdir='.writer'
        self.dpi = 90
        anifilename = 'particle_animation.mp4'.format(self.filetime)
        writer.setup(fig,anifilename, dpi=self.dpi)
        self.tke=0
        self.ke,self.elapsed = [],[]
        while True:
            for i in self.ports:
                if not 'plot' in str(i):
                    continue
                lis = self.recv(i)
                self.send('hi',i)
                if isinstance(lis,str):
                    c+=1
                    self.color=lis
                    if c >=self.length:
                        writer.finish()
                        print(len(self.ke))
                        fig = plt.figure()
                        plt.plot(self.elapsed,self.ke)
##                        plt.autoscale()
##                        plt.relim()
                        plt.title("Total Kinetic Energy vs Time")
                        plt.savefig('energy_vs_time.png'.format(self.filetime))
                        return
                    continue
                
                for line in lis:
                    self.colordic[line.name] = [line.color, line.r]
                    if line.name not in self.dic:
                        self.dic[line.name]=[]
                        self.linedic[line.name], = ax.plot([],[],self.colordic[line.name][0])
                    self.tke += line.ke
                    def xy(r,phi):
                        return [r*np.cos(phi), r*np.sin(phi)]
                    ucircle = xy(self.colordic[line.name][1],np.arange(0,6.28,0.01))
                    x,y = line.p[0]+ucircle[0],line.p[1]+ucircle[1]
                    self.linedic[line.name].set_data(x,y)
                modcount+=1
                elapsed = line.elapsed
                if round(elapsed,1) > self.oe:
                    print('Elapsed Time:', round(elapsed,1))
                    self.oe=round(elapsed,1)
                if modcount >= self.length:
                    self.ke.append(self.tke)
                    self.elapsed.append(elapsed)
                    self.tke=0
                    writer.grab_frame()
                    modcount = 0