import matplotlib.pyplot as plt
from statistics import mean
import matplotlib.animation as animation
import numpy as np
import os

def movie(data, **kwargs):

    #Initial histogram
    fig, axs = plt.subplots(figsize=(5, 5))
    init_frame = 0
    beam = data['astra'].particles[init_frame]

    arr, x, y, _ = axs.hist2d(beam.x*10**3, beam.y*10**3, data['num_bins'], cmin=1)
    axs.set_title(f'Mean z={round(mean(beam.z), 3)} m')
    axs.set_xlabel('x [mm]')
    axs.set_ylabel('y [mm]')
    axs.set(xlim = [data['axes']['left_xaxis'], data['axes']['right_xaxis']], ylim = [data['axes']['left_yaxis'], data['axes']['right_yaxis']])
    
    frameCount = axs.text(data['axes']['right_xaxis']-1, data['axes']['right_yaxis']+0.4, f'Frame: {init_frame}')
    pix = np.flipud(arr.T)
    im = plt.imshow(pix, extent=[x[0], x[-1], y[0], y[-1]])
    axs.clear()

    def animate(i):
        plt.cla()
        beam = data['astra'].particles[i]
        X = beam.x*10**3
        Y = beam.y*10**3
        arr, x, y, _ = plt.hist2d(X, Y, data['num_bins'], cmin=1)
        axs.set_title(f'Mean z={round(mean(beam.z), 3)} m')
        axs.set(xlim =[data['axes']['left_xaxis'], data['axes']['right_xaxis']], ylim = [data['axes']['left_yaxis'], data['axes']['right_yaxis']])
        axs.set_xlabel('x [mm]')
        axs.set_ylabel('y [mm]')
        frameCount.set_text(f'Frame: {i}')
        pix = np.flipud(arr.T)
        im.set_data(pix)
        im.set_extent([x[0], x[-1], y[0], y[-1]])
    
    num = len(data['astra'].particles)
    playback_speed = 6 #In fps
    anim = animation.FuncAnimation(fig, animate, np.arange(1,num), repeat_delay = 2500, repeat = False)

    #Save animation
    writervideo = animation.FFMpegWriter(fps=playback_speed)
    savepath = os.path.join(data['plots_path'], 'animations', data['name']+'.mp4')
    anim.save(savepath, writer=writervideo)
    plt.close()
    