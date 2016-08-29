################################################################################
# Author(s): Matthew Connolly
# Conventions"
#    functions: lowercase_with_underscores()
#    classes: UpperCase
#    variables: camelCase"
################################################################################
#_________________________________________________________________________Import
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
from struct import *
import peakdetect
import pylab
#________________________________________________________________________Classes
class OverheadAnalyzer(object):
    def __init__(self, pathToFile):
        self.sampleFreq = None
        self.sampleRes = None
        self.numSamples = None
        self.numChannels = None

        
        waveFile = wave.open(pathToFile)
        self.sampleFreq = waveFile.getframerate()
        self.sampleRes = waveFile.getsampwidth()
        self.numSamples = waveFile.getnframes()
        self.numChannels = waveFile.getnchannels()
        
        self.data = self.unpack_audio(self.numChannels, 
                                      self.sampleRes, 
                                      waveFile.readframes(-1))
        
        self.plot_waveforms()
        self.find_peaks()
        
    def unpack_audio(self,nChannels, sampWidth, data):
        numSamples, remainder = divmod(len(data), sampWidth * nChannels)
        if remainder > 0:
            raise ValueError("The length of the data is not a multiple")
        if sampWidth > 4:
            raise ValueError("sampwidth must not be greater than 4.")

        if sampWidth == 3:
            a = np.empty((numSamples, nChannels, 4), dtype=np.uint8)
            raw_bytes = np.fromstring(data, dtype=np.uint8)
            a[:, :, :sampWidth] = raw_bytes.reshape(-1, nChannels, sampWidth)
            a[:, :, sampWidth:] = (a[:, :, sampWidth - 1:sampWidth] >> 7) * 255
            result = a.view('<i4').reshape(a.shape[:-1])
        else:
            # 8 bit samples are stored as unsigned ints; others as signed ints.
            dt_char = 'u' if sampWidth == 1 else 'i'
            a = np.fromstring(data, dtype='<%s%d' % (dt_char, sampWidth))
            result = a.reshape(-1, nChannels)
        return result
    
    def plot_waveforms(self):
        fig, axarr = plt.subplots(2, sharex=True)
        
        x = np.arange(0,self.numSamples)
        axarr[0].plot(x, self.data[:,0])
        axarr[0].set_title("Stereo Output")
        axarr[1].plot(x, self.data[:,1])
        plt.show()
        

        x = np.arange(0,self.numSamples)
        #y = np.arange(-8388608, 8388608)
        #plt.plot(self.data[:,1])
        #plt.show()
    def find_peaks(self):
        _max,_min = peakdetect.peakdetect(self.data[:,0], 
                                          np.arange(0,self.numSamples), 
                                          4000,
                                          0.5)
        xm = [p[0] for p in _max]
        ym = [p[1] for p in _max]
        xn = [p[0] for p in _min]
        yn = [p[1] for p in _min]
        
        plot = pylab.plot(np.arange(0,self.numSamples), self.data[:,0])
        pylab.hold(True)
        pylab.plot(xm, ym, "r+")
        pylab.plot(xn, yn, "g+")
        
        
        pylab.show()        
    def overhead_peak_detect(self):
        threshold = 112000
        minDur = 31650
        curLeftPeak = 0
        curRightPeak = 0
        countDownLeft = 0
        countDownRight = 0
        peakListLeft = 
        peakListRight = []
        for i,dataPoint in enumerate(self.data):
            if i != 0:
                if dataPoint[0] > threshold or dataPoint[1] > threshold:
                    if dataPoint[0] > curLeftPeak:
                        curLeftPeak = dataPoint[0]
                        countdownLeft = minDur
                        
                    if dataPoint[1] > curRightPeak:
                        curRightPeak = dataPoint[1]
                        countDownRight = minDur
                if countDownLeft:
                    if countDownLeft == 1:
                        peakListLeft.append([curLeftPeak,(i - 31649)])
                    countDownLeft = countDownLeft - 1

                if countDownRight:
                    countDownRight = countDownRight - 1
                
                    
        

        

        


        
#___________________________________________________________________________Main
def main():
    oHA = OverheadAnalyzer('MM-OH.wav')
     
if __name__ == "__main__":
    main()
    


#3:25

#def stringList_to_intList(stringList):
    #return np.fromstring(stringList, 'Int16')
#def print_wave_details(wF):
    #print "Number of Channels : " + str(wF.getnchannels())
    #print "Sample Width : " + str(wF.getsampwidth())
    #print "Sample Frequency : " + str(wF.getframerate()) + " Hz"
    #print "Number of Samples : " + str(wF.getnframes())
    #print "Track Duration : " + sec_to_min((wF.getnframes() / wF.getframerate()))

#def sec_to_min(timeSec):
    #minutes = timeSec / 60
    #seconds = timeSec % 60
    #return str(minutes) + ":" + str(seconds)

#"""
#Wavefile data is stored as a list of strings
#""" 
#def convert_to_int(byteList):
    #tempList = []
    
#def unpack_wav_file(wF):
    #rawData = wF.readframes(4)
    #print str(rawData)
    #numData = unpack("%dh" % (12), rawData)
    #print "Unpack Wave File"
    #print wF.readframes(2).decode("utf-8")
    #print sys.getsizeof(wF.readframes(2))
    ##print wF.readframes(-1)
    

#def split_wav_file(wF):
    #data = unpack("%dh" % (wF.getnchannels()*wF.getnframes()), wF.readframes(-1))

    #temp =  [wF.readframes(-1)[chanOffset::wF.getnchannels()] for chanOffset in range(wF.getnchannels())]
    #return temp




##Output Wave File Details
#print_wave_details(waveFile)
##Unpack Wave file
#numWave = unpack_wav_file(waveFile)
##Split stereo wave file
##splitWave = split_wav_file(waveFile)
##Convert String Lists to integers
##print waveFile.readframes(-1)
