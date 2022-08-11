import os
import matplotlib.pyplot as plt
import numpy as np
from tools import rotate_particles
import matplotlib.animation as animation
from statistics import mean

class plot:
    def __init__(self, IMAGE, laser_name, astra, plots_path, axes, num_bins) -> None:
        self.data = [IMAGE, laser_name, astra, plots_path, axes, num_bins]
        self.plots_path = self.data[3]
        self.num_bins = num_bins

    def single(self, type, save=True, close=False, **kwargs):
        single_path = os.path.join(self.plots_path, 'single')
        if not os.path.exists(single_path):
            os.mkdir(single_path)
            print(f'Created directory: {single_path}')
        self.data[3] = single_path

        single(self.data, type, save, close, **kwargs)

    def compare(self, type, save=True, close=False, **kwargs):
        compare_path = os.path.join(self.plots_path, 'compare')
        if not os.path.exists(compare_path):
            os.mkdir(compare_path)
            print(f'Created directory: {compare_path}')
        self.data[3] = compare_path

        compare(self.data, type, save, close, **kwargs)

class single:
    def __init__(self, data, type, save=True, close=False, **kwargs) -> None:
        self.IMAGE = data[0]
        self.laser_name = data[1]
        self.astra = data[2]
        self.plots_path = data[3]
        self.left_xaxis, self.right_xaxis, self.left_yaxis, self.right_yaxis = data[4]
        self.num_bins = data[5]

        #Generates plot based on type and returns desired file name
        if type == 'laser_image':
            name = self.laser_image(title=self.laser_name, **kwargs)
        elif type == 'initial_dist':
            name = self.initial_dist(**kwargs)
        elif type == 'final_dist':
            name = self.final_dist(**kwargs)
        elif type == 'rotated_final_dist': 
            name = self.rotated_final_dist(**kwargs)
        else:
            raise Exception('Invalid Plot Type')

        if save:
            save_path = os.path.join(self.plots_path, name)
            plt.savefig(save_path, dpi=300)#, bbox_inches='tight')

        if close:
            plt.close()

    def laser_image(self, title, **kwargs):
        plt.figure(figsize=(5, 5))
        plt.imshow(self.IMAGE)
        plt.title(title)
        plt.xlabel('Pixel')
        plt.ylabel('Pixel')
        return f'{title}.jpg'
            

    def initial_dist(self, **kwargs):
        plt.figure(figsize=(5, 5))
        plt.hist2d(self.astra.particles[0].x*10**3, self.astra.particles[0].y*10**3, self.num_bins, facecolor='blue', cmin=1)
        plt.title('Initial Electron Distribution')
        plt.xlabel('x [mm]')
        plt.ylabel('y [mm]')
        plt.xlim([self.left_xaxis, self.right_xaxis])
        plt.ylim([self.left_yaxis, self.right_yaxis])
        return 'initial_electron_dist.jpg'

    def final_dist(self, **kwargs):
        plt.figure(figsize=(5, 5))
        plt.hist2d(self.astra.particles[-1].x*10**3, self.astra.particles[-1].y*10**3, self.num_bins, facecolor='blue', cmin=1)
        plt.title('Final Electron Distribution')
        plt.xlabel('x [mm]')
        plt.ylabel('y [mm]')
        plt.xlim([self.left_xaxis, self.right_xaxis])
        plt.ylim([self.left_yaxis, self.right_yaxis])
        return 'final_electron_dist.jpg'

    def rotated_final_dist(self, **kwargs):
        rotVect = rotate_particles(self.astra, -1)

        plt.figure(figsize=(5, 5))
        plt.hist2d(rotVect[0], rotVect[1], self.num_bins, facecolor='blue', cmin=1)
        plt.title('Rotated Final Electron Distribution')
        plt.xlabel('x [mm]')
        plt.ylabel('y [mm]')
        plt.xlim([self.left_xaxis, self.right_xaxis])
        plt.ylim([self.left_yaxis, self.right_yaxis])
        return 'rotated_final_electron_dist.jpg'

