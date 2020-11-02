""" 
Generates corner plot assuming a 10-parameter fit. All parameters
must have a range (i.e., not static values) in order to be plotted.

Functions 
---------

retriveRecentFile()
    Return the most recent samples output file to plot.
    Used by: pullSamples()

pullSamples()
    Retrieve data to be plotted, change from str to float.
    Used by: main()

createLabels()
    Create parameter lables using math text.
    Used by: main()

main() 
    Call above functions, generate a labeled corner plot. 
    Plot attributes are defined here (e.g., color, font size).
"""

#  Python standard library imports 
import os
import numpy as np
import time
import csv
import glob

#  Plotting imports 
from matplotlib import pyplot as plt
import corner

def retriveRecentFile():
    '''Returns the most recent samples output file to plot.'''
    try:
        results_folder = os.path.join(os.getcwd(), "results")
        files = glob.glob(results_folder + '/*.csv')
        return max(files)
    except:
        print("There are no files in this folder")

def pullSamples(filename):
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

def main():
    '''Generates corner plot'''

    samples = pullSamples(retriveRecentFile())
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