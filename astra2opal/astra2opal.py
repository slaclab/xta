from pmd_beamphysics.units import unit
import os
import re
from math import isnan
import numpy as np

debug = 1
# Converting ASTRA .in input files into Properly Formatted OPAL .in input files.
dirname = os.path.dirname(__file__)
# Firstly we will need to create a dictionary object in which to put the data we are reading

# TESTING GROUNDS
# -------------------------------------------------------------------------------------------------------------
# Thank you, Christopher Mayes

# ------ Number parsing ------
def isfloat(value):
      try:
            float(value)
            return True
      except ValueError:
            return False

def isbool(x):        
    z = x.strip().strip('.').upper()
    if  z in ['T', 'TRUE', 'F', 'FALSE']:
        return True
    else:
        return False
    
def try_int(x):
    if x == int(x):
        return int(x)
    else:
        return x

def try_bool(x):
    z = x.strip().strip('.').upper()
    if  z in ['T', 'TRUE']:
        return True
    elif z in ['F', 'FALSE']:
        return False
    else:
        return x

# Simple function to try casting to a float, bool, or int
def number(x):
    z = x.replace('D', 'E') # Some floating numbers use D
    if isfloat(z):
        val =  try_int(float(z))
    elif isbool(x):
        val = try_bool(x)
    else:
        # must be a string. Strip quotes.
        val = x.strip().strip('\'').strip('\"')
    return val    

# ------ Astra input file (namelist format) parsing
def clean_namelist_key_value(line):
    """
    Cleans up a namelist "key = value line"
    
    """
    z = line.split('=')
    # Make key lower case, strip
    return z[0].strip().lower()+' = '+''.join(z[1:])

def unroll_namelist_line(line, commentchar='!', condense=False ):
    """
    Unrolls namelist lines. Looks for vectors, or multiple keys per line. 
    """
    lines = [] 
    # Look for comments
    x = line.strip().strip(',').split(commentchar)
    if len(x) ==1:
        # No comments
        x = x[0].strip()
    else:
        # Unroll comment first
        comment = ''.join(x[1:])
        if not condense:
            lines.append('!'+comment)
        x = x[0].strip()
    if x == '':
        pass    
    elif x[0] == '&' or x[0]=='/':
        # This is namelist control. Write.
        lines.append(x.lower())
    else:
        # Content line. Should contain = 
        # unroll.
        # Check for multiple keys per line, or vectors.
        # TODO: handle both
        n_keys = len(x.split('='))
        if n_keys ==2:
            # Single key
            lines.append(clean_namelist_key_value(x))
        elif n_keys >2:
            for y in x.strip(',').split(','):
                lines.append(clean_namelist_key_value(y))

    return lines

def parse_simple_namelist(filePath, commentchar='!', condense=False ):
    """
    Unrolls namelist style file. Returns lines.
    makes keys lower case
    
    Example:
    
    &my_namelist
    
        x=1, YY  = 4 ! this is a comment:
    /
    
    unrolls to:
    &my_namelist
    ! this is a comment
        x = 1
        yy = 4
    /
    
    """
    
    lines = []
    with open(filePath, 'r') as f:
        if condense:
            pad = ''
        else:
            pad = '    '
        
        for line in f:
            ulines = unroll_namelist_line(line, commentchar=commentchar, condense=condense)
            lines = lines + ulines

            
    return lines

def parse_unrolled_namelist(unrolled_lines):
    """
    Parses an unrolled namelist into a dict
    
    """
    namelists={}
    for line in unrolled_lines:
        if line[0]=='1' or line[0]=='/' or line[0]=='!':
            # Ignore
            continue
        if line[0]=='&':
            name = line[1:].lower()
            namelists[name]={}
            # point to current namelist
            n = namelists[name]
            continue
        # content line
        key, val = line.split('=')
        
        # look for vector
        vals = val.split()
        if len(vals) == 1:
            val = number(vals[0])
        else:
            if isfloat(vals[0].replace(',',' ')):
                # Vector. Remove commas
                val = [number(z) for z in val.replace(',',' ').split()] 
            else:
                # This is just a string. Just strip
                val = val.strip()
        n[key.strip()] = val
        
        
    return namelists

