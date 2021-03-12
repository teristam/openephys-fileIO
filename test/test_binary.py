import numpy as np 
from openephys_fileIO.fileIO import *
from openephys_fileIO.Binary import *

def test_write_binary_data():
    # Test writing of binary data
    
    dataFolder = 'test/data'

    # Read the data in original int16 format
    data,headers = load_OpenEphysRecording4BinaryFile(dataFolder,
        num_data_channel=1,num_aux_channel=1, num_adc_channel=1)
    print(headers)

    # Write to binary file
    writeBinaryData(dataFolder+'/experiment1/recording1/',data)
    writeStructFile(dataFolder+'/experiment1/recording1/structure.oebin',headers)

    #load the data in float format (take care of the bit per volt)
    data,headers = load_OpenEphysRecording4BinaryFile(dataFolder,
        num_data_channel=1,num_aux_channel=1, num_adc_channel=1,dtype=float)

    # Load binary file using the offical function
    data2, rate2 = Load('test/data')

    np.allclose(data.T,data2['100']['0']['0'])

def test_numpy2binary():
    # test write of numpy data
    Fs = 30000
    x = np.random.randn(3*Fs,4)
    bitVolts = 0.195
    dataFolder = 'test/data2'
    channel_names = [f'CH{i}' for i in range(x.shape[1])]
    writeBinaryData(dataFolder+'/experiment1/recording1/', x, bitVolts)
    writeStructFile(dataFolder+'/experiment1/recording1/structure.oebin',samplerate=30000,
     num_channels= x.shape[1], bit_volts=bitVolts,channel_names=channel_names)

    # load the binary file
    data, rate = Load(dataFolder)

    np.allclose(x, data['100']['0']['0'])






    
