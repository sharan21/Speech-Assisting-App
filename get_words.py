import pyaudio
import wave
import numpy as np
import math
from pydub import AudioSegment
from pydub.silence import split_on_silence
from import_words import getNumberOfFiles, getNumberOfSentences, importAllFromDir, plotAll

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()
RECORD_SECONDS = 10
minimumWordSize = 300  # if the size of the word is <= this, reject the chunk
maximumWordSize = 2000

def startRecording(seconds = RECORD_SECONDS):
    frames = []

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("* recording")

    for i in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()

    # commented below code to prevent "cannot find default device error" when opened multiple times
    # p.terminate()

    return frames

def detectnoiselevel(): # in dBFS

    print ("detecting noise level...")
    print ("recording for 5 seconds")
    frames = startRecording(5)
    storeWavFile(frames, './noise/noisetest.wav')

    data , _ = importAllFromDir('./noise')
    print (data.shape)
    data = data[:,1000:]

    print (20*math.log10(np.mean(data)/32767))





def storeWavFile(frames, filename, verbosity = True):
    print (filename) if verbosity else 0
    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    # print ("Done recording, stored in output.wav") if verbosity else 0


def splitWavFileAndStore(filename, minsillen= 100, silthresh = -60):

    line = AudioSegment.from_wav(filename)

    audio_chunks = split_on_silence(line, min_silence_len=minsillen, silence_thresh=silthresh)  # isolation of words is done here

    rejectedOffset = 0

    for i, chunk in enumerate(audio_chunks): # audio_chunks is a python list

        if(checkChunk(chunk,i, minimumWordSize, maximumWordSize)): #
            rejectedOffset = rejectedOffset + 1
            continue

        out_file = DEFAULT_CHUNKNAME.format(i-rejectedOffset+fileOffset)
        print("size of chunk{}: {} ".format(i-rejectedOffset+fileOffset, len(chunk)))
        print ("exporting", out_file)
        chunk.export(out_file, format="wav")
        print("done exporting...")
        temp = i

    print("Total number of files:", temp+1)

    return temp+1

def checkChunk(chunk,i, minimumWordSize=minimumWordSize, maximumWordSize=maximumWordSize): # check if the chunk is valid or not, according to size of chunk.

    # (len(chunk) <= minimumWordSize) or (len(chunk) > maximumWordSize and askUser() == 0)
    if( (len(chunk) > maximumWordSize)):
        print("rejected chunk{}".format(i))
        print ("too long")
    if((len(chunk) <= minimumWordSize )):
        print("rejected chunk{}".format(i))
        print ("too short")



    return ((len(chunk) <= minimumWordSize ) or (len(chunk) > maximumWordSize))

def askUser():

    choice = input("Press 1 for LL sentence input, Press 0 for Non LL sentence input. ")
    global RECORD_SECONDS
    RECORD_SECONDS = input("How many seconds do you want to record for? ")

    if choice == 0:
        print("You are recording Non LL sentences...")
        global WAVE_OUTPUT_FILENAME
        global DEFAULT_CHUNKNAME
        global minimumWordSize
        global fileOffset
        global sentenceOffset
        global silence_thresh
        global min_silence_len
        min_silence_len = 20
        sentenceOffset = getNumberOfFiles("../nonLL-sentences")
        fileOffset = getNumberOfFiles("../nonLL_chunks")
        WAVE_OUTPUT_FILENAME = "../nonLL-sentences/output" + str(sentenceOffset) + ".wav"
        DEFAULT_CHUNKNAME = "../nonLL_chunks/chunk{}.wav"
        minimumWordSize = 300
        print (fileOffset)


    else:
        print (fileOffset)
        print("You are recording LL sentences...")

    return choice


if __name__ == '__main__':

    # fileOffset = getNumberOfFiles()  # makes sure that old chunks are not re-written
    # sentenceOffset = getNumberOfSentences()  # makes sure that old sentences are not re-written
    # WAVE_OUTPUT_FILENAME = "../LL-sentences/sample" + str(sentenceOffset) + ".wav"
    # DEFAULT_CHUNKNAME = "../LL_chunks/chunk{}.wav"
    #
    #
    #
    # # min_silence_len = 30  # default for LL
    # # silence_thresh = -60  # default for LL
    #
    #
    #
    # askUser()
    # frames = startRecording(RECORD_SECONDS) # get frames from user
    # storeWavFile(frames, WAVE_OUTPUT_FILENAME)
    # splitWavFileAndStore(WAVE_OUTPUT_FILENAME)

    detectnoiselevel()


