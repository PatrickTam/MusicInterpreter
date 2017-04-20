#Some code based on - https://github.com/n00bsys0p/python-visualiser/blob/master/plotvals.py
#!/usr/bin/env python
import wave
import struct
import sys
import numpy as np
from math import sqrt
import matplotlib
matplotlib.use('Agg')
from matplotlib import pylab
import matplotlib.pyplot as plt
from scipy.io import wavfile
import detect_peaks
from scipy import fft, arange, ifft
import note
import MusicNotes
import record
import gui2

#filename = "17569__danglada__c-major.wav"
#filename = "94811__digifishmusic__c3-major-scale-piano.wav"
#filename = "235972__rom2014__emotional-piano-riff.wav"
#filename = "369934__nerkamitilia__piano-chromatic-scale-c5-to-b5.wav"
filename = "file6.wav"

def stereo_to_mono(hex1, hex2):
    """average two hex string samples"""
    return hex((ord(hex1)))

if __name__ == '__main__':
        print "Recording for 5 seconds..."
        record.startRecord()
        # Open the wave file and get info
        wave_file = wave.open(filename, 'r')
        data_size = wave_file.getnframes()
        sample_rate = wave_file.getframerate()
        print "Sample rate: %s" % sample_rate
        sample_width = wave_file.getsampwidth()
        print "Sample width: %s" % sample_width
        duration = data_size / float(sample_rate)
        channels = wave_file.getnchannels()
        print "Channels: %s" % channels

        # Read in sample data
        sound_data = wave_file.readframes(data_size * channels)

        # Close the file, as we don't need it any more
        wave_file.close()
        
        total_samples = data_size * channels

        if sample_width == 1: 
            fmt = "%iB" % total_samples # read unsigned chars
        elif sample_width == 2:
            fmt = "%ih" % total_samples # read signed 2 byte shorts
##        if channels == 1:
##                # Unpack the binary data into an array
##                unpack_fmt = '%dh' % (data_size)
##                #sound_data = struct.unpack(unpack_fmt, sound_data)
##                sound_data = struct.unpack('{}h'.format(data_size*channels), sound_data)
##        else:
##                sound_data = struct.unpack('{}h'.format(data_size*channels), sound_data)
##
        sound_data = struct.unpack_from ("%dh" % data_size * channels, sound_data)
        if channels == 2:
            sound_data = np.array (list (sound_data[0::2]))
        else:
            sound_data = np.array (sound_data)
        # Process many samples
        fouriers_per_second = 32 # Frames per second
        fourier_spread = 1.0/fouriers_per_second
        fourier_width = fourier_spread
        fourier_width_index = fourier_width * float(sample_rate)

        if len(sys.argv) < 3:
                if duration > 2:
                        length_to_process = int(duration)+1
                else:
                        length_to_process = int(duration)
        else:
                length_to_process = float(sys.argv[2])

        print "Fourier width: %s" % str(fourier_width)

        total_transforms = int(round(length_to_process * fouriers_per_second))
        fourier_spacing = round(fourier_spread * float(sample_rate))

        print "Duration: %s" % duration
        print "For Fourier width of "+str(fourier_width)+" need "+str(fourier_width_index)+" samples each FFT"
        print "Doing "+str(fouriers_per_second)+" Fouriers per second"
        print "Total " + str(total_transforms * fourier_spread)
        print "Spacing: "+str(fourier_spacing)
        print "Total transforms "+str(total_transforms)

        lastpoint=int(round(length_to_process*float(sample_rate)+fourier_width_index))-1

        sample_size = fourier_width_index
        freq = sample_rate / sample_size * np.arange(sample_size)

        f = open("hello.txt", 'w')
        noteList = []

        for offset in range(0, total_transforms):
                start = int(offset * sample_size)
                end = int((offset * sample_size) + sample_size -1)

                print "Frame %i of %i (%d seconds)" % (offset + 1, total_transforms, end/float(sample_rate))
                sample_range = sound_data[start:end]
                if not sample_range.any():
                    continue
                ## FFT the data
                #fft_data = abs(np.fft.fft(sample_range))
                #print sample_range
                n = len(sample_range)
                Y = fft(sample_range)/n
                Y = Y[range(n/2)]
                Y = abs(Y)
                peaks = detect_peaks.detect_peaks(Y, mph=5, mpd=6)
                #print peaks
                Yarr = []
                for val in peaks:
                        Yarr.append(Y[val])
                        #print Y[val], (val*32), note.pitch(val*32)
                if len(peaks):
                    currNoteList = []
                    print " "
                    print peaks*32
                    print Yarr
                    maxYarr = max(Yarr)
                    print "max = %d" % maxYarr
                    index = Yarr.index(maxYarr)
                    print note.pitch(peaks[index]*32)
                    currNoteList.append(note.pitch(peaks[index]*32))
                    f.write(repr(offset+1) + "-----------------------------------------------\n")
                    f.write("max = " + repr(maxYarr) + " pitch = " + repr(note.pitch(peaks[index]*32)) + "\n")
                    for val in peaks:
                        if Y[val] != maxYarr and maxYarr*1 < Y[val]:
                            print Y[val]
                            print note.pitch(val*32)
                            f.write("val = " + repr(Y[val]) + " pitch = " + repr(note.pitch(val*32)))
                            currNoteList.append(note.pitch(val*32))
                    if len(noteList) != 0:
                        if currNoteList[0] == noteList[-1].main:
                            if len(currNoteList) == noteList[-1].noteCount:
                                noteList[-1].addCount()
                            else:
                                noteList.append(MusicNotes.Notes(currNoteList[0], currNoteList[1:], len(currNoteList)))
                        else:
                            if len(currNoteList) == noteList[-1].noteCount and len(noteList[-1].noteList) != 0:
                                added = 0
                                for n in noteList[-1].noteList:
                                    if currNoteList[0] == n:
                                        noteList[-1].addCount()
                                        added = 1
                                        break
                                if not added:
                                    noteList.append(MusicNotes.Notes(currNoteList[0], currNoteList[1:], len(currNoteList)))
                            else:
                                noteList.append(MusicNotes.Notes(currNoteList[0], currNoteList[1:], len(currNoteList)))
                    else:
                        noteList.append(MusicNotes.Notes(currNoteList[0], currNoteList[1:], len(currNoteList)))
                else:
                    if len(noteList) > 0 and noteList[-1].main == "Rest":
                        noteList[-1].addCount()
                    else:
                        noteList.append(MusicNotes.Notes("Rest", [], 1))
                del Yarr
                f.write("-----------------------------------------------\n\n")
        print "DONE!"
        f.close()
        
        filtered = []
        for val in noteList:
            if val.count >= 3:
                filtered.append(val)
            elif len(filtered) > 0:
                filtered[-1].count += val.count
        noteList = filtered
        filtered = []
        prevVal = ""
        prevList = []
        for val in noteList:
            if prevVal == val.main:
                filtered[-1].count += val.count
            else:
                filtered.append(val)
            prevVal = val.main
        noteList = filtered

        onlyNotes = []
        noteVal = []
        for val in noteList:
            onlyNotes.append(val.main[:-2].replace("#", "Sharp"))
            count = val.count
            if count >= 3 and count < 6:
                val.value = "eigth"
                noteVal.append("eigth")
            elif count >= 6 and count < 14:
                val.value = "quarter"
                noteVal.append("quarter")
            elif count >= 14 and count < 29:
                val.value = "half"
                noteVal.append("half")
            elif count >= 29:
                val.value = "whole"
                noteVal.append("whole")
            val.printData()
        print onlyNotes
        gui2.writeGui(onlyNotes, noteVal)
