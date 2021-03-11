#%%
from openephys_fileIO import fileIO
import numpy as np
import os
import shutil

#%% Shorten continuous data
basePath = 'E:\\open-ephys-testdata\\M1_D20_2018-10-15_12-51-42'
newPath = basePath+'_short'
shortenLength = 30000*60*10

try:
    os.mkdir(newPath)
except  FileExistsError:
    print("Folder already exist")

for f in os.scandir(basePath):
    if f.name.endswith('.continuous'):
        print(f'{f.name} truncated')
        file = fileIO.loadContinuousFast(f.path)
        fileIO.writeContinuousFile(newPath+'/'+f.name, file['header'],
            file['timestamps'], file['data'][:shortenLength], file['recordingNumber'])
    else:
        if f.is_dir():
            shutil.copytree(f.path, newPath+'/'+f.name)
        else:
            shutil.copyfile(f.path, newPath+'/'+f.name)

        print(f'{f.name} copied')

