import os
from tools import rotate_particles, subtractImg
import numpy as np
import matplotlib.pyplot as plt

class scan:
    def __init__(self, astra, parameter, range, divisions, precision = 2):
        self.astra = astra
        self.parameter = parameter #list of xta.in parameter to be optimized
        self.min, self.max = range
        self.divisions = divisions
        self.precision = precision
        self.sub_bins = 42 #Number of bins for image subtraction

        self.left_xaxis, self.right_xaxis, self.left_yaxis, self.right_yaxis = self.defineAxes()

        self.scoreDict = {}
        self.opt_val = self.scan()
        return self.opt_val

    def defineAxes(self):
        axes = [-10, 10, -10, 10]
        return axes
    
    #How the function scores the image
    def score(img):
        sumPixels = img.sum()
        squareSum = np.square(img).sum()
        return sumPixels

    def run(self, parameter, val):
        self.astra.input[f'{parameter[0]}'][f'{parameter[1]}'] = val
        self.astra.run()
        rotVect = rotate_particles(self.astra, -1)
        
        fig, ax = plt.subplots(figsize=(5, 5), frameon=False)
        plt.hist2d(self.astra.particles[0].x, self.astra.particles[0].y, self.sub_bins, facecolor='blue', cmin=1)
        ax.set(xlim=[self.left_xaxis, self.right_xaxis], ylim=[self.left_yaxis, self.right_yaxis])
        fig.canvas.draw()
        ncols, nrows = fig.canvas.get_width_height()
        initIm = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8).reshape(nrows, ncols, 3)
        plt.close()

        fig, ax = plt.subplots(figsize=(5, 5), frameon=False)
        plt.hist2d(rotVect[0], rotVect[1], self.sub_bins, facecolor='blue', cmin=1)
        ax.set(xlim=[self.left_xaxis, self.right_xaxis], ylim=[self.left_yaxis, self.right_yaxis])
        fig.canvas.draw()
        ncols, nrows = fig.canvas.get_width_height()
        finIm = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8).reshape(nrows, ncols, 3)
        #fig.savefig(f'{data_path}/cont_scan/final_{image_name}.jpg', bbox_inches='tight', pad_inches=0)
        #plt.imsave('test.jpg', finIm)
        plt.close()
        subImg = subtractImg(initIm, finIm)
        #subImg = plt.imread(f'{data_path}/cont_scan/diff_{image_name}.jpg')
        return self.score(subImg)

    def scan(self):
        if self.divisions <= 3:
            raise ValueError('There must be more than 3 divisions!')
        parameter_space = np.linspace(self.min, self.max, self.divisions)
        opt_val = self.min
        opt_score = 1e9
        for val in parameter_space:
            if val in self.scoreDict.keys():
                score = self.scoreDict[val]
            else:
                score = self.run(self.parameter, val)
                self.scoreDict[val] = score
            if score > opt_score:
                if val > opt_val:
                    self.max = val
                    break
                continue
            elif parameter_space[-1] == val:
                raise ValueError('Upper limit is optimal limit, increase upper limit for proper scan!')
            self.min = opt_val
            opt_val = val
            opt_score = score

        return self.opt_val, self.min, self.max

class cont_scan:
    def __init__(self, astra, parameter, init_domain, divisions, precision):
        self.astra = astra
        self.parameter = parameter
        self.min, self.max = init_domain
        self.divisions = divisions
        self.precision = precision
        return self.cont_scan()

    def cont_scan(self):
        while round(self.min, self.precision) != round(self.max, self.precision):
            self.opt_val, self.min, self.max = scan(self.astra, self.parameter, self.min, self.max, self.divisions, self.precision)
        return self.opt_val