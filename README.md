# openephys-fileIO

![build](https://github.com/teristam/openephys-fileIO/workflows/build/badge.svg?branch=master)

Allow one to write data into open-ephys continuous and binary format. Useful for offline development and debugging of online algorithms.

### Features
- Fast reading of open-ephys continuous file (9x speed up compared to original Python 3 version)
- Writing of open-ephys flat binary file (including the oebin and timestamp file)
- Writing of open-ephys continuous file in Python
- Writing any numpy array into openephys binary format
- Basically allow one to convert any neuron data readable in python to open-ephys format


### Installation

- clone the repository `git clone https://github.com/teristam/openephys-fileIO.git`
- go to the `openephys-fileIO` folder, then `pip install .`

### Usage

Fast load a continuous file:

```
from openephys_fileIO import fileIO
file = fileIO.loadContinuousFast('test/data/100_CH1.continuous')
```

Writing of continuous file

```
file = fileIO.loadContinuousFast('test/data/100_CH1.continuous')
fileIO.writeContinuousFile('test/data/test.continuous',file['header'],file['timestamps'],file['data'],file['recordingNumber'])
   
```

Convert a continuous file into flat binary format

```
dataFolder = 'test/data'

data,headers = load_OpenEphysRecording4BinaryFile(dataFolder,
    num_data_channel=1,num_aux_channel=1, num_adc_channel=1)

writeBinaryData(dataFolder+'/experiment1/recording1/',data)
writeStructFile(dataFolder+'/experiment1/recording1/structure.oebin',headers)
```

Convert a numpy array into openEphys binary data (useful for generating simulated recording)

```
Fs = 30000
x = np.random.randn(3*Fs,4)
bitVolts = 0.195
dataFolder = 'test/data2'
channel_names = [f'CH{i}' for i in range(x.shape[1])]
writeBinaryData(dataFolder+'/experiment1/recording1/', x, bitVolts)
writeStructFile(dataFolder+'/experiment1/recording1/structure.oebin',samplerate=30000,
    num_channels= x.shape[1], bit_volts=bitVolts,channel_names=channel_names)
```


Further example can be seen in the `example_*.py` python scripts.


For ease of use, this repo contains some Python module from the original [analysis-tool](https://github.com/open-ephys/analysis-tools) repo 

### TODO
- Event data are not yet supported in writing of binary file
