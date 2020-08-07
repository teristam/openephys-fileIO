#%%
import OpenEphys
import fileIO
import numpy as np
import os
import shutil
#%% Example: Verify that the data is written correctly
file = fileIO.loadContinuousFast('E:/open-ephys-testdata/M1_D31_2018-11-01_12-28-25/100_CH1.continuous')
fileIO.writeContinuousFile('test.continuous',file['header'],file['timestamps'],file['data'],file['recordingNumber'])
x = OpenEphys.loadContinuous('test.continuous')
np.allclose(file['data'],x['data'])

#%% Example: create short files of an entire recording for debugging purpose
basePath = 'E:/open-ephys-testdata/M1_D31_2018-11-01_12-28-25/'
newPath = basePath+'_short'
shortenLength = 30000*60*3 #length of the shorten data

try:
    os.mkdir(newPath,)
except  FileExistsError:
    print("Folder already exist")

for f in os.scandir(basePath):
    if f.name.endswith('.continuous'):
        # Truncate the continous files
        print(f'{0} truncated'.format(f.name))
        file = fileIO.loadContinuousFast(f.path)
        fileIO.writeContinuousFile(newPath+'/'+f.name, file['header'],
            file['timestamps'], file['data'][:shortenLength], file['recordingNumber'])
    else:
        # Copy all other files
        if f.is_dir():
            shutil.copytree(f.path, newPath+'/'+f.name)
        else:
            shutil.copyfile(f.path, newPath+'/'+f.name)

        print(f'{0} copied'.format(f.name))



# %%
