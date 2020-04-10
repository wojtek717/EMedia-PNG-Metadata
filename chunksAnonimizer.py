from numpy import savetxt

def listToString(list):
    s = ""
    counter = 0

    for element in list:
        s += element
        if(counter < (len(list) - 1)):
            s += " "
        counter += 1
    return s


def anonimize_chunks(chunksArray):
    onlyCriticalChunks = []
    file = open("anonimized.txt","a")
    s = ""

    chunkIterator = 0
    while chunkIterator < len(chunksArray):
        if((chunksArray[chunkIterator].getChunkTypeText() == 'IHDR') or
            (chunksArray[chunkIterator].getChunkTypeText() == 'PLTE') or
            (chunksArray[chunkIterator].getChunkTypeText() == 'IDAT') or
            (chunksArray[chunkIterator].getChunkTypeText() == 'IEND')):

            onlyCriticalChunks.append(chunksArray[chunkIterator].getChunk())
            
        chunkIterator += 1
    
    tmp = onlyCriticalChunks[0].lengthArray
    mapka = map(str, tmp)
    listka = list(mapka)
    s = listToString(listka)
    file.write(s)