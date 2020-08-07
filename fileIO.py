
'''
Created on 7 August 2020
@author: Teris Tam

'''


from OpenEphys import *
from pathlib import Path
import json
import OpenEphys

# constants
NUM_HEADER_BYTES = 1024
SAMPLES_PER_RECORD = 1024
BYTES_PER_SAMPLE = 2
RECORD_SIZE = 4 + 8 + SAMPLES_PER_RECORD * BYTES_PER_SAMPLE + 10 # size of each continuous record in bytes
RECORD_MARKER = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 255])

# constants for pre-allocating matrices:
MAX_NUMBER_OF_SPIKES = int(1e6)
MAX_NUMBER_OF_RECORDS = int(1e6)
MAX_NUMBER_OF_EVENTS = int(1e6)


def writeHeader(f,header):
    headerstr=''
    for k,v in header.items():
        k = 'header.'+k.strip()
        headerstr = headerstr+'{0} = {1};\n'.format(k,v)
    headerstr=headerstr.ljust(1024)
    f.write(headerstr.encode('ascii'))
    
def writeFrame(f, timestamp, recording_num, x):
    byteWritten = 0
    if x.size==1024:      
        byteWritten += f.write(np.array(timestamp).astype('<i8').tobytes())
        byteWritten += f.write(np.array(1024).astype('<i2').tobytes())
        byteWritten += f.write(np.array(recording_num).astype('<i2').tobytes())
        byteWritten += f.write(x.astype('>i2').tobytes())
        byteWritten += f.write(np.array([0,1,2,3,4,5,6,7,8,255]).astype(np.byte).tobytes())
    else:
        print('Data point not correct. Skipped')
    return byteWritten
    
def writeContinuousFile(fname,header,timestamp,x,recording_num=None,dtype=np.float):
    f = open(fname,'wb')
    writeHeader(f,header)

    noFrame = x.size//1024
    
    if dtype == np.float:
        #convert back the value to int according to the bitVolts
        x = np.round(x/np.float(header['bitVolts']))
    
    for i in range(noFrame):
        if recording_num is not None:
            writeFrame(f,timestamp[i],recording_num[i],x[i*1024:(i+1)*1024])
        else:
            writeFrame(f,timestamp[i],0,x[i*1024:(i+1)*1024])
    
    f.close()


def writeBinaryData(parentFolder,signals):
    """Write data in the flat binary format of openephys
    
    Arguments:
        parentFolder {str} -- base folder of the binary file
        signals {np.darray} -- input signal, should be in np.int16 format
    """
    #signals should be in time x channel format
    if signals.shape[0] < signals.shape[1]:
        signals = signals.T

    if signals.dtype != np.int16:
        raise TypeError('The input signals should be of type np.int16')

    # make parent folders
    folderpath = Path(parentFolder) / 'continuous' / 'openephys-100.0'
    folderpath.mkdir(parents=True, exist_ok=True)

    # write data file
    print('Writing binary file...')
    with (folderpath / 'continuous.dat').open('wb') as f:
        f.write(signals.tobytes())

    # create and write timestamp
    timestamps = np.arange(signals.shape[0],dtype='i8')
    np.save(str(folderpath/'timestamps.npy'), timestamps)

def load_OpenEphysRecording4BinaryFile(folder,
     source_prefix ='100', dtype=np.int16, num_data_channel=16,
     num_adc_channel =8, num_aux_channel = 3):
    """Load continuous data to be converted to flat binary files

    Arguments:
        folder {str} -- folder containing the continuous files
        num_tetrodes {int} -- number of tetrode in recording
        data_file_prefix {str} -- prefix of data file
        data_file_suffix {str} -- suffix of data file

    Keyword Arguments:
        dtype {np.dtype} -- dtype of the data in the continuous files (default: {float})
    """
    signal = []
    headers = []

    ADCList = [folder+f'/{source_prefix}_ADC{i+1}.continuous' for i in range(num_adc_channel)]
    ChList =[folder+f'/{source_prefix}_CH{i+1}.continuous' for i in range(num_data_channel)]
    AUXList = [folder+f'/{source_prefix}_AUX{i+1}.continuous' for i in range(num_aux_channel)]

    fileList = ChList + AUXList + ADCList

    for i,fname in enumerate(fileList):
        # fname = folder+'/'+data_file_prefix+str(i+1)+data_file_suffix+'.continuous'
        dataFile = loadContinuousFast(fname, dtype=dtype)
        x= dataFile['data']
        headers.append(dataFile['header'])

        if i==0:
            #preallocate array on first run
            signal = np.zeros((len(fileList),x.shape[0]),dtype=dtype)
        signal[i,:] = x
    return signal,headers

