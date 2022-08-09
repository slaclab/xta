"""
Configures and runs a single simulation of the XTA
"""

from distgen import Generator
import glob
from tools import dcm_crop, laser_load, write_distgen_xy_dist

class xta_sim:

    def __init__(self, xta_path, sim_path, init_dcm_path):
        self.xta_path = xta_path
        self.sim_path = sim_path
        self.init_dcm_path = init_dcm_path
        self.configured = False
        
        #Initialize dist file
        dist_file = 'astra-inputs/distgen.yaml'
        self.dist = Generator(dist_file, verbose=False)

    def sim_checkdir(self):
        #Check directories and assign path variables
        self.dcm_path = dcm_path
        pass

    def sim_mkdir(self):
        self.dcm_path = self.init_dcm_path
        pass

    def generate_dist(self, laser_index):

        #Load laser image
        vcc = glob.glob(f'{self.sim_path}/laser_mat_images/*.mat')
        IMAGE, xy, laser_name = laser_load(vcc, laser_index)
        FOUT = write_distgen_xy_dist(f'astra-inputs/{laser_name}.txt', IMAGE, xy, resolution_units='um')

        #Generates distribution
        self.dist.input['xy_dist']['file'] = dcm_crop(self.dcm_path)
        self.dist.run()

        particles = self.dist.particles 
        particles.write_astra('astra-inputs/astra_particles.txt')
        return particles, self.dist

    def input(self):

        self.configured = True
        pass

    def run(self, **kwargs):

        if not self.configured:
            raise Exception("Simulation inputs not configured")
            

        pass

    def scan(parameter, verbose):
        pass

    def plot():
        pass
