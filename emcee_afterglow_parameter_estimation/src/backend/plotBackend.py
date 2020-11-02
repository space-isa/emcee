import emcee
from matplotlib import pyplot as plt
import os
import glob
import corner
import time 

def retriveRecentFile():
    '''Returns the most recent samples output file to plot.'''
    try:
        backend_folder = os.getcwd()
        files = glob.glob(backend_folder + '/*.h5')
        print(max(files))
        return max(files)
    except:
        print("There are no files in this folder")

def createLabels():
    '''Creates lables for parameters using math text.
    
    Parameters
    ----------
    None 

    Returns
    ----------
    labels: list, str 
    '''
    # r"$parameter$" will use math text
    # \mathrm{} will remove math text 
    # e.g., r"$θ_{\mathrm{observed}}$" 
    params  = []
    labels = params[:]
    return labels

def checkEmceeBackend():
    reader = emcee.backends.HDFBackend(retriveRecentFile())
    thin = 15
    # tau = reader.get_autocorr_time()
    #burn_in = int(2*np.max(tau))
    #thin = int(0.5 * np.min(tau))
    samples = reader.get_chain(discard=burn_in, thin=thin, flat=True)
    return samples 

def plotChains(samples, labels):
    fig, axes = plt.subplots(samples.shape[1], figsize=(10, 7), sharex=True)
    for i in range(samples.shape[1]):
        ax = axes[i]
        ax.plot(samples[:, i], "k", alpha=0.7)
        ax.set_xlim(0, len(samples))
        ax.set_ylabel(labels[i])
        axes[-1].set_xlabel("step number")
    fig.savefig("chain-burnin-{}-steps.png".format(burn_in))
    plt.show()

def main():
    '''Generates corner plot'''
    
    samples = checkEmceeBackend()
    labels = createLabels()
    plotChains(samples, labels)

    #samples = pullSamples(retriveRecentFile())
    xkcd_color = 'xkcd:' + 'dark teal'
    corner_plot = corner.corner(samples,
                                labels=labels,
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
    plots_folder = os.path.join(os.getcwd(), "plots")
    filename = "corner-plot-burnin-{}-steps-{}.png".format(burn_in, 
        time.strftime("%Y%m%d-%H%M")
        )
    corner_plot.savefig(
        os.path.join(plots_folder, filename)
        )
    print("Corner plot generated. " \
        "Check .../results/plots folder to view results.")

burn_in = 1000

if __name__ == "__main__":
    main()

