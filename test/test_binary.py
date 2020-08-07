import numpy as np 
from fileIO import *
from Binary import *

dataFolder = 'test/data'

def test_write_binary_data():
    # Test writing of binary data

    # Read the data in original int16 format
    data,headers = load_OpenEphysRecording4BinaryFile(dataFolder,
        num_data_channel=1,num_aux_channel=1, num_adc_channel=1)

    # Write to binary file
    writeBinaryData(dataFolder+'/experiment1/recording1/',data)
    writeStructFile(dataFolder+'/experiment1/recording1/structure.oebin',headers)

    #load the data in float format (take care of the bit per volt)
    data,headers = load_OpenEphysRecording4BinaryFile(dataFolder,
        num_data_channel=1,num_aux_channel=1, num_adc_channel=1,dtype=float)

    # Load binary file using the offical function
    data2, rate2 = Load('test/data')

    np.allclose(data.T,data2['100']['0']['0'])

    
