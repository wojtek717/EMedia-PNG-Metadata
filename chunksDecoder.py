import deflateDecompresser

def decode_chunks(chunksArray):
    chunkIterator = 0
    while chunkIterator < len(chunksArray):
        if(chunksArray[chunkIterator].getChunkTypeText() == 'IHDR'):
            decode_IHDR(chunksArray[chunkIterator])
        
        if(chunksArray[chunkIterator].getChunkTypeText() == 'tEXt'):
            decode_tEXt(chunksArray[chunkIterator])

        if(chunksArray[chunkIterator].getChunkTypeText() == 'zTXt'):
            decode_zTXt(chunksArray[chunkIterator])

        if(chunksArray[chunkIterator].getChunkTypeText() == 'iTXt'):
            decode_iTXt(chunksArray[chunkIterator])

        if(chunksArray[chunkIterator].getChunkTypeText() == 'IDAT'):
            decode_IDAT(chunksArray[chunkIterator])
        
        #TODO add if statements for other chunks then handle their decode methods
        
        chunkIterator += 1

##### IHDR Chunk #####
def decode_IHDR(ihdrChunk):
    width = ihdrChunk.dataArray[3] | (ihdrChunk.dataArray[2]<<8) | (ihdrChunk.dataArray[1]<<16) | (ihdrChunk.dataArray[0]<<24)
    height = ihdrChunk.dataArray[7] | (ihdrChunk.dataArray[6]<<8) | (ihdrChunk.dataArray[5]<<16) | (ihdrChunk.dataArray[4]<<24)
    bitDepth = ihdrChunk.dataArray[8]
    colorType = ihdrChunk.dataArray[9]
    compressionMethod = ihdrChunk.dataArray[10]
    filterMethod = ihdrChunk.dataArray[11]
    interlaceMethod = ihdrChunk.dataArray[12]

    print("Width = " + str(width))
    print("Height = " + str(height))
    print("Bit Depth = " + str(bitDepth) + " bits per sample/palette index")
    decode_IHDRcolorType(colorType, bitDepth)
    print(decode_IHDRcompressionMethod(compressionMethod))
    print(decode_IHDRfilterMethod(filterMethod))
    print(decode_IHDRinterlaceMethod(interlaceMethod))

def decode_IHDRcolorType(colorType, bitDepth):
    allowedBitDepth = {}
    sampleDepth = bitDepth

    if(colorType == 0):
        print("Color type = Each pixel is a grayscale sample")
        allowedBitDepth = {1, 2, 4, 8, 16}
    elif(colorType == 2): 
        print("Color type = Each pixel is an R,G,B triple")
        allowedBitDepth = {8, 16}
    elif(colorType == 3): 
        print("Color type = Each pixel is a palette index; a PLTE chunk must appear")
        allowedBitDepth = {1, 2, 4, 8}
        sampleDepth = 8
    elif(colorType == 4): 
        print("Color type = Each pixel is a grayscale sample, followed by an alpha sample")
        allowedBitDepth = {8, 16}
    elif(colorType == 6): 
        print("Color type = Each pixel is an R,G,B triple, followed by an alpha sample")
        allowedBitDepth = {8, 16}
    else:
        print("Color type = Invalid color type")    

    if bitDepth in allowedBitDepth:
        print("Bit Depth correct!")
        print("Sample Depth = " + str(sampleDepth) + " bits")
    else:
        print("Bit Depth INCORRECT. May pose problems with compression.")

def decode_IHDRcompressionMethod(compressionMethod):
    switcher = {
        0: "Compression method = Compression Method 0 (deflate/inflate)"
    }
    return switcher.get(compressionMethod, "Compression method = INVALID (not yet implemented)")

def decode_IHDRfilterMethod(filterMethod):
    switcher = {
        0: "Filter method = Filter Method 0 (adaptive filtering with five basic filter types)"
    }
    return switcher.get(filterMethod, "Filter method = INVALID (not yet implemented)")

