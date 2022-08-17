"""
Configures and runs a single simulation of the XTA
"""

import os
import matplotlib.pyplot as plt
from distgen import Generator
import glob
from xta.tools import dcm_crop, laser_load, write_distgen_xy_dist
import shutil
from astra import Astra
from xta.scan import scan, cont_scan
from xta.plot import *
from xta.movie import movie

class xta_sim:

    def __init__(self, xta_path, sim_path, init_dcm_path, vcc_path):
        self.xta_path = xta_path
        self.sim_path = sim_path
        self.init_dcm_path = init_dcm_path
        self.vcc_path = vcc_path
        self.name = os.path.splitext(os.path.split(init_dcm_path)[-1])[0]

        #Initialize simulation directory
        self.sim_checkdir()

        #Initialize dist file
        self.init_dist()

    def sim_checkdir(self):
        #Check directories and assign path variables
        self.image_path = os.path.join(self.sim_path, self.name)
        self.data_path = os.path.join(self.image_path, 'data')
        self.plots_path = os.path.join(self.image_path, 'plots')
        paths = [self.image_path, self.data_path, self.plots_path]
        for path in paths:
            if not os.path.exists(path):
                os.mkdir(path)
                print(f'Created directory: {path}')
        self.dcm_path = os.path.join(self.data_path, f'{self.name}.dcm')
        if not os.path.exists(self.dcm_path):
            shutil.copy2(self.init_dcm_path, self.data_path)

    def init_dist(self):
        dist_file = 'astra-inputs/distgen.yaml'
        self.dist = Generator(dist_file, verbose=False)

    def generate_dist(self, laser_index):
        #Load laser image
        vcc = glob.glob(self.vcc_path)
        self.IMAGE, xy, self.laser_name = laser_load(vcc, laser_index)
        FOUT = write_distgen_xy_dist(f'astra-inputs/{self.laser_name}.txt', self.IMAGE, xy, resolution_units='um')

        #Generates distribution
        dist_path = os.path.join(self.data_path, f'{self.name}.jpg')
        plt.imsave(dist_path, dcm_crop(self.dcm_path))
        self.dist.input['xy_dist']['file'] = dist_path
        self.dist.run()

        self.dist_particles = self.dist.particles 
        self.dist_particles.write_astra('astra-inputs/astra_particles.txt')

        #Initialize Astra
        self.init_astra()
        self.init_plots()

        return self.dist_particles, self.dist

    def init_astra(self):
        astra_file = 'astra-inputs/xta.in'
        self.astra = Astra(initial_particles=self.dist_particles, input_file=astra_file, verbose=False)
        self.astra_particles = self.astra.particles

    def init_plots(self):
        #Need automatic limit calculation here
        plt.close('all')
        self.axes = {
            'left_xaxis': -10,
            'right_xaxis': 10, 
            'left_yaxis': -10, 
            'right_yaxis': 10
        }

        #Is this necessary?
        #self.left_xaxis, self.right_xaxis, self.left_yaxis, self.right_yaxis = self.axes.values()
        
        self.num_bins = 42
        self.data = {
            'name': self.name,
            'laser_IMAGE': self.IMAGE, 
            'laser_name': self.laser_name,
            'dist': self.dist,
            'astra': self.astra,
            'plots_path': self.plots_path,
            'axes': self.axes,
            'num_bins': self.num_bins
            }

    def plot(self, type, **kwargs):
        from xta.plot import plotTypes
        if type in plotTypes.keys():
            plotTypes[type](self.data, **kwargs)
        elif type == 'all':
            for type in plotTypes.keys():
                plotTypes[type](self.data, **kwargs)
        else:
            raise ValueError(f'Invalid Plot Type: {type}')

    def movie(self, **kwargs):
        animations_path = os.path.join(self.plots_path, 'animations')
        if not os.path.exists(animations_path):
            os.mkdir(animations_path)
        movie(self.data, **kwargs)

    def simulation(self, type = 'single', parameter = None, **kwargs):
        if type == 'single':
            self.single()
        elif type == 'scan':
            self.scan(parameter, **kwargs)
        elif type == 'cont_scan':
            self.cont_scan(parameter, **kwargs)
        else:
            raise Exception('Invalid Simulation Type')
        self.opt_val = self.outputs[0] #opt_val
        self.min = self.outputs[1]
        self.max = self.outputs[2]

    def single(self):
        self.astra.run()
        self.outputs = [None, None, None]

    def scan(self, parameter, interval, divisions):
        self.outputs = scan(self.astra, parameter, interval, divisions).outputs

    def cont_scan(self, parameter, range, divisions, precision):
        self.outputs = cont_scan(self.astra, parameter, range, divisions, precision).outputs

    def archive(self, name):
        path = os.path.join(self.sim_path, self.name, 'data', name)
        self.astra.archive(path)

    def save_plot(self, ):
        pass