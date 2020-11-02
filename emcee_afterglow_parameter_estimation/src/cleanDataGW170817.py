"""
Take an observation datafile, clean it, and 
organize data for use in afterglow code.

Observation data used from Mooley (et al? year?):
    col 1: Observation time [s]
    col 2: Frequency label (radio, optical, xray)
    col 3: Observed flux [mJy]
    col 4: Flux uncertanty [mJy]
    col 5: Observed frequency [GHz, ?, ?]

Parameters
----------
datafile : external file, str
    e.g.: "observations_Mooley.dat"  

Returns
-------
time_obs : list, int
    Observation time [s]
freq_labels : list, str
    Frequency label
flux_obs : list, float
    Observed flux [mJy]
flux_uncert : list, float
    Flux uncertainty [mJy]
freq_obs : list, float
    Observed frequency, converted to Hz
"""
import numpy as np

def cleanDataGW170817(datafile):
    '''Clean and organize data.'''

    #  CONSTANTS 

    #  Speed of light [m/s]
    c = 2.99792458 * 10**8
    #  Planck's constant [eV * s]  
    h = 4.135667696 * 10**-15  
    
    compiled_list = []
    open_data = open(datafile)
    for line in open_data:
        compiled_list.append(
            [elt.strip() for elt in line.split('\t')]
            )
    compiled_list = list(compiled_list)

    time_obs = []
    freq_labels = []
    flux_obs = []
    flux_uncert = []
    freq_obs = []
    
    #  Organizing data, changing data type
    for i in range(len(compiled_list) - 2):
        time_obs.append(int(compiled_list[i][0]))
        freq_labels.append(compiled_list[i][1])
        flux_obs.append(float(compiled_list[i][2])) 
        flux_uncert.append(float(compiled_list[i][3])) 
        freq_obs.append(float(compiled_list[i][4]))
    
    #  Converting frequencies
    for i, nu in enumerate(freq_labels):
        #  Given in GHz, convert to Hz
        if nu == "Radio":  
            freq_obs[i] = freq_obs[i] * (10**9)
        #  Optical: replace data with 6000 angstroms, convert to Hz
        if nu == "Opt":  
            freq_obs[i] = c / (6000 * 10**(-10))
        # Replace with 1 keV (1000 eV), convert to Hz
        if nu == "Xray":  
            freq_obs[i] = 1000 / h
    print("Data cleaned.")
    return time_obs, freq_labels, flux_obs, flux_uncert, freq_obs

time_obs, freq_labels, flux_obs, flux_uncert, freq_obs = cleanDataGW170817("observations_Mooley.dat")