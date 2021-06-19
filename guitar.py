# import numpy as np
# import simpleaudio as sa
# from itertools import repeat
#
# sargamdict = {"sa":261,
#              "re":294,
#              "ga":330,
#              "ma":349,
#              "pa":392,
#              "dha":440,
#              "ni":494,
#              "sa":515}
#
# def play_audio(audio):# normalize to 16-bit range
#     audio *= 32767 / np.max(np.abs(audio))
#     # convert to 16-bit data
#     audio = audio.astype(np.int16)
#
#     # start playback
#     play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
#
#     # wait for playback to finish before exiting
#     play_obj.wait_done()
#
# T = 0.25
# sample_rate = 44100
# TxS = int(T * sample_rate)
# t = np.linspace(0, T, TxS, endpoint=False)
#
# Sa_note = np.sin(sargamdict["sa"] * t * 3 * np.pi)
# Re_note = np.sin(sargamdict["re"] * t * 3 * np.pi)
# Ga_note = np.sin(sargamdict["ga"] * t * 3* np.pi)
# Ma_note = np.sin(sargamdict["ma"] * t * 3 * np.pi)
# Pa_note = np.sin(sargamdict["pa"] * t * 3 * np.pi)
# Dha_note = np.sin(sargamdict["dha"] * t * 3 * np.pi)
# Ni_note = np.sin(sargamdict["ni"] * t * 3 * np.pi)
# # Sa1_note = np.sin(sargamdict["sa1"] * t * 3 * np.pi)
#
# get_pause  = lambda seconds: repeat(0, int(seconds * sample_rate))
# pause_note=list(get_pause(0.01))
#
# sargam = np.hstack((Sa_note,pause_note,Re_note,pause_note,Ga_note,
#                    pause_note,Ma_note, pause_note,Pa_note, pause_note,
#                     Dha_note, pause_note,Ni_note, pause_note))
#
# import wavio
# fs = 44100
# s2 = np.append(sargam,sargam[::-1])
# wavio.write("mp3/pythonsargam.wav", s2, fs, scale=None, sampwidth=2)


# Read in a WAV and find the freq's
import pyaudio
import wave
import numpy as np

chunk = 1024

# open up a wave

wf = wave.open('pythonsargam.wav', 'rb')
swidth = wf.getsampwidth()
RATE = wf.getframerate()
# use a Blackman window
window = np.blackman(chunk)
# open stream
p = pyaudio.PyAudio()
channels = wf.getnchannels()
stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = channels,
                rate = RATE,
                output = True)

# read some data
data = wf.readframes(chunk)
# play stream and find the frequency of each chunk
print('switdth {} chunk {} data {} ch {}'.format(swidth,chunk,len(data), channels))
while len(data) == chunk*swidth*channels:
    # write data out to the audio stream
    stream.write(data)
    # unpack the data and times by the hamming window
#    indata = np.array(wave.struct.unpack("%dh"%(len(data)/(swidth)),data))*window
    indata = np.fromstring(data, dtype='int16')
    # deinterleave, select 1 channel
    channel0 = indata[0::channels]

    # Take the fft and square each value
    fftData=abs(np.fft.rfft(indata))**2
    # find the maximum
    which = fftData[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(fftData)-1:
        y0,y1,y2 = np.log(fftData[which-1:which+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        thefreq = (which+x1)*RATE/chunk
        print ("The freq is %f Hz." % (thefreq))
    else:
        thefreq = which*RATE/chunk
        print ("The freq is %f Hz." % (thefreq))
    # read some more data
    data = wf.readframes(chunk)
if data:
    stream.write(data)
stream.close()
p.terminate()
