"""
Configures and runs a single simulation of the XTA
"""

import os
import matplotlib.pyplot as plt
from distgen import Generator
import glob
from tools import dcm_crop, laser_load, write_distgen_xy_dist
import shutil
from astra import Astra

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
        IMAGE, xy, laser_name = laser_load(vcc, laser_index)
        FOUT = write_distgen_xy_dist(f'astra-inputs/{laser_name}.txt', IMAGE, xy, resolution_units='um')

        #Generates distribution
        dist_path = os.path.join(self.data_path, f'{self.name}.jpg')
        plt.imsave(dist_path, dcm_crop(self.dcm_path))
        self.dist.input['xy_dist']['file'] = dist_path
        self.dist.run()

        self.particles = self.dist.particles 
        self.particles.write_astra('astra-inputs/astra_particles.txt')

        #Initialize Astra
        self.init_astra()

        return self.particles, self.dist

    def init_astra(self):
        astra_file = 'astra-inputs/xta.in'
        self.astra = Astra(initial_particles=self.particles, input_file=astra_file, verbose=False)

    def run(self, type, **kwargs):
        if type == 'single':
            self.single_scan()
        elif type == 'cont_scan':
            self.cont_scan(kwargs)
        else:
            raise Exception('No simulation type given')

    def single_scan(self):
        self.astra.run()

    def cont_scan(parameter, verbose):
        pass

    def archive(self, name):
        path = os.path.join(self.sim_path, self.name, 'data', name)
        self.astra.archive(path)

    def plot():
        pass
