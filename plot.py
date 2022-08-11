import os
import matplotlib.pyplot as plt

class plot:
    def __init__(self, IMAGE, astra, plots_path) -> None:
        self.IMAGE = IMAGE
        self.astra = astra
        self.plots_path = plots_path

    def single(self, type, save=True, close=False, **kwargs):
        if not os.path.exists(self.plots_path):
            dir_path = os.path.join(self.plots_path, type)
            os.mkdir(dir_path)
        single(self.plots_path, type, **kwargs)
        if save:

            pass
        if close:
            pass
        pass

    def compare(self, type, **kwargs):
        compare(self.plots_path, type, **kwargs)
        self.compare_dict[type]

class single:
    def __init__(self, plots_path, type, save=True, **kwargs) -> None:
        self.plots_path = plots_path
        self.single_dict = {
        'laser_image': self.laser_image(**kwargs),
        'initial_dist': self.initial_dist(**kwargs),
        'rotated_final_dist': self.rotated_final_dist(**kwargs)
        }
        data = self.single_dict[type]
        if save:
            plt.savefig()
        
    def laser_image(self, **kwargs):
        plt.figure()
        plt.imshow(self.IMAGE)
        plt.xlabel('Pixel', size=20)
        plt.ylabel('Pixel', size=20)

    def initial_dist(self, **kwargs):
        pass

    def rotated_final_dist(self, **kwargs):
        pass

class compare:
    def __init__(self) -> None:
        self.compare_dict = {
        'initial_vs_final': self.initial_vs_final(),
        'inital_vs_rotated': self.inital_vs_rotated()
        }
       

    def initial_vs_final(self):
        pass

    def initial_vs_rotated(self):
        pass
        
class movie:
    def __init__(self, astra) -> None:
        self.astra = astra