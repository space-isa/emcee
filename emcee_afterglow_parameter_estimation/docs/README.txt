-------------------------------------------------------------------------------
Author: Isabel J. Rodriguez, Oregon State University 
email: rodrjack at oregonstate dot edu 
-------------------------------------------------------------------------------

Install dependencies in requirements.txt: 
    - Open terminal 
    - $ run pip3 install -r requirements.txt
    - $ pip freeze > requirements.txt 

Before you run this code: 

1) Put in your afterglow code: 
    - Open runAfterglow.py
       - Inputs will be emcee's estimates for your parameters of interest. 
       - Outputs will be lightcurves that will be used as part of emcee's likelihood function.
       - If your code is disrtibuted over a number of scripts:
           - Keep all scripts in src folder 
           - Ensure the code that runs the code is named runAfterglow.py, as 
              this script will be imported by runEmcee.py. 

2) Locate and update parameters and prior values:
    - init_params.py 
    - runEmcee.py
       - logPrior()
       - logLiklihood() 
    - plot_samples.py
       - pullSamples()
       - createLabels()
    - /backend/plotBackend.py
       - createLabels() 

To run emcee code: 
    - Open runEmcee.py
    - In lines 340-344, set preferred MCMC parameters: 
        - n_walkers = ___ (number of walkers)
        - n_processes = __ (number of pool processes)
        - max_iter = ____ (numpber of iterations/steps)
        - check_iter = ___ (number of steps after which code checks for convergence e.g., 
          every 100 steps. max_iter must be divisible by this number)
    - In terminal, run:
        - $ python3 runEmcee.py
    - When code is complete, terminal will read: 
      "Corner plot generated. Check .../results/plots folder to view results." 

Notes:    
    - Backend .h5 files can be found in backend folder (/backend)
    - Samples are saved as .csv files in results folder as backup. 
    - Preliminary plots are saved as .png files in results/plots folder
        - Go back to the backend file that was generated at the start of the run.
        - Plot final results using plotBackend.py
            - Adjust plotting parameters to your preferences (color, etc.)
            - Plots will live in /src/backend/plots
    - Most functions contain doc strings w/ information (documentation ongoing)
    - Temp folder is cleared at the beginning of each run  

References: 
    - Emcee documentaton: https://emcee.readthedocs.io/en/stable/ 