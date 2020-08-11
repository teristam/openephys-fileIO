# openephys-fileIO

Allow one to write data into open-ephys continuous and binary format. Useful for offline development and debugging of online algorithms.

### Features
- Fast reading of open-ephys continuous file (9x speed up compared to original Python 3 version)
- Writing of open-ephys flat binary file (including the oebin and timestamp file)
- Writing of open-ephys continuous file in Python
- Basically allow one to convert any neuron data readable in python to open-ephys format



### Usage

Fast load a continuous file:

```
import fileIO
file = fileIO.loadContinuousFast('test/data/100_CH1.continuous')
```

Writing of continuous file

```
file = fileIO.loadContinuousFast('test/data/100_CH1.continuous')
fileIO.writeContinuousFile('test/data/test.continuous',file['header'],file['timestamps'],file['data'],file['recordingNumber'])
   
```

Further example can be seen in the `example_*.py` python scripts.


### TODO
- Event data are not yet supported in writing of binary file
