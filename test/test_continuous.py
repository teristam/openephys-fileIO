import fileIO
import OpenEphys
import numpy as np
import time

def test_readwriteContinuous():
    file = fileIO.loadContinuousFast('test/data/100_CH1.continuous')
    fileIO.writeContinuousFile('test/data/test.continuous',file['header'],file['timestamps'],file['data'],file['recordingNumber'])
    x = OpenEphys.loadContinuous('test/data/test.continuous')
    np.allclose(file['data'],x['data'])
    np.allclose(file['timestamps'], x['timestamps'])

def test_benchmark_originload(benchmark):

    @benchmark
    def dummy():
        OpenEphys.loadContinuous('test/data/test.continuous')


def test_benchmark_fastload(benchmark):

    benchmark(fileIO.loadContinuousFast,'test/data/test.continuous')
