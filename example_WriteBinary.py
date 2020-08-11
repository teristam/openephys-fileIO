#%%
# Write data to the new binary format
import sys
sys.path.append("..") # Adds higher directory to python modules path.

import numpy as np 
from pathlib import Path
import fileIO
#%% Convert continuous data to flat binary
outFolder = 'E:\\open-ephys-testdata\\M1_D20_2018-10-15_12-51-42-binary'
input_folder = 'E:\\open-ephys-testdata\\M1_D20_2018-10-15_12-51-42'

fileIO.convertContinuous2Binary(input_folder,outFolder)



# %%
