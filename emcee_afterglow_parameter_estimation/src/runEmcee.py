#!/usr/bin/python3

""" 
Use emcee module to generate parameter fits based on DL afterglow code. 

Imported files
--------------
init_params.py
plots.py
dataGW170817.py
runtimeSMS.py (optional)
exceptionHandler.py

Functions 
--------------

cleanTempFolder(None)
    Remove files from /temp folder.
    Used by: main()

createParamFiles(*args)
    Store emcee parameter values in .dat file. 
    Used by: main()

runAfterglow(*args)
    Call afterglow script runAfterglowDL.py to calculate lightcurves.
    Used by: logLikelihood()

logPrior(*agrs)
    Create parameter lables using math text.
    Used by: logProbability()

logLikelihood(*args)
    Used by: logProbability()

logProbability(*args)
    Used by: main()

main(None)
    Run emcee package, save and plot results. 
"""

#  Standard Python library imports 
import numpy as np
from math import log10
import time #  for calculating runtime 
import shutil #  for cleaning /temp folder
import os 
os.environ["OMP_NUM_THREADS"] = "1"
print(os.getcwd())
import sys
print("Python version {}".format(sys.version))
import multiprocessing
from multiprocessing import Pool

#  Emcee imports 
import emcee
print("emcee version", emcee.__version__)
import tqdm #  for progress bar 

#  Importing from companion scripts 
from cleanDataGW170817 import time_obs, flux_obs, flux_uncert
from init_params import params_list
import runAfterglow as run_ag
import plots as corner_plot
##from runtimeSMS import calcRuntime
from exceptionHandler import exception_handler

def cleanTempFolder():
    """Remove files from /temp folder."""

    folder = os.path.join(os.getcwd(), "temp")
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def createParamFiles(params_list):
    """
    Determine whether a duplicate file exists 
    using pid and timestamp as identifiers.
    If file exists, create a new one with a different timestamp.
    If not, create a temp file containing emcee parameter samples.

    Parameters
    ----------
    params_list: list
        List of emcee parameter values. 

    Returns
    ----------
    params_datafile: .dat file 
        Contains emcee parameter values for use by runAfterglow.
    """
    folder = os.path.join(os.getcwd(), "temp")
    filename = "params-pid-{}-time-{}.dat".format(
            str(os.getpid()), str(time.time()))
    if os.path.isfile(os.path.join(folder, filename)):
        new_filename = 'params-pid-{}-time-{}.dat'.format(
            str(os.getpid()), str(time.time()))
        params_datafile = os.path.join(folder, new_filename) 
    else: 
        params_datafile = os.path.join(folder, filename)
         
    dataout = []
    for i, item in enumerate(params_list):
        dataout.append(item[0])
    np.savetxt(params_datafile, dataout, fmt='%s')
    return params_datafile

def runAfterglow():
        pass 

def logPrior(theta):
    """
    Define flat ("uninformative") priors for a set of parameters, theta.
    
    Parameters
    ----------
    theta: set of parameters 

    Returns
    ----------
    0.0 if sample drawn within the bounds, -infinity otherwise. 
    """ 
    pass

def logLikelihood(theta, x, y, yerr):
    """
    Define log-likelihood function assuming 
    a Gaussian distribution.
    
    Parameters
    ----------
    theta: set of parameters
    y: array, float 
        Observed flux 
    yerr: array, float 
        Observed flux uncertainty 

    Returns
    ----------
    -0.5 * np.sum(((y-model)/yerr)**2): float
        Likelihood function 
    """ 
    pass  

def logProbability(theta, x, y, yerr):
    """Define full log-probabilty function to be sampled."""
    if not np.isfinite(logPrior(theta)):
        return -np.inf
    return logPrior(theta) + logLikelihood(theta, x, y, yerr)

