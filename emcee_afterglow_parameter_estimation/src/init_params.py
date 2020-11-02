"""
Take list of initial guesses for parameter values  
and save to datafile for use by runEmcee.py.

Place any parameters not being fitted by emcee in unused_params:
e.g. unused_params = {(log10(6.22e+49),),  (log10(7.6e+48),) , (2.067,)} 


Parameters
----------
None 


Returns
-------
params_list : list 
unused_params : dict

"""
import numpy as np
from math import log10

def initParams():
    num_params = int  
    params_list = []
    
    dataout = []
    for i, item in enumerate(params_list):
        dataout.append(item[0])
    print("Initial parameters:{}".format(dataout))
    np.savetxt('params.dat', dataout)
    
    #  Param values to be removed from list for emcee fitting
    unused_params = {}
    #  Final list of parameters for fitting  
    params_list = [param for param in params_list if param not in unused_params] 
    return params_list, unused_params  
params_list, unused_params = initParams()