def parse_astra_input_file(filePath, condense=False):
    """
    Parses an Astra input file into separate dicts for each namelist. 
    Returns a dict of namelists. 
    """
    lines = parse_simple_namelist(filePath, condense=condense)
    namelists = parse_unrolled_namelist(lines)
    return namelists
# -------------------------------------------------------------------------------------------------------------

input = parse_astra_input_file(dirname + '/xta.in')
#print(input)



# -------------------------------------------------------------------------------------------------------------
# (OPTIONAL) We would like to be able to reverse this process, so we will also need to read the OPAL file.

# Next we will need to prepare the (string?) to be written to file, properly formatted OPAL .in

# (OPTIONAL) We would like to be able to write a properly formatted ASTRA .in file

# Finally a simple, reliable write function that accepts the input string and translates it to a file on disk.


# We must write the data to file in the proper format, so that we can reliably complete the conversion process
# TEST AREA
#-------------------------------------------------------------------------------------------------------------


# This is the beginning of implementation of the OPAL .in file for an LCLS II (logic - if we can print it in the
# correct format to console, all of it can be easily wrapped into functions and written to file)
# Also, this is a way to determine and identify what variables to look for in ASTRA .in files.

# Gathering a list of variables
bEcho = "FALSE"
bInfo = "FALSE"
psDumpFreq = 300000000
statDumpFreq = 10
autoPhase = 4
versionNo = 20200
enableHDF5 = "TRUE"
sTitle = "LCLS2"
rfFreq = "187.0e6"
nParticles = "5e4"
beamBunchCharge = "100.0*1e-12"
beamCurrent = "rf_freq*beam_bunch_charge*1e6"
fEDes = "1.4e-9"
vGamma = "(Edes+EMASS)/EMASS"
vBeta = "sqrt(1-(1/gamma^2))"
vP0 = "gamma*beta*EMASS"
gunL = 0.199
gunVolt = 20.0
gunElemEdge = 0.0
gunType = "STANDING"
gunFreq = 87.0
gunLag = "8.5*deg"
buncherL = 0.358
buncherVolt = 1.8
buncherElemEdge = 0.809116
buncherType = "STANDING"
buncherFreq = 1300.0
buncherLag = "-88.5*deg"
solBFL = 0.48
solBFElemEdge = -0.062
solBFKS = 0.0
sol1L = 0.48
sol1ElemEdge = 0.24653
sol1KS = 0.056
sol2L = 0.48
sol2ElemEdge = 1.64581
sol2KS = 0.03
vLCav = 1.3836
vD1 = 3.3428
vD2 = "d1 + lcav"
vD3 = "d2 + lcav"
vD4 = "d3 + lcav"
vD5 = "d4 + lcav"
vD6 = "d5 + lcav"
vD7 = "d6 + lcav"
vD8 = "d7 + lcav"
vDeg = "PI/180.0"
#
c1L = 1.3836 
c1Volt = 11.0
c1ElemEdge = "d1"
c1Type = "STANDING"
c1Freq = "1.3e3"
c1Lag = "8*deg"
#
c2L = 1.3836
c2Volt = "1.0E-5"
c2ElemEdge = "d2"
c2Type = "STANDING"
c2Freq = "1.3e3"
c2Lag = "-9.0*deg"
#
c3L = 1.3836
c3Volt = "26.0"
c3ElemEdge = "d3"
c3Type = "STANDING"
c3Freq = "1.3e3"
c3Lag = "-20.0*deg"
#
c4L = 1.3836
c4Volt = "24.0"
c4ElemEdge = "d4"
c4Type = "STANDING"
c4Freq = "1.3e3"
c4Lag = "-18.0*deg"
#
c5L = 1.3836
c5Volt = "32.0"
c5ElemEdge = "d5"
c5Type = "STANDING"
c5Freq = "1.3e3"
c5Lag = "0.0*deg"
#
c6L = 1.3836
c6Volt = "32.0"
c6ElemEdge = "d6"
c6Type = "STANDING"
c6Freq = "1.3e3"
c6Lag = "0.0*deg"
#
c7L = 1.3836
c7Volt = "32.0"
c7ElemEdge = "d7"
c7Type = "STANDING"
c7Freq = "1.3e3"
c7Lag = "0.0*deg"
#-------------------------------------------------------------------------------------------------------------
c8L = 1.3836
c8Volt = "32.0"
c8ElemEdge = "d8"
c8Type = "STANDING"
c8Freq = "1.3e3"
c8Lag = "10.0*deg"
#
print('OPTION, ECHO=' + bEcho + ';') 
print('OPTION, INFO=' + bInfo + ';		//psdump and statdump are in time steps')
print('OPTION, STATDUMPFREQ = ' + str(statDumpFreq) + ';	//How often beam stats dumped to .stat.')  
print('OPTION, PSDUMPFREQ = ' + str(psDumpFreq) + ';')
print('OPTION, AUTOPHASE=' + str(autoPhase) + ';		//Always leave this on, unless doing a phase scan')
print('Option, VERSION=' + str(versionNo) + ';')
print('Option, ENABLEHDF5=' + enableHDF5 + ';') 
print('\n') 
print('Title, string="' + sTitle + '";')
print('\n')
print('//------------------------------------------------------------------------')
print('//					Global Parameters')
print('\n')
print('REAL rf_freq         	     = ' + rfFreq + ';        //RF frequency. (Hz)')
print('REAL n_particles             = ' + nParticles + ';            //Number of particles in simulation.')
print('REAL beam_bunch_charge       = ' + beamBunchCharge + ';    //Charge of bunch. (C)')
print('REAL beam_current            = ' + beamCurrent + ';')
print('\n')
print('//Initial energy Calc')
print('REAL Edes    = ' + fEDes + ';')
print('REAL gamma   = ' + vGamma + ';')
print('REAL beta    = ' + vBeta + ';')
print('REAL P0      = ' + vP0 + ';')
print('\n')
print('value , {' + fEDes + ', ' + vP0 + '};') 					
print('\n')
print('//Input components for LCLS2 - EIC area')
print('//-------------------------------------------------------------------------------------')
print('// Gun')
print('//')
print('// Cavity/RF field.')
print('//')
print('// L:           physical element length (real in m). Length (of field map) (m).')
print('// VOLT:        field scaling factor (real). RF field magnitude (MV/m).')
print('// FMAPFN:      field file name (string)')
print('// ELEMEDGE:        physical start of the element on the floor (real in m)')
print('// TYPE:        specifies "STANDING" (default), "TRAVELLING" or "SINGLE GAP" structure')
print('// FREQ:        RF frequency of cavity (real in MHz). Resonance frequency.')
print('// LAG:         cavity phase (radians)')
print('//')
print('\n')
print('REAL deg=PI/180.0;')
print('\n')
print('GUN:    RFCavity, L = ' + gunL + ', VOLT = ' + gunVolt + ', ELEMEDGE = ' + gunElemEdge + ', TYPE = "' + gunType + '", FMAPFN = "../../fieldmaps/rfgunb_187MHz.txt", FREQ = ' + gunFreq + ', LAG = ' + gunLag + ';')
print('\n')
print('// Buncher field map has z = -0.179 to 0.179')
print('// Element edge should be center of device')
print('BUNCHER:    RFCavity, L = ' + buncherL + ', VOLT = ' + buncherVolt + ', ELEMEDGE = ' + buncherElemEdge + ', TYPE = "' + buncherType + '", FMAPFN = "../../fieldmaps/rfgunb_buncher.txt", FREQ = ' + buncherFreq + ', LAG = ' + buncherLag + ';')
print('\n')
print('//-------------------------------------------------------------------------------------')
print('// Solenoids')
print('//')
print('// L:           Physcial element length (m)')
print('// ELEMEDGE:    Physcial start of element (m)')
print('// KS:          Solenoid strength (T/m)')
print('// FMAPFM:      Field file (string)')
print('\n')
print('// realbucking Field map has z = -2.5 to 2.5')
print('// Element edge should be center of device')
print('SOLBF:  Solenoid, L = ' + solBFL + ', ELEMEDGE= ' + solBFElemEdge + ', KS = ' + solBFKS + ', FMAPFN = "/fieldmaps/rfgunb_bucking.txt";')
print('\n')
print('// newSOL Field map has z = -0.24 to 0.24')
print('// Element edge should be center of device')
print('SOL1:   Solenoid, L = ' + sol1L + ', ELEMEDGE= ' + sol1ElemEdge + ', KS = ' + sol1KS + ', FMAPFN = "../../fieldmaps/rfgunb_solenoid.txt";')
print('\n')
print('SOL2:   Solenoid, L = ' + sol2L + ', ELEMEDGE= ' + sol2ElemEdge + ', KS = ' + sol2KS + ', FMAPFN = "../../fieldmaps/rfgunb_solenoid.txt";')
print('\n')
print('\n')
print('EIC:  Line = (GUN, SOL1, BUNCHER, SOL2);')
print('\n')
print('\n')
print('//Input components for LCLS2 - Cryomodule 1')
print('//-------------------------------------------------------------------------------------')
print('// Cryomodule 1')
print('//')
print('// Cavity/RF field.')
print('//')
print('// L:           physical element length (real in m). Length (of field map) (m).')
print('// VOLT:        field scaling factor (real). RF field magnitude (MV/m).')
print('// FMAPFN:      field file name (string)')
print('// ELEMEDGE:        physical start of the element on the floor (real in m)')
print('// TYPE:        specifies "STANDING" (default), "TRAVELLING" or "SINGLE GAP" structure')
print('// FREQ:        RF frequency of cavity (real in MHz). Resonance frequency.')
print('// LAG:         cavity phase (radians)')
print('//')
print('\n')
print('REAL lcav = ' + vLCav + ';')
print('\n')
print('REAL d1 = ' + vD1 + ';')
print('REAL d2 = ' + vD2 + ';')
print('REAL d3 = ' + vD3 + ';')
print('REAL d4 = ' + vD4 + ';')
print('REAL d5 = ' + vD5 + ';')
print('REAL d6 = ' + vD6 + ';')
print('REAL d7 = ' + vD7 + ';')
print('REAL d8 = ' + vD8 + ';')
print('REAL deg = ' + vDeg + ';')
print('\n')
print('C1: RFCavity, L = ' + c1L + ', VOLT = ' + c1Volt + ', ELEMEDGE = ' + c1ElemEdge + ', TYPE = "' + c1Type + '", FMAPFN = "../../fieldmaps/L0B_9cell.txt", FREQ = ' + c1Freq + ', LAG = ' + c1Lag + ';')
print('\n')
print('C2: RFCavity, L = ' + c2L + ', VOLT = ' + c2Volt + ', ELEMEDGE = ' + c2ElemEdge + ', TYPE = "' + c2Type + '", FMAPFN = "../../fieldmaps/L0B_9cell.txt", FREQ = ' + c2Freq + ', LAG = ' + c2Lag + ';')
print('\n')
print('C3: RFCavity, L = ' + c3L + ', VOLT = ' + c3Volt + ', ELEMEDGE = ' + c3ElemEdge + ', TYPE = "' + c3Type + '", FMAPFN = "../../fieldmaps/L0B_9cell.txt", FREQ = ' + c3Freq + ', LAG = ' + c3Lag + ';')
print('\n')
print('C4: RFCavity, L = ' + c4L + ', VOLT = ' + c4Volt + ', ELEMEDGE = ' + c4ElemEdge + ', TYPE = "' + c4Type + '", FMAPFN = "../../fieldmaps/L0B_9cell.txt", FREQ = ' + c4Freq + ', LAG = ' + c4Lag + ';')
print('\n')
print('C5: RFCavity, L = ' + c5L + ', VOLT = ' + c5Volt + ', ELEMEDGE = ' + c5ElemEdge + ', TYPE = "' + c5Type + '", FMAPFN = "../../fieldmaps/L0B_9cell.txt", FREQ = ' + c5Freq + ', LAG = ' + c5Lag + ';')
print('\n')
print('C6: RFCavity, L = ' + c6L + ', VOLT = ' + c6Volt + ', ELEMEDGE = ' + c6ElemEdge + ', TYPE = "' + c6Type + '", FMAPFN = "../../fieldmaps/L0B_9cell.txt", FREQ = ' + c6Freq + ', LAG = ' + c6Lag + ';')
print('\n')
print('C7: RFCavity, L = ' + c7L + ', VOLT = ' + c7Volt + ', ELEMEDGE = ' + c7ElemEdge + ', TYPE = "' + c7Type + '", FMAPFN = "../../fieldmaps/L0B_9cell.txt", FREQ = ' + c7Freq + ', LAG = ' + c7Lag + ';')
print('\n')
print('C8: RFCavity, L = ' + c8L + ', VOLT = ' + c8Volt + ', ELEMEDGE = ' + c8ElemEdge + ', TYPE = "' + c8Type + '", FMAPFN = "../../fieldmaps/L0B_9cell.txt", FREQ = ' + c8Freq + ', LAG = ' + c8Lag + ';')
print('\n')
print('CM1:  Line = (C1,C2,C3,C4,C5,C6,C7,C8);')
print('\n')
# DR1: DRIFT, L = 5.0, ELEMEDGE = 13.0; 
print('\n')
print('//--------------------------------------------------------------------------------')
print('// Accelerator lines')
#-------------------------------------------------------------------------------------------------------------
cm1Line = "C1,C2,C3,C4,C5,C6,C7,C8"
# Col:ECOLLIMATOR, L=15.0, ELEMEDGE=0.0, XSIZE=30E-3,
#     YSIZE=30E-3, OUTFN="col.h5";
print('\n')
# SC_INJ:  Line = (Col, EIC, CM1, DR1);
print('//-------------------------------------------------------------------------------------')
print('\n')
print('//// Distribution definition')
#-------------------------------------------------------------------------------------------------------------