def decode_IHDRinterlaceMethod(interlaceMethod):
    switcher = {
        0: "Interlace method = No interlace",
        1: "Interlace method = Adam7 interlace"
    }
    return switcher.get(interlaceMethod, "Interlace method = INVALID")

##### IDAT Chunk #####
def decode_IDAT(idatChunk):
    print(len( deflateDecompresser.decompress_text(idatChunk.dataArray)))
   

##### tEXt Chunk #####
def decode_tEXt(textualChunk):
    # Read and decode keyWord
    keyWord = []
    decodedKeyWord = ''

    chunkIterator = 0
    while textualChunk.dataArray[chunkIterator] != 0:
        keyWord.append(textualChunk.dataArray[chunkIterator])
        chunkIterator += 1
    decodedKeyWord = bytearray(keyWord).decode('utf-8')
    print('Key Word = ' + decodedKeyWord)

    chunkIterator += 1 # Skip null separator

    #Read and decode text
    text = []
    decodedText = ''

    while chunkIterator < len(textualChunk.dataArray):
        text.append(textualChunk.dataArray[chunkIterator])
        chunkIterator += 1
    decodedText = bytearray(text).decode('latin1')
    print('Text = ' + decodedText)

##### zTXt #####
def decode_zTXt(textualChunk):
    # Read and decode keyWord
    keyWord = []
    decodedKeyWord = ''

    chunkIterator = 0
    while textualChunk.dataArray[chunkIterator] != 0:
        keyWord.append(textualChunk.dataArray[chunkIterator])
        chunkIterator += 1
    decodedKeyWord = bytearray(keyWord).decode('latin1')
    print('Key Word = ' + decodedKeyWord)

    chunkIterator += 1 # Skip null separator

    # Read compress method
    compressMethon = textualChunk.dataArray[chunkIterator]
    chunkIterator += 1
    print('Compress Methon = ' + str(compressMethon))

    # Read compressed text from chunk
    text = []
    decodedText = ''

    while chunkIterator < len(textualChunk.dataArray):
        text.append(textualChunk.dataArray[chunkIterator])
        chunkIterator += 1

    # Decompress and decode text
    decodedText = deflateDecompresser.decompress_text(text).decode('latin1')
    print('Text = ' + decodedText)

##### iTXt Chunk #####
def decode_iTXt(textualChunk):
    # Read and decode keyWord
    keyWord = []
    decodedKeyWord = ''

    chunkIterator = 0
    while textualChunk.dataArray[chunkIterator] != 0:
        keyWord.append(textualChunk.dataArray[chunkIterator])
        chunkIterator += 1
    decodedKeyWord = bytearray(keyWord).decode('utf-8')
    print('Key Word = ' + decodedKeyWord)

    chunkIterator += 1 # Skip null separator

    # Check if text is compressed
    compressFlag = textualChunk.dataArray[chunkIterator]
    isCompressed = (compressFlag == 1)
    chunkIterator += 1

    # Read compress method
    compressMethon = textualChunk.dataArray[chunkIterator]
    chunkIterator += 1
    print('Compress Methon = ' + str(compressMethon))

    # Skip to the text data
    nullSeparatorCounter = 0
    while nullSeparatorCounter < 2:
        while textualChunk.dataArray[chunkIterator] != 0:
            chunkIterator += 1
        chunkIterator += 1
        nullSeparatorCounter += 1

    # Read compressed text from chunk
    text = []
    decodedText = ''

    while chunkIterator < len(textualChunk.dataArray):
        text.append(textualChunk.dataArray[chunkIterator])
        chunkIterator += 1

    # Decompress if compressed and decode text
    if(isCompressed):
        decodedText = deflateDecompresser.decompress_text(text).decode('utf-8')
    else:
        decodedText = bytearray(text).decode('utf-8')
    print('Text = ' + decodedText)
