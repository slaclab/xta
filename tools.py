"""
Tools and Functions
"""

import os
import matplotlib as plt
import numpy as np
import pandas as pd
import shutil
import scipy
import pydicom as dicom

def parse_opal_emitted_dist(filename, names=['x', 'px','y','py','t','pz']):
    '''Read in particle distribution used 
    in OPAL-T simulation. Used to describe the 
    beam distribution as it leaves the cathode.'''
    dist = {}
    data = np.loadtxt(filename, skiprows=1)
    for i,name in enumerate(names):
        dist[name] = data[:,i]
    return dist
    
def parse_astra_dist(filename, header=['x', 'y', 'z', 'px','py', 'pz', 't', 'Q', 'ptype', 'flag']):
    '''
    Read in initial particle distribution used 
    in ASTRA simulation. Used to describe the 
    beam distribution as it leaves the cathode.
   
    t     = time in ns
    Q     = macro charge
    ptype = particle type (electron: 1)
    flag  = particle location (cathode: -1)
    '''
    #print(filename)
    data = pd.read_csv(filename, delim_whitespace=True, names=header)
    #print(data)
    #only return non traj probe particles at cathodeprint(astradist['z'])
    dist = data[data.flag == -1]
    return dist #dist

def make_tri(n, xmin, xmax, x):

    half = int(n/2)
    yr  = np.zeros(half*2)
    #step 1
    nr = int(n)
    xr = np.random.rand(nr)

    for j in range(0,nr):
        #step 3
        if j < half:
            yr[j] = (1- np.sqrt(1-xr[j]))*(xmax-xmin)  
        elif j >= half:
        #step 4 
            yr[j] = (-1 + np.sqrt(1-xr[j]))*(xmax-xmin) 

    #showplot(xr, yr)
    for k in range(0,len(x)):
        #print(y[k])
        if (-yr[k]/8 <= x[k] <= yr[k]/8):
            pass
            #x[k]=0
        else:
            #print(x[k])
            x[k]=0
            #pass

    #showplot(xr,x)
    return x, xr

# From Chris: https://github.com/slaclab/lcls-lattice/tree/master/distgen/models/cu_inj/vcc_image
def write_distgen_xy_dist(filename, image, resolution, resolution_units='m'):
    """
    Writes image data in distgen's xy_dist format
    
    Returns the absolute path to the file written
    
    """
    
    # Get width of each dimension
    widths = resolution * np.array(image.shape)
    
    # Form header
    header = f"""x {widths[1]} {widths[1]/2} [{resolution_units}]
y {widths[0]} {widths[0]/2}  [{resolution_units}]"""
    
    # Save with the correct orientation
    np.savetxt(filename, np.flip(image, axis=0), header=header, comments='')
    
    return os.path.abspath(filename)

#Loads and returns reshaped laser image based on index
def laser_load(vcc, index):
    mat = scipy.io.loadmat(vcc[index])
    #Scraping Name of File
    laser_name = str(mat['data'][0][0][0][0])

    #Image Reshaping
    arr = mat['data']
    dim = arr.shape[0]
    #print(dim)
    xy = int(np.sqrt(dim))
    nrow = xy
    ncol = xy
    return arr.reshape(nrow, ncol)[0][0][1], xy, laser_name

def sim_mkdir(init_dcm_path, sim_path, name):

    #makes scan directory
    os.mkdir(os.path.join(sim_path, name))
    scan_path = os.path.join(sim_path, name)

    #makes data and plots directory
    global data_path, plots_path, image_name
    image_name = name
    data_path = os.path.join(scan_path, 'data')
    plots_path = os.path.join(scan_path, 'plots')
    
    os.mkdir(data_path)
    os.mkdir(plots_path)

    #defining directories to add to data and plots
    
    #directories used b y functions
    data_dirs = ['dcm_crop', 'cont_scan']
    #plot directories
    plots_dirs = ['animations', 'compare_dist',  'energy_dist', 'final_electron_dist', 'init_electron_dist', 'laser_images', 'compare_dist_rotated']
    for dir in data_dirs:
        os.mkdir(os.path.join(data_path, dir))
    for dir in plots_dirs:
        os.mkdir(os.path.join(plots_path, dir))

    #copies .dcm to scan_path directory
    shutil.copy2(init_dcm_path, scan_path)
    return [data_path, plots_path]

def dcm_crop(im_input):
    ds = dicom.dcmread(im_input)
    pixArr = ds.pixel_array
    dim = pixArr.shape
    height, width = dim[0], dim[1]

    #pixel crop threshold 5000
    x, y = np.where(pixArr > 5000)
    xl, xr = x.min(), x.max()
    yl, yr = y.min(), y.max()
    crop = pixArr[xl:xr, yl:yr]
    
    #Pad to preserve original shape
    padx = (height - crop.shape[0])//2
    pady = (width - crop.shape[1])//2
    padImg = np.pad(crop, [(padx, padx), (pady, pady)], mode='constant')

    save_path = f'{data_path}/dcm_crop/{image_name}.jpg'
    plt.imsave(save_path, padImg)
    return save_path
