import pyaudio
import wave
from pydub import AudioSegment
from pydub.silence import split_on_silence
from import_words import getNumberOfFiles, getNumberOfSentences

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
frames = []
p = pyaudio.PyAudio()
RECORD_SECONDS = 10
minimumWordSize = 200 # if the size of the word is <= this, reject the chunk

countOffset = getNumberOfFiles() # makes sure that old chunks are not re-written
fileOffset = getNumberOfSentences() # makes sure that old sentences are not re-written

WAVE_OUTPUT_FILENAME = "LL-sentences/output"+str(fileOffset)+".wav"


def startRecording():

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("* recording")

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()


def storeWavFile():
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    print("Done recording, stored in output.wav")



def splitWavFileAndStore(): # run this after output.wav is obtained

    line = AudioSegment.from_wav(WAVE_OUTPUT_FILENAME)

    audio_chunks = split_on_silence(line, min_silence_len=60, silence_thresh=-30)  # isolation of words is done here

    # next step is to name and export all the chunks, into ./LL_chunks

    rejectedOffset = 0


    for i, chunk in enumerate(audio_chunks): # audio_chunks is a python list

        if(checkChunk(chunk,i, minimumWordSize)): #
            rejectedOffset = rejectedOffset + 1
            continue

        out_file = "./LL_chunks/chunk{0}.wav".format(i-rejectedOffset+countOffset)
        print("size of chunk{}: {} ".format(i-rejectedOffset+countOffset, len(chunk)))
        print ("exporting", out_file)
        chunk.export(out_file, format="wav")
        print("done exporting...")

    print("Total number of files:", i+1)

    return i+1

def checkChunk(chunk, i, minimumWordSize): # check if the chunk is valid or not, according to size of chunk

    if(len(chunk) <= minimumWordSize):
        print("rejected chunk{}".format(i))

    return len(chunk) <= minimumWordSize


if __name__ == '__main__':

    print(WAVE_OUTPUT_FILENAME)

    # startRecording()
    # storeWavFile()
    # splitWavFileAndStore()
    
    
    
