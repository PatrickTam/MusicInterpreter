#from https://www.johndcook.com/blog/2016/02/10/musical-pitch-notation/
from math import log, pow

A4 = 440
C0 = A4*pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
def pitch(freq):
    h = round(12*log(freq/C0, 2))
    octave = h // 12
    n = h % 12
    return name[int(n)] + str(octave)
