## Adapted from AudioAmplitude.py
## MSI-Keyboard-Lights v1.0.1 by CosmicSubspace
## https://github.com/CosmicSubspace/MSI-Keyboard-Lights
## Licensed under the MIT License.

if __name__=="__main__":
    import sys
    import traceback
    ## This will make it so the console won't close on its own when an exception is raised.
    def show_exception_and_exit(exc_type, exc_value, tb):
        if not str(exc_value)=='name \'exit\' is not defined':
            print("\n\n---ERROR---\n")
            traceback.print_exception(exc_type, exc_value, tb)
            input("\nPress any key to exit.")
        sys.exit(-1)
    sys.excepthook = show_exception_and_exit

import pyaudio
import time
import struct
import math
from AorusKeyboardRgb import set_static

## Setup
audio = pyaudio.PyAudio()
deg=0
reference=0
lastTime=time.time()

## PyAudio returns a byes object for the recording.
## We have to convert that to a float before doing stuff
## Outputs: A list of tuples, each being a tuple of R and L data. Or was it L and R....
def stereo_from_bytes(b):
    res=[]
    #print(b)
    for i in range(0,len(b),4):
        res.append((struct.unpack("=h",b[i:i+2])[0]/32768,
                    struct.unpack("=h",b[i+2:i+4])[0]/32768))
    return res

## get the RMS value of the stereo data.
## pretty straghtforward.
def rms_stereo(dat):
    r=0
    l=0
    for i in dat:
        r+=i[0]*i[0]
        l+=i[1]*i[1]
    return (math.sqrt(r/len(dat)/2),math.sqrt(l/len(dat)/2))

## Recording callback function
def cb(in_data,frame_count,time_info,status_flags):

    global current_data
    global reference
    global lastTime

    currentTime=time.time()
    print("Time delta: {:.03f}".format(currentTime-lastTime),end="\t")
    lastTime=currentTime

    ## We convert the data received from PyAudio
    ## And we take the RMS value of that.
    ## RMS is a good representation of loudness here
    ## ...I think?
    dat=rms_stereo(stereo_from_bytes(in_data))

    ## We calculate a "Reference Value".
    ## Since we sometimes turn our volume up, listen to quiet songs, etc,
    ## Using the same range of loudness to map the brightness of the keyboard
    ## won't work well.
    ## So we make a dynamically changing reference value
    ## Used to map the loudness to RGB values.

    ## This is the average(sorta) value of the recent loudness values.
    ## It changes to about the average value of the currently playing audio,
    ## But does this in a smooth manner.
    reference=reference*0.99+((dat[0]+dat[1])/2)*0.01

    ## If we stop there, we will get strange results when nothing is playing
    ## because the reference will converge to zero.
    ## So we set a minimum value here. (0.1% of maximum amplitude)
    if reference<0.001:
        reference=0.001

    # print("Reference: {:.04f}".format(reference),end="\t")

    ## We map the amplitude to the color value.
    ## If the amplitude is exactly at reference, it is mapped to 0.5

    ## The ^2 here makes things look a bit better
    ## It gives the brightness a bit more of an abrupt ramp.

    # val_L=(dat[0]/reference/2)**2
    val_L=(dat[0]/reference/2)
    # val_R=(dat[1]/reference/2)**2
    val_R=(dat[1]/reference/2)
    # print("L: {:.04f}\tR: {:.04f}".format(val_L,val_R),end="\t")

    vis_n=10
    textvis_L=min(round(val_L*vis_n),vis_n)
    textvis_R=min(round(val_R*vis_n),vis_n)
    # print("["+" "*(vis_n-textvis_L)+"#"*textvis_L+" L/R "+"#"*textvis_R+" "*(vis_n-textvis_R)+"]")

    brightness = (((val_L + val_R) / 2) - reference)
    brightness = 10 * round(10*brightness)
    if brightness > 100:
        brightness = 100
    elif brightness < 0:
        brightness = 0
    
    # # Can be divided into partitions for clearer difference
    # if brightness < 30:
    #     brightness = 10
    # elif brightness < 70:
    #     brightness = 50
    # else:
    #     brightness = 90

    print(brightness)
    set_static('GREEN', brightness)
    return (None, pyaudio.paContinue)

print("Which audio device should be used?")
print("Some of them might not return a sound, and some may just throw an error.")
print("A device called Stereo Mix is a input loopback for audio output, and should be selected if you want to visualize audio output.")
print("If you don't know, just guess until you get the one you want.\n")
for i in range(audio.get_device_count()):
    try:
        print(i+1,audio.get_device_info_by_index(i)["name"],sep="\t")
    except UnicodeEncodeError:
        print("???",sep="\t")
idx=int(input("\nEnter index: "))-1

## PyAudio code.
## See the PyAudio docs for an explanation.
s=audio.open(format=pyaudio.paInt16,
             channels=2,
             rate=44100,
             input=True,
             frames_per_buffer=2048,
             input_device_index=idx,
             stream_callback=cb)

## The process must not die.
while True:
    time.sleep(0.1)