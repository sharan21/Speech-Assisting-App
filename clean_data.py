from import_words import *
import numpy as np


betaForExponentialAverage = 0.8
# use b = 0 to mirror the original data
# as beta increases, oscillations decrease

fixedChunkSize = 200
# each word chunk has a fixed size to feed into the tf graph

densityOfChunk = 100



def reduceDensity(soundDataHere):

    cleanSoundData = []

    for i in range(numberOfFiles):

        k = 0
        bufferForCleaning = []

        for j in range(0, soundDataHere[i].size-1, densityOfChunk):

            bufferForCleaning.insert(k, soundDataHere[i][j])
            k += 1

        cleanSoundData.append(np.absolute(bufferForCleaning))

    return cleanSoundData



def weightedAverage(soundDataHere, beta):

    # newData[i] = beta*newData[i-1] + (1-beta)*soundData[i]

    print("Finding the weighted exponential average...")
    print

    newSoundData = []

    for i in range(numberOfFiles):

        bufferHere = []

        for j in range(0, soundDataHere[i].size - 1, 1):

            if j == 0:
                bufferHere.append(0)
            else:
                biasCorrection = 1/(1-pow(beta, j))
                bufferHere.append(beta*bufferHere[j-1] + (1-beta)*soundDataHere[i][j] * biasCorrection)

        newSoundData.append(np.absolute(bufferHere))

        print("done finding the exponential average...")

    return newSoundData

def trimChunks(soundData, fixedSize): # trim the chunk to get fixed size

    print("trimming all the chunks...")
    print

    for i in range(numberOfFiles):

        diffInSize = soundData[i].size - fixedSize

        if soundData[i].size % 2 == 0:
            temporaryBuffer = np.split(soundData[i], [diffInSize/2, soundData[i].size-diffInSize/2])
        else:
            temporaryBuffer = np.split(soundData[i], [diffInSize / 2, soundData[i].size - 1 - diffInSize / 2])

        soundData[i] = temporaryBuffer[1] # take the middle slice of the split soundData array


    return soundData

def assertConstantChunkSize(soundData):

    print("asserting that all the chunks are of constant size...")
    print
    size = soundData[0].size
    status = 1
    for i in range(1,numberOfFiles,1):
        if soundData[i].size != soundData[i-1].size:
            status = 0

    if status == 1:
        print("Done checking...: same size")
    else:
        print("Done checking...: non constant size")


def printChunkSizeDiff(soundData, fixedSize):

    for i in range(numberOfFiles):
        diffInSize = fixedSize - soundData[i].size
        print("difference in size for chunk{}: is {}".format(i, diffInSize))







if __name__ == "__main__":
    numberOfFiles = 4

    soundData = importAll(numberOfFiles)

    soundData = reduceDensity(soundData)

    soundData = weightedAverage(soundData, betaForExponentialAverage)

    trimChunks(soundData, fixedChunkSize)

    assertConstantChunkSize(soundData)

    plotAllMaxFour(soundData, numberOfFiles)







