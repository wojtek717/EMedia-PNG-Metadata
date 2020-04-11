def getPNGSygnatureAsBytes():
    sygnature = [137, 80, 78, 71, 13, 10, 26, 10]
    return bytearray(sygnature)

def anonimize_chunks(chunksArray):
    file = open("anonimized.png","a+b")
    file.write(getPNGSygnatureAsBytes())

    chunkIterator = 0
    while chunkIterator < len(chunksArray):
        if((chunksArray[chunkIterator].getChunkTypeText() == 'IHDR') or
            (chunksArray[chunkIterator].getChunkTypeText() == 'PLTE') or
            (chunksArray[chunkIterator].getChunkTypeText() == 'IDAT') or
            (chunksArray[chunkIterator].getChunkTypeText() == 'IEND')):

            file.write(chunksArray[chunkIterator].getChunkAsList())
            
        chunkIterator += 1