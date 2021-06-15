import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
matplotlib.rcParams.update({'font.size': 16, 'text.usetex':True, 'font.family':'Times New Roman'})

import nmma.em
from nmma.em.model import SVDLightCurveModel, GRBLightCurveModel, KilonovaGRBLightCurveModel, SupernovaGRBLightCurveModel

# construction the model
sample_times_KN = np.arange(0., 30., 0.1)
sample_times_GRB = np.arange(30., 950., 1.)
sample_times = np.concatenate((sample_times_KN, sample_times_GRB))
kilonova_kwargs = dict(model='Bu2019lm', svd_path='./svdmodels', mag_ncoeff=10, lbol_ncoeff=10, parameter_conversion=None)
model = KilonovaGRBLightCurveModel(sample_times=sample_times, kilonova_kwargs=kilonova_kwargs)

# fetch the best-fit parameters
posterior_samples = pd.read_csv('./outdir/AT2017gfo_Bu2019lm_posterior_samples.dat', header=0, delimiter=' ')
bestfit_idx = np.argmax(posterior_samples.log_likelihood.to_numpy())
params = posterior_samples.to_dict(orient='list')
for key in params.keys():
    params[key] = params[key][bestfit_idx]

KNmodel = model.kilonova_lightcurve_model
# generate the best-fit light curves (KNonly)
_, mag = KNmodel.generate_lightcurve(sample_times - params['KNtimeshift'], params)
for filt in mag.keys():
    mag[filt] += 5. * np.log10(params['luminosity_distance'] * 1e6 / 10.)
sample_times += params['KNtimeshift']
mag['sample_times'] = sample_times
df = pd.DataFrame.from_dict(mag)
df.to_csv('./outdir/bestfit_lightcurve_data_KN_from_KNGRBmodel_1KN_1GRB.dat', sep=' ', index=False)
