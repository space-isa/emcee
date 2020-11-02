"""NOTE: To replace plots.py"""

#  Python standard library imports 
import os
import numpy as np
import time
import csv
import glob
import emcee 

#  Plotting imports 
from matplotlib import pyplot as plt
import corner

def retriveRecentFile_csv():
    '''Returns the most recent samples output file to plot.'''
    try:
        results_folder = os.path.join(os.getcwd(), "results")
        files = glob.glob(results_folder + '/*.csv')
        return max(files)
    except:
        print("There are no files in this folder")

def retriveRecentFile_backend():
    '''Returns the most recent samples output file to plot.'''
    try:
        results_folder = os.path.join(os.getcwd(), "backend")
        files = glob.glob(results_folder + '/*.h5')
        return max(files)
    except:
        print("There are no files in this folder")

def pullSamples_csv(filename):
    '''Retrieve data to be plotted, change from str to float.
    
    Parameters
    ----------
    filename: external .csv file, str

    Returns
    ----------
    samples: list, float

    '''
    with open(filename) as data:
        eps_E = []
        eps_B = []
        p_e = []
        n_ISM = []
        E_j = []
        E_c = []
        theta_c = []
        theta_j = []
        theta_obs = []
        Gamma_0 = []
        reader = csv.reader(data, delimiter=',')
        for row in reader:
            eps_E.append(np.float(row[0]))
            eps_B.append(np.float(row[1]))
            p_e.append(np.float(row[2]))
            n_ISM.append(np.float(row[3]))
            E_j.append(np.float(row[4]))
            E_c.append(np.float(row[5]))
            theta_j.append(np.float(row[6]))
            theta_c.append(np.float(row[7]))
            theta_obs.append(np.float(row[8]))
            Gamma_0.append(np.float(row[9]))
    samples = list(
        zip(
            eps_E, eps_B, p_e, 
            n_ISM, E_j, E_c, theta_j,
            theta_c, theta_obs, Gamma_0
           )
        )
    return samples

def pullSamples_Backend(filename):
    reader = emcee.backends.HDFBackend(filename)
    tau = reader.get_autocorr_time()
    burnin = int(2 * np.max(tau))
    thin = int(0.5 * np.min(tau))
    samples = reader.get_chain(discard=burnin, flat=True, thin=thin)
    return samples 

def createLabels(num_params):
    '''Creates lables for parameters using math text.
    
    Parameters
    ----------
    num_params: int 
        Number of parameters to be plotted. 

    Returns
    ----------
    labels: list, str 
    '''
    params  = [
               r"$ɛ_{\mathrm{e}}$",
               r"$ɛ_{\mathrm{b}}$",
               r"$p_{\mathrm{index}}$",
               r"$n_{\mathrm{ISM}}$",
               r"$E_{\mathrm{j}}$",
               r"$E_{\mathrm{c}}$",
               r"$θ_{\mathrm{j}}$",
               r"$θ_{\mathrm{c}}$",
               r"$θ_{\mathrm{obs}}$",
               r"$Gamma_{\mathrm{0}}$"
               ]
    labels = params[:num_params]
    #print(labels)
    return labels


def main(backend=True):
    '''Generates corner plot'''
    if backend==True: 
        samples = pullSamples_Backend(retriveRecentFile_backend())
    else: 
        samples = pullSamples_csv(retriveRecentFile_csv())
    xkcd_color = 'xkcd:' + 'dark teal'
    corner_plot = corner.corner(samples,
                                labels=createLabels(len(samples[0])),
                                quantiles=[0.16, 0.5, 0.84],
                                color=xkcd_color,
                                histtype='bar',
                                show_titles=True,
                                title_kwargs={"fontsize": 18},
                                title_fmt='.1e',
                                smooth=True,
                                fill_contours=True,
                                plot_density=True,
                                use_math_text=False,
                                hist_kwargs={
                                "color": xkcd_color,
                                "fill": True,
                                "edgecolor": 'k',
                                "linewidth": 1.2
                                },
                                top_ticks=False,
                                figsize=((12, 12)))
    for ax in corner_plot.get_axes():
        ax.tick_params(
            axis='both', 
            labelsize=9, 
            direction='out', 
            pad=8.0
            )
    plots_folder = os.path.join(os.getcwd(), "results", "plots")
    filename = "corner-plot-DL-emcee-{}.png".format(
        time.strftime("%Y%m%d-%H%M")
        )
    corner_plot.savefig(
        os.path.join(plots_folder, filename)
        )
    print("Corner plot generated. " \
        "Check .../results/plots folder to view results.")

if __name__ == "__main__":
    main() 