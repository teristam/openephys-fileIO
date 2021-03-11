#%%
# Write data to the new binary format
import sys
sys.path.append("..") # Adds higher directory to python modules path.

import numpy as np 
from pathlib import Path
from openephys_fileIO import fileIO

#%% Convert continuous data to flat binary
outFolder = 'E:\\open-ephys-testdata\\M2_D23-binary'
input_folder = 'E:\\open-ephys-testdata\\M2_D23_2019-04-03_13-34-00'

fileIO.convertContinuous2Binary(input_folder,outFolder)



# %%