# Dist:DISTRIBUTION, TYPE = FROMFILE,
#                    FNAME = "opal_50k.txt",
#                    EMITTED = TRUE,
#                    EMISSIONMODEL = NONE,
#                    EMISSIONSTEPS = 100,
#                    EKIN=0;
print('\n')
print('//Dist:DISTRIBUTION, TYPE = GAUSS,')
print('//                   SIGMAR = 0.000168,')
print('//                   TRISE = 14.2e-12,')
print('//                   TFALL = 14.2e-12,')
print('//                   CUTOFFLONG = 4.0,')
print('//                   NBIN = 5,')
print('//                   EMISSIONSTEPS = 100,')
print('//                   EMISSIONMODEL = ASTRA,')
print('//                   EKIN = 0.5,')
print('//                   EMITTED = TRUE, ')
print('//                   WRITETOFILE = TRUE;')
print('\n')
print('\n')
print('//-------------------------------------------------------------------------------------')
print('// Define Field solvers')
print('// The mesh sizes should be a factor of 2 for most efficient space charge (SC) calculation.')
print('\n')
#-------------------------------------------------------------------------------------------------------------

# FS_SC: Fieldsolver, FSTYPE = FFT, 
#                     MX = 32, MY = 32, MT = 32,
# 		            PARFFTX = false, 
# 		            PARFFTY = false, 
# 		            PARFFTT = true,#
# 		            BCFFTX = open, 
# 		            BCFFTY = open, 
# 		            BCFFTT = open,
# 		            BBOXINCR = 1, 
# 		            GREENSF = INTEGRATED;
print('\n')
print('//-------------------------------------------------------------------------------------')
print('// Beam Definition')
print('\n')
#-------------------------------------------------------------------------------------------------------------