class compare:
    def __init__(self, data, type, save=True, close=False, **kwargs) -> None:
        self.IMAGE = data[0]
        self.laser_name = data[1]
        self.astra = data[2]
        self.plots_path = data[3]
        self.left_xaxis, self.right_xaxis, self.left_yaxis, self.right_yaxis = data[4]
        self.num_bins = data[5]

        if type == 'initial_vs_final':
            name = self.initial_vs_final(**kwargs)
        elif type == 'initial_vs_rotated':
            name = self.initial_vs_rotated(**kwargs)
        else:
            raise Exception(f'Invalid Plot Type: {type}')

        if save:
            save_path = os.path.join(self.plots_path, name)
            plt.savefig(save_path, dpi=300)#, bbox_inches='tight')

        if close:
            plt.close()

    def initial_vs_final(self, title=''):
        #Super plot
        fig, plots = plt.subplots(1, 2, figsize=(10, 5), sharex=True, sharey=True)
        fig.subplots_adjust(wspace=0.2)

        #Final plot
        finalxy = plt.subplot(1,2,2)
        plt.hist2d(self.astra.particles[-1].x*10**3, self.astra.particles[-1].y*10**3, self.num_bins, facecolor='blue', cmin=1)
        plots[1].set(title='Final Shape', xlabel='x [mm]')

        #Initial Plot
        initialxy = plt.subplot(1,2,1)
        plt.hist2d(self.astra.particles[0].x*10**3, self.astra.particles[0].y*10**3, self.num_bins, facecolor='blue', cmin=1)
        plots[0].set(title='Initial Shape', xlabel='x [mm]', ylabel='y [mm]', xlim=[self.left_xaxis, self.right_xaxis], ylim=[self.left_yaxis, self.right_yaxis])

        plt.suptitle(title)

        return 'initial_vs_final.jpg'


    def initial_vs_rotated(self, title=''):
        #Super plot
        fig, plots = plt.subplots(1, 2, figsize=(10, 5), sharex=True, sharey=True)
        fig.subplots_adjust(wspace=0.2)

        rotVect = rotate_particles(self.astra, -1)
        #Final plot
        finalxy = plt.subplot(1,2,2)
        plt.hist2d(rotVect[0], rotVect[1], self.num_bins, facecolor='blue', cmin=1)
        plots[1].set(title='Final Rotated Shape', xlabel='x [mm]')

        #Initial Plot
        initialxy = plt.subplot(1,2,1)
        plt.hist2d(self.astra.particles[0].x*10**3, self.astra.particles[0].y*10**3, self.num_bins, facecolor='blue', cmin=1)
        plots[0].set(title='Initial Shape', xlabel='x [mm]', ylabel='y [mm]', xlim=[self.left_xaxis, self.right_xaxis], ylim=[self.left_yaxis, self.right_yaxis])

        plt.suptitle(title)

        return 'initial_vs_rotated.jpg'
        
class movie:
    def __init__(self, astra, animations_path, axes, num_bins, dist, name, title='', **kwargs) -> None:
        self.astra = astra
        self.animations_path = animations_path
        self.left_xaxis, self.right_xaxis, self.left_yaxis, self.right_yaxis = axes
        self.num_bins = num_bins
        self.dist = dist
        self.name = name
        self.title = title

        #Initial histogram
        self.fig, self.axs = plt.subplots(figsize=(5, 5))
        init_frame = 0
        beam = self.astra.particles[init_frame]

        data, x, y, _ = self.axs.hist2d(beam.x*10**3, beam.y*10**3, num_bins, cmin=1)
        self.axs.set_title(f"{self.title} Mean z={round(mean(beam.z), 3)} m")
        self.axs.set_xlabel('x [mm]')
        self.axs.set_ylabel('y [mm]')
        self.axs.set(xlim =[self.left_xaxis, self.right_xaxis], ylim = [self.left_yaxis, self.right_yaxis])
        
        self.frameCount = self.axs.text(self.right_xaxis-1, self.right_yaxis+0.4, f'Frame: {init_frame}')
        pix = np.flipud(data.T)
        self.im = plt.imshow(pix, extent=[x[0], x[-1], y[0], y[-1]])
        self.axs.clear()
        self.run(title=self.title, **kwargs)

    def animate(self, i):
        plt.cla()
        beam = self.astra.particles[i]
        X = beam.x*10**3
        Y = beam.y*10**3
        data, x, y, _ = plt.hist2d(X, Y, self.num_bins, cmin=1)
        self.axs.set_title(f"{self.title} Mean z={round(mean(beam.z), 3)} m")
        self.axs.set(xlim =[self.left_xaxis, self.right_xaxis], ylim = [self.left_yaxis, self.right_yaxis])
        self.axs.set_xlabel('x [mm]')
        self.axs.set_ylabel('y [mm]')
        self.frameCount.set_text(f'Frame: {i}')
        pix = np.flipud(data.T)
        self.im.set_data(pix)
        self.im.set_extent([x[0], x[-1], y[0], y[-1]])
    
    def run(self, title=''):
        num = len(self.astra.particles)
        playback_speed = 6 #In fps
        anim = animation.FuncAnimation(self.fig, self.animate, np.arange(1,num), repeat_delay = 2500, repeat = False)

        #Save animation
        writervideo = animation.FFMpegWriter(fps=playback_speed)
        save_path = os.path.join(self.animations_path, f'{self.name}.mp4')
        anim.save(save_path, writer=writervideo)
        plt.close()
    