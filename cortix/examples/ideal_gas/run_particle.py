import os, time, datetime, threading, random, sys, string
import numpy as np
from cortix import Module
from cortix import Network
from cortix import Cortix
from cortix.examples import Particle_Plot
from cortix.examples import Particle_Handler

class Simulation:
    def __init__(self):
        self.n_list = [15,]

        self.procs = 15
        self.runtime=30
        self.t_step = 0.01
        
        self.r=1
        self.mod_list = []
        self.shape = [(0, 0), (0, 100), (100, 100),(100,0),(0, 0)]

        self.fps = 60

    def run(self):
        for c,i in enumerate(self.n_list):
            self.cortix = Cortix(use_mpi=False)
            self.net = Network()
            self.cortix.network = self.net
            self.plot = Particle_Plot(self.shape,modules=self.procs,runtime=self.runtime)
            self.plot.fps = self.fps
            self.net.add_module(self.plot)
            print(c+1,'iterations')
            self.balls = i
            self.balleach = int(self.balls/self.procs)
            remainder = self.balls/self.procs
            self.mod_list = []
            for i in range(self.procs):
                balls = self.balleach
                if remainder > 0:
                    balls+=1
                    remainder -= 1
                app = Particle_Handler(self.shape, balls=balls,runtime = self.runtime)
                app.r=self.r
                app.t_step = 0.01
                self.mod_list.append(app)
                self.net.add_module(app)
            for c,i in enumerate(self.mod_list):
                self.net.connect([i,'plot-send{}'.format(c)],[self.plot,'plot-receive{}'.format(c)])
                for j in self.mod_list:
                    if i == j:
                        continue
                    name = '{}{}'.format(i.name,j.name)
                    name2 = '{}{}'.format(j.name,i.name)
                    self.net.connect([i,name], [j,name2])
##            threading.Thread(target=self.plotting,daemon=True).start()
            self.cortix.run()
            self.cortix.close()
            del self.cortix
            print('finished sim')


if __name__ == '__main__':
    sim = Simulation()
    sim.runtime = 20
    sim.r = 1
    sim.fps = 100
    sim.shape = [(-10, -10), (-10, 30), (30, 30),(30,-10),(-10, -10)]
    sim.t_step = 0.01
    sim.procs = 4
    sim.n_list = [10]
    sim.run()
