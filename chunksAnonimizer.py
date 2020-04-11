def getPNGSygnatureAsBytes():
    sygnature = [137, 80, 78, 71, 13, 10, 26, 10]
    return bytearray(sygnature)

def anonimize_chunks(chunksArray):
    isIDATChain = False
    wasIDAT = False

    fileName = input("Enter file name (without extension)")
    fileName += ".png"
    file = open(fileName, "a+b")

    # Write PNG file sygnature
    file.write(getPNGSygnatureAsBytes())

    # Save only critical chunks
    chunkIterator = 0
    while chunkIterator < len(chunksArray):
        if((chunksArray[chunkIterator].getChunkTypeText() == 'IHDR') or
            (chunksArray[chunkIterator].getChunkTypeText() == 'PLTE') or
            (chunksArray[chunkIterator].getChunkTypeText() == 'IDAT') or
            (chunksArray[chunkIterator].getChunkTypeText() == 'IEND')):

            # Some information can be stored in IDAT chunks after main IDATs chain which are NOT displayed
            # Remove that IDAT chunks
            if(chunksArray[chunkIterator].getChunkTypeText() == 'IDAT' and wasIDAT == False):
                wasIDAT = True
                isIDATChain = True

            if(chunksArray[chunkIterator].getChunkTypeText() != 'IDAT' and isIDATChain):
                isIDATChain = False

            if(chunksArray[chunkIterator].getChunkTypeText() != 'IDAT'):
                file.write(chunksArray[chunkIterator].getChunkAsList())
            elif (isIDATChain):
                file.write(chunksArray[chunkIterator].getChunkAsList())
            
        chunkIterator += 1