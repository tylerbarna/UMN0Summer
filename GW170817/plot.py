import numpy as np
import pandas as pd

import nmma.em
from nmma.em.model import SVDLightCurveModel, GRBLightCurveModel, KilonovaGRBLightCurveModel, SupernovaGRBLightCurveModel

import matplotlib
import matplotlib.pyplot as plt

import seaborn as sns

fig_width_pt = 750.0  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = 0.9*fig_width*golden_mean      # height in inches
fig_size =  [fig_height,fig_width]  # rotate by 90 degree
params = {'backend': 'pdf',
           'axes.labelsize': 14, 
           'legend.fontsize': 14, 
           'xtick.labelsize': 14, 
           'ytick.labelsize': 14, 
           'text.usetex': True,
           'font.family':'Times New Roman',
           'figure.figsize': fig_size}
matplotlib.rcParams.update(params)

# construction the model
trigger_time = 57982.5285236896

# load the best-git light curves
magKN_KNGRB = pd.read_csv('./outdir/bestfit_lightcurve_data_KN_from_KNGRBmodel_1KN_1GRB.dat', header=0, delimiter=' ')

# load the observed data
data = nmma.em.utils.loadEvent('AT2017gfo_KNdominate.dat')

filts = ['g', 'r']
colors = sns.color_palette('rainbow', len(filts))

plt.figure(1)
cnt = 0
for filt, color in zip(filts, colors):
    cnt = cnt + 1
    vals = "%d%d%d"%(len(filts),1,cnt)
    if cnt == 1:
        ax1 = plt.subplot(eval(vals))
        ax = ax1
        ax.set_ylim([36, 16])
        ax.set_xlim([1., 950.])
        ax.set_xscale('log')
    else:
        ax2 = plt.subplot(eval(vals),sharex=ax1, sharey=ax1)
        ax = ax2

    ax.set_ylabel('{0}'.format(filt))

    samples = data[filt]
    t, y, sigma_y = samples[:,0], samples[:,1], samples[:,2]
    t -= trigger_time
    idx = np.where(~np.isnan(y))[0]

    idx = np.where(np.isfinite(sigma_y))[0]
    ax.errorbar(t[idx],y[idx],yerr=sigma_y[idx],marker='o',color='k', fmt='o')

    idx = np.where(~np.isfinite(sigma_y))[0]
    if len(idx) == 1:
        ax.scatter(t[idx][0],y[idx][0],marker='v',color='k')
    else:
        ax.scatter(t[idx],y[idx],marker='v',color='k')

    magKN_KNGRB_plot = nmma.em.utils.getFilteredMag(magKN_KNGRB, filt)

    ax.plot(magKN_KNGRB.sample_times, magKN_KNGRB_plot, color='C2', linestyle='--', label='KN from KN-GRB')
    ax.fill_between(magKN_KNGRB.sample_times, magKN_KNGRB_plot + 1, magKN_KNGRB_plot - 1, color='C2', alpha=0.2)
    if cnt == 1:
        plt.setp(ax.get_xticklabels(), visible=False)
        plt.legend(loc='upper right')
    elif not cnt == len(filts):
        plt.setp(ax.get_xticklabels(), visible=False)

#ax1.set_zorder(1)
ax.set_xlabel('Time [days]')
plt.savefig('best_lightcurves_plot.pdf', bbox_inches='tight')