# BEAM1: BEAM, PARTICLE = ELECTRON,
#        pc = P0, NPART = n_particles, BFREQ = rf_freq,
#        BCURRENT = beam_current, CHARGE = -1;
print('\n')
print('//-------------------------------------------------------------------------------------')
print('// Run beamline')
print('\n')
#-------------------------------------------------------------------------------------------------------------

# TRACK, LINE = SC_INJ, BEAM = BEAM1, MAXSTEPS = 1900000, DT = {5.0e-13, 5.0e-12}, ZSTOP={0.2, 15.0};
# RUN, METHOD = "PARALLEL-T", BEAM = BEAM1, FIELDSOLVER = FS_SC, DISTRIBUTION = Dist;
print('ENDTRACK;')
print('\n')
print('Stop;') 
print('Quit;')






#-------------------------------------------------------------------------------------------------------------

# This is the beginning of breaking down the sample .in file into data values. Ideally this will 
# evolve to take generic input values and add them to a dictionary
"""
count = 0
# if(debug == 1): print()
with open (dirname + '/xta.in') as f:
    fLines = f.readlines()
    for line in fLines:
        count += 1
        if( line[0] == '/' or line[0] == '&'):
            if(debug == 1): print(line)
            continue
        elif(line[0]+line[1]+line[2]+line[3] == 'head'):
            x = re.findall(r"'(.*?)'", line)
            headName = x[0]
            if(debug == 1): print('var: ' + headName + '. File type: ' + str(type(headName)))
        elif(line[0]+line[1]+line[2] == 'run'):
            x = line.split('= ')[1]
            runCount = int(x)
            d = type(runCount) is int
            if(debug == 1): print('var: ' + str(runCount) + '. File type: ' + str(d))
        elif(line[0]+line[1]+line[2]+line[3] == 'loop')
# Then we need to decide how we will read the ASTRA .in file, and implement it.
# TESTING GROUNDS
# -------------------------------------------------------------------------------------------------------------
# &newrun
headName = 'X-Band injector 5.59 cell'
# head = 'X-Band injector 5.59 cell'
runCount = 1
# run = 1 
bLoop = False
# loop = False
nLoop = 0
# nloop = 0
currentDistribution = 'astra.particles'
# distribution = 'astra.particles'
xOff = 0
# xoff = 0
yOff = 0
# yoff = 0
lMagnetized = False
# lmagnetized = False
bEmits = True
# emits = True
cEmits = True
# c_emits = True
localEmit = True
# local_emit = True
bPhases = True
# phases = True
bTracks = False
# tracks = False
bRefs = True
# refs = True
tChecks = True
# tchecks = True
bCathodes = False
# cathodes = False
bBinary = False
# binary = False
bHighRes = False
# high_res = False
lMonitor = True
# lmonitor = True
bTrackAll = True
# track_all = True
bPhaseScan = False
# phase_scan = False
bLRMBack = True
# l_rm_back = True
bAutoPhase = True
# auto_phase = True
bCheckRefPart = False
# check_ref_part = False
zStart = 0.0
# zstart = 0.0
zStop = 5.5
# zstop = 5.5
zEmit = 200
# zemit = 200
zPhase = 2
# zphase = 2
trEmits = False
# tr_emits = False
screen1 = 0.0001
# screen(1) = 0.0001
screen2 = 0.65
# screen(2) = 0.65
screen3 = 1.7
# screen(3) = 1.7
screen4 = 1.9
# screen(4) = 1.9
screen5 = 5.449
# screen(5) = 5.449
hMin = 1e-05
# h_min = 1e-05
hMax = 0.001
# h_max = 0.001

# /

# &scan
lScan = False
# lscan = False
bScanPara = 'maxB(1)'
# scan_para = 'maxB(1)'
sMin = 0.54
# s_min = 0.54
sMax = 0.555
# s_max = 0.555
sNumb = 7
# s_numb = 7
fom1 = 'bunch charge'
# fom(1) = 'bunch charge'
fom2 = 'hor. Emittance'
# fom(2) = 'hor. Emittance'
fom3 = 'hor. spot'
# fom(3) = 'hor. spot'
fom4 = 'mean energy'
# fom(4) = 'mean energy'
fom5 = 'rms energy'
# fom(5) = 'rms energy'
fom6 = 'length'
# fom(6) = 'length'

# /

# &charge
bLoop = False
# loop = False
bLspch = False
# lspch = False
bLspch3D = False
# lspch3d = False
nXF = 16
# nxf = 16
nYF = 16
# nyf = 16
nZF = 16
# nzf = 16
cellVar = 2
# cell_var = 2
minGrid = 4e-07
# min_grid = 4e-07
maxScale = 0.05
# max_scale = 0.05

# /

# &aperture

# /

# &fem

# /

# &cavity
bLoop = False
# loop = False
bLEField = True
# lefield = True
fileEField1 = 'fieldmaps/map559.dat'
# file_efield(1) = 'fieldmaps/map559.dat'
nue1 = 11.424
# nue(1) = 11.424
maxe1 = 200.01
# maxe(1) = 200.01
phi1 = -10
# phi(1) = -10
cPos1 = 0.0
# c_pos(1) = 0.0
cSmooth1 = 50
# c_smooth(1) = 50
fileEField2 = 'fieldmaps/TWS_xband_linac.dat'
# file_efield(2) = 'fieldmaps/TWS_xband_linac.dat'
nue2 = 11.424
# nue(2) = 11.424
maxE2 = 130.001
# maxe(2) = 130.001
phi2 = 0
# phi(2) = 0
cPos2 =1.0
# c_pos(2) = 1.0
cNumb2 = 105
# c_numb(2) = 105

# /

# &solenoid
bLoop = False
# loop = False
bLBField = True
# lbfield = True
fileBField1 = 'fieldmaps/xband_solenoid.dat'
# file_bfield(1) = 'fieldmaps/xband_solenoid.dat'
maxB1 = 0.57
# maxb(1) = 0.57
sPos1 = 0
# s_pos(1) = 0
sXOff1 = 0
# s_xoff(1) = 0
sYOff1 = 0
# s_yoff(1) = 0
sSmooth1 = 10
# s_smooth(1) = 10

# /

# &quadrupole
bLoop = False
# loop = False
bLQuad = True
# lquad = True
qLength1 = 0.2062
# q_length(1) = 0.2062
qK1 = 4.0
# q_k(1) = 4.0
qPos1 = 2.41
# q_pos(1) = 2.41
qBore1 = 0.0327
# q_bore(1) = 0.0327
qLength2 = 0.2062
# q_length(2) = 0.2062
qK2 = -2.3
# q_k(2) = -2.3
qPos2 = 2.84
# q_pos(2) = 2.84
qBore2 = 0.0327
# q_bore(2) = 0.0327
qLength3 = 0.2062
# q_length(3) = 0.2062
qK3 = 4.0
# q_k(3) = 4.0
qPos3 = 3.68
# q_pos(3) = 3.68
qBore3 = 0.0327
# q_bore(3) = 0.0327
qLength4 = 0.2062
# q_length(4) = 0.2062
qK4 = 0.0
# q_k(4) = 0.0
qPos4 = 3.6122
# q_pos(4) = 3.6122
qBore4 = 0.0327
# q_bore(4) = 0.0327

# /
"""