@exception_handler
def main():
    """        
    Clean temp folder and run emcee sampler. 
    When complete:
        - Save results in a .csv file
        - Generate a corner plot
        - Send SMS alert (optional)  
    """
    start = time.time()
    cleanTempFolder()

    def emceeSampler(params_list):
        """" 
        Run emcee sampler and check for convergence every n steps.  

        Parameters
        ----------
        params_list: list, float
            NOTE: This is a global variable, 
            imported from init_params.py (see imports list, line 63). 

        Returns
        ----------
        None  
        """
        def _prepEmcee(params_list):
            """Iniitalize walkers in a Gaussian ball around initial guess."""
            num_params = len(params_list)
            print("# of parameters emcee is fitting: {}".format(num_params))
            print("Initial parameter guesses:{}".format(params_list))
            params_list = np.reshape(params_list, (1, num_params))
            pos = params_list + 1e-4 * np.random.randn(n_walkers, num_params)
            nwalkers, ndim = pos.shape 
            return nwalkers, ndim, pos

        def _createBackendFile():
            """Generate a .h5 backend file to save and monitor progress.""" 
            print(os.getcwd())
            backend_folder = os.path.join(os.getcwd(), "backend")
            datestamp = time.strftime("%Y%m%d-%H%M")
            filename = "backend-file-{}.h5".format(datestamp)
            backend = emcee.backends.HDFBackend(
                os.path.join(backend_folder, filename)
                )
            return backend

        def _saveResults(backend, samples):
            datestamp = time.strftime("%Y%m%d-%H%M")
            #  Save samples in .csv file stamped with 
            #  date and time the run was completed 
            results_folder = os.path.join(os.getcwd(), "results")
            samples_filename = 'samples-{}.csv'.format(datestamp)
            np.savetxt(
                os.path.join(results_folder, samples_filename), 
                samples, 
                delimiter=',', 
                fmt='%e'
                )
            #  Update backend file name to match 
            #  the date and time of above .csv file
            backend_folder = os.path.join(os.getcwd(), "backend")
            filename = "backend-file-{}.h5".format(datestamp)
            os.rename(
                backend.filename,
                os.path.join(backend_folder, filename)
                ) 

        def _runEmcee(backend, nwalkers, ndim, pos):
            """            
            Set up a pool process to run emcee in parallel. 
            Run emcee sampler and check for convergence very n steps,
            where n is user-defined. 
            """
            backend.reset(nwalkers, ndim)
            index = 0
            autocorr = np.empty(max_iter)
            old_tau = np.inf
            
            #  Set up parallel processing 
            with Pool(processes = n_processes) as pool:
                sampler = emcee.EnsembleSampler(
                    nwalkers, 
                    ndim, 
                    logProbability,
                    args = (x,y,yerr), 
                    backend=backend, 
                    moves=[
                        (emcee.moves.DEMove()), 
                        (emcee.moves.DESnookerMove()),
                    ],
                    pool=pool
                    )
                #  Run emcee 
                for sample in sampler.sample(
                    pos, iterations=max_iter, progress=True):

                    #print("log_prob = {} ".format(sampler.get_log_prob()))
                    #print("tau = {}".format(sampler.get_autocorr_time()))
                    #print("acceptance fraction = {} ".format(sampler.acceptance_fraction))  

                    #  Check for convergence very "check_iter" steps
                    if sampler.iteration % check_iter:
                        continue
                    tau = sampler.get_autocorr_time(tol=0)
                    autocorr[index] = np.mean(tau)
                    index += 1
                    converged = np.all(tau * 100 < sampler.iteration)
                    converged &= np.all(np.abs(old_tau - tau) / tau < 0.01)
                    if converged:
                        break
                    old_tau = tau

                    #  Get samples 
                    samples = sampler.chain[:, :, :].reshape((-1,ndim))
                    print(samples.shape, samples)
            return samples

        backend = _createBackendFile()
        nwalkers, ndim, pos = _prepEmcee(params_list)
        samples = _runEmcee(backend, nwalkers, ndim, pos)
        _saveResults(backend, samples)
        ##return samples

    #  Run emcee sampler code 
    emceeSampler(params_list)

    # Plot samples, save in /results/plots folder
    corner_plot.main()

    #  Calculate runtime, send SMS alert (optional)  
    end = time.time()
    ##calcRuntime(start,end)

# Global variables from imports  
x = time_obs
y = flux_obs
yerr = flux_uncert 
num_params = len(params_list)
params = np.reshape(params_list, (1, num_params))

# User-defined global variables 
n_walkers = 20  
n_processes = 4
max_iter = 1
#  Check for convergence every n iterations
check_iter = 1 #  Note: max_iter must be divisible by n

#  Run script 
if __name__ == "__main__":
    main() 