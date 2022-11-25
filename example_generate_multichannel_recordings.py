#%%
from openephys_fileIO import fileIO
import numpy as np
import os
import shutil
from tqdm import tqdm

#%% Shorten continuous data
basePath = 'E:\\open-ephys-testdata\\M2_D23_2019-04-03_13-34-00'
newPath = basePath+'_short'
shortenLength = 30000*60*3

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

#%% Load the data
input_folder = 'E:\\open-ephys-testdata\\M2_D23_2019-04-03_13-34-00_short'
data,headers = fileIO.load_OpenEphysRecording4BinaryFile(input_folder,
    num_data_channel=16,num_aux_channel=3, num_adc_channel=8)

data_neuro = data[:16,:]
data_aux = data[16:,:]

#%% cut the data in time, and then stack them into new channels
repeat = 1
data2 = data_neuro.reshape(data_neuro.shape[0]*repeat, -1)
data2 = np.vstack([data2,data_aux[:,:data2.shape[1]]])
print(data2.shape)

#%%  Modify the channel header

# duplicate the original header
ch_header = headers[0]
for i in range(16*repeat-16):
    headers.insert(0, ch_header.copy())

# reformat the channel number
idx = 1
for h in headers:
    if 'CH' in h['channel']:
        h['channel'] = f"'CH{idx}'"
        idx += 1
    print(h['channel'])

#%%
for h in headers:
    if 'CH' in h['channel']:
        print(h['channel'])

#%% write binary file
outFolder = f'E:\\open-ephys-testdata\\M2_D23_short_ch{16*repeat}'

fileIO.writeBinaryData(outFolder+'/experiment1/recording1/',data2)
fileIO.writeStructFile(outFolder+'/experiment1/recording1/structure.oebin',headers)


# %%
