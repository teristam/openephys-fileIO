#%%
# Write data to the new binary format
import sys
sys.path.append("..") # Adds higher directory to python modules path.

import OpenEphys
import numpy as np 
import json
import os
from pathlib import Path
import OpenEphys
import fileIO
#%%
outFolder = 'testData'
debug_folder = '/media/data2/pipeline_testing_data/M1_D31_2018-11-01_12-28-25'

fileIO.convertContinuous2Binary(debug_folder,outFolder)

# %% Make some test data
Fs = 30000
nChan = 16
signals = np.random.randint(0,1000,(Fs*60*3,nChan),dtype='<i2')
datapath ='testData/continuous/open-ephys'
try:
    os.makedirs(datapath)
except FileExistsError:
    print('Folder exists. Skipping')

with open(datapath+'/continuous.dat','wb') as f:
    f.write(signals.tobytes())

np.save(datapath+'/timestamps.npy',np.arange(signals.shape[0],dtype='i8'))

#%% Reading flat binary data
x = np.fromfile('testData/continuous/open-ephys/continuous.dat',dtype=np.int16)
x = x.reshape(-1,27)

#%% plot
bit_per_volt = 0.000152588
Fs = 30000
plt.plot(x[:Fs*30,17]*bit_per_volt) #ADC channel

# %%