def writeStructFile(filename,headers):
    """Write the structure file for loading binary files in open-ephys GUI
    
    Arguments:
        filename {str} -- name of the structure file, using structure.oebin
        headers {list} -- list of headers returned from load_OpenEphysRecording4BinaryFile
    """
    structDict = {'GUI version':'0.4.5','continuous':[], 'events':[], 'spikes':[]}

    structDict['continuous'] = [{
        "folder_name":"openephys-100.0/",
        "sample_rate":headers[0]['sampleRate'],
        "source_processor_name":"Demo source",
        "source_processor_id":100,
        "source_processor_sub_idx":0,
        "recorded_processor":"Demo source",
        "recorded_processor_id":100,
        "num_channels":len(headers),
        "channels":[]
    }]

    #assemble channel data
    channels = []
    # print(headers)
    for i,h in enumerate(headers):
        channels.append({
            
            "channel_name": h['channel'],
            "description":"Demo data channel",
            "identifier":"genericdata.continuous",
            "history":"Demo source",
            "bit_volts":float(h['bitVolts']),
            "units":"uV",
            "source_processor_index":i,
            "recorded_processor_index":i
                
        })

    structDict['continuous'][0]['channels'] = channels

    with open(filename,'w') as f:
        f.write(json.dumps(structDict,indent=4))
    
def loadContinuousFast(filepath, dtype=float):
    #A much faster implementation for loading continous file
    #load all data at once rather than by chunks

    assert dtype in (float, np.int16), \
        'Invalid data type specified for loadContinous, valid types are float and np.int16'

    print("Loading continuous data...")

    ch = { }

    #read in the data
    f = open(filepath,'rb')

    fileLength = os.fstat(f.fileno()).st_size

    # calculate number of samples
    recordBytes = fileLength - NUM_HEADER_BYTES
    if  recordBytes % RECORD_SIZE != 0:
        raise Exception("File size is not consistent with a continuous file: may be corrupt")
    nrec = recordBytes // RECORD_SIZE
    nsamp = nrec * SAMPLES_PER_RECORD
    # pre-allocate samples
    samples = np.zeros(nsamp, dtype)
    timestamps = np.zeros(nrec)
    recordingNumbers = np.zeros(nrec)
    indices = np.arange(0, nsamp + 1, SAMPLES_PER_RECORD, np.dtype(np.int64))

    header = readHeader(f)

    buffer = f.read()
    data_tmp=np.frombuffer(buffer,np.dtype('>i2')) #read everything into a large buffer
    data_tmp = data_tmp.reshape(int(len(data_tmp)/(RECORD_SIZE/2)),int(RECORD_SIZE/2)) #reshape it into each chunk
    
    timestamps = data_tmp[:,:4].ravel().view('<i8') #reinterpret the timestamp
    N = data_tmp[:,4].ravel().view('<u2') #reinterpret number of recording
    recordingNumbers = data_tmp[:,5].ravel().view('>u2') #reintepret the recording number
    
    if np.any(N!=SAMPLES_PER_RECORD):
        raise Exception('Found corrupted record at '+np.where(N!=SAMPLES_PER_RECORD))
        
    if dtype == float: # Convert data to float array and convert bits to voltage.
        samples=data_tmp[:,6:6+SAMPLES_PER_RECORD].ravel() * float(header['bitVolts']) # #extract the data
    else:  # Keep data in signed 16 bit integer format.
        samples=data_tmp[:,6:6+SAMPLES_PER_RECORD].ravel()    
     

    ch['header'] = header
    ch['timestamps'] = timestamps
    ch['data'] = samples  # OR use downsample(samples,1), to save space
    ch['recordingNumber'] = recordingNumbers
    f.close()
    return ch


def convertContinuous2Binary(continuousFolder, binaryFolder):
    """Convert continuous files to float binary format
    
    Arguments:
        continuousFolder {str} -- folder of continuous files
        binaryFolder {str} -- target folder of flat binary format
    """

    data,headers = load_OpenEphysRecording4BinaryFile(continuousFolder)
    writeBinaryData(binaryFolder,data)
    writeStructFile(binaryFolder+'/structure.oebin',headers)


