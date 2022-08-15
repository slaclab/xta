import os
import matplotlib.pyplot as plt
import numpy as np
from tools import rotate_particles
import matplotlib.animation as animation
from statistics import mean

#Global Default Settings
save = True
close = False

def save_plot(filename):
    
    plt.savefig(filename, dpi=300, bbox_inches='tight')

def laser_image(data, **kwargs):
    plt.figure(figsize=(5, 5))
    plt.imshow(data['laser_IMAGE'])
    plt.title(data['laser_name'])
    plt.xlabel('Pixel')
    plt.ylabel('Pixel')
    if save:
        savepath = os.path.join(data['plots_path'], 'laser_images', data['laser_name']+'.jpg')
        save_plot(savepath)
    if close:
        plt.close()

def initial_dist(data, **kwargs):
    plt.figure(figsize=(5, 5))
    plt.hist2d(data['astra'].particles[0].x*10**3, data['astra'].particles[0].y*10**3, data['num_bins'], facecolor='blue', cmin=1)
    plt.title('Initial Electron Distribution')
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.xlim(data['axes']['left_xaxis'], data['axes']['right_xaxis'])
    plt.ylim(data['axes']['left_yaxis'], data['axes']['right_yaxis'])
    if save:
        savepath = os.path.join(data['plots_path'], 'laser_images', 'initial_dist.jpg')
        save_plot(savepath)
    if close:
        plt.close()

def final_dist(data, **kwargs):
    plt.figure(figsize=(5, 5))
    plt.hist2d(data['astra'].particles[-1].x*10**3, data['astra'].particles[-1].y*10**3, data['num_bins'], facecolor='blue', cmin=1)
    plt.title('Final Electron Distribution')
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.xlim([data['axes']['left_xaxis'], data['axes']['right_xaxis']])
    plt.ylim([data['axes']['left_yaxis'], data['axes']['right_yaxis']])
    if save:
        savepath = os.path.join(data['plots_path'], 'laser_images', 'final_dist.jpg')
        save_plot(savepath)
    if close:
        plt.close()

def rotated_final_dist(data, **kwargs):
    rotVect = rotate_particles(data['astra'], -1)

    plt.figure(figsize=(5, 5))
    plt.hist2d(rotVect[0], rotVect[1], data['num_bins'], facecolor='blue', cmin=1)
    plt.title('Rotated Final Electron Distribution')
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.xlim([data['axes']['left_xaxis'], data['axes']['right_xaxis']])
    plt.ylim([data['axes']['left_yaxis'], data['axes']['right_yaxis']])
    if save:
        savepath = os.path.join(data['plots_path'], 'laser_images', 'rotated_final_dist.jpg')
        save_plot(savepath)
    if close:
        plt.close()

def initial_vs_final(data, title='', **kwargs):
    #Super plot
    fig, plots = plt.subplots(1, 2, figsize=(10, 5), sharex=True, sharey=True)
    fig.subplots_adjust(wspace=0.2)

    #Final plot
    finalxy = plt.subplot(1,2,2)
    plt.hist2d(data['astra'].particles[-1].x*10**3, data['astra'].particles[-1].y*10**3, data['num_bins'], facecolor='blue', cmin=1)
    plots[1].set(title='Final Shape', xlabel='x [mm]')

    #Initial Plot
    initialxy = plt.subplot(1,2,1)
    plt.hist2d(data['astra'].particles[0].x*10**3, data['astra'].particles[0].y*10**3, data['num_bins'], facecolor='blue', cmin=1)
    plots[0].set(title='Initial Shape', xlabel='x [mm]', ylabel='y [mm]', xlim=[data['axes']['left_xaxis'], data['axes']['right_xaxis']], ylim=[data['axes']['left_yaxis'], data['axes']['right_yaxis']])

    plt.suptitle(title)

    if save:
        savepath = os.path.join(data['plots_path'], 'laser_images', 'initial_vs_final.jpg')
        save_plot(savepath)
    if close:
        plt.close()


def initial_vs_rotated(data, title='', **kwargs):
    #Super plot
    fig, plots = plt.subplots(1, 2, figsize=(10, 5), sharex=True, sharey=True)
    fig.subplots_adjust(wspace=0.2)

    rotVect = rotate_particles(data['astra'], -1)
    #Final plot
    finalxy = plt.subplot(1,2,2)
    plt.hist2d(rotVect[0], rotVect[1], data['num_bins'], facecolor='blue', cmin=1)
    plots[1].set(title='Final Rotated Shape', xlabel='x [mm]')

    #Initial Plot
    initialxy = plt.subplot(1,2,1)
    plt.hist2d(data['astra'].particles[0].x*10**3, data['astra'].particles[0].y*10**3, data['num_bins'], facecolor='blue', cmin=1)
    plots[0].set(title='Initial Shape', xlabel='x [mm]', ylabel='y [mm]', xlim=[data['axes']['left_xaxis'], data['axes']['right_xaxis']], ylim=[data['axes']['left_yaxis'], data['axes']['right_yaxis']])

    plt.suptitle(title)

    if save:
        savepath = os.path.join(data['plots_path'], 'laser_images', 'initial_vs_rotated.jpg')
        save_plot(savepath)
    if close:
        plt.close()
        
plotTypes = {
    'laser_image': laser_image,
    'initial_dist': initial_dist,
    'final_dist': final_dist,
    'rotated_final_dist': rotated_final_dist,
    'initial_vs_final': initial_vs_final,
    'initial_vs_rotated': initial_vs_rotated,
}
