import fileIO
import OpenEphys
import numpy as np
import os

def test_readwriteContinuous():
    file = fileIO.loadContinuousFast('test/data/100_CH1.continuous')
    fileIO.writeContinuousFile('test/data/test.continuous',file['header'],file['timestamps'],file['data'],file['recordingNumber'])
    x = OpenEphys.loadContinuous('test/data/test.continuous')
    np.allclose(file['data'],x['data'])
    np.allclose(file['timestamps'], x['timestamps'])
