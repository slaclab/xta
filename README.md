# xta
Simulations for xta beam line in TID

## Path definitions

Before any simulations can be run, environment path variables for astra must be defined. To set up a simulation, four directory paths must be defined: xta_path, sim_path, init_dcm_path, and vcc_path.

### xta_path

This is the path of the xta repository on the local machine.

### sim_path

The simulations directory where all data will be saved.

### init_dcm_path

The path of the .dcm file to be loaded into the simulation.

### vcc_path

The directory containing the example vcc laser images.

## xta_sim

The xta_sim object contains all the necessary functions and methods to configure/run simulations and save/plot the data. The following methods are defined:

### .generate_dist(index)

This method generates the initial electron distribution based on the laser image and the tumor image using distgen. The index argument indicates which laser image to choose from library.

### .simulation(type)
This method runs a simulation with the current xta_sim configuration. A simulation type is passed as an argument; simulation arguments are also passed based on the simulation type.

#### Types of Simulations:
'single': runs one simulation
'scan': optimizes a simulation input by running a single scan over a linear space with a defined interval and discrete divisions. Required arguments: optimization parameter, interval, divisions.
'cont_scan': runs single scans until parameter is optimized to a specified decimal precision. Required arguments: optimization parameter, interval, divisions, precision.

### .plot
This method is responsible for generating the prebuilt plot types.

#### Keyword Arguments
The save arguement is responsible for saving the plot to the plots folder in the simulation. The close argument is responsible for closing the plot. Normal keyword arguments from matplotlib can be passed for single plot types.

### Types of Prebuilt Plots:

#### Single Plots:
'laser_image': the laser image
'initial_dist': the initial electron distribution
'final_dist': the final electron distribution
'rotated_final_dist': the final electron distribution with the rotation correction

#### Compare Plots:
'initial_vs_final': initial vs final electron distributions
'initial_vs_rotated': initial vs final electron distributions with final rotation correction

### .movie
This method generates a movie of the entire simulation. The .mp4 is saved to the animations directory.

## Todo

### Automatic Plot Axes
Currently the plot axes must be configured manually in xta.py, automatic axes calculations need to be developed.

### Plot Kwargs
Need to configure xta.py and plot.py to allow for matplotlib kwargs to be passed for  all plot types.