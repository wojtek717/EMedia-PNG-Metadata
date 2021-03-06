import deflateDecompresser
import binascii
import imageAtributes
import directoryEntry
import tagTypes

def decode_chunks(chunksArray):
    chunkIterator = 0
    mergedIdatChunkData = []

    while chunkIterator < len(chunksArray):
        if(chunksArray[chunkIterator].getChunkTypeText() == 'IHDR'):
            imageAtributes = decode_IHDR(chunksArray[chunkIterator])
        
        if(chunksArray[chunkIterator].getChunkTypeText() == 'tEXt'):
            decode_tEXt(chunksArray[chunkIterator])

        if(chunksArray[chunkIterator].getChunkTypeText() == 'zTXt'):
            decode_zTXt(chunksArray[chunkIterator])

        if(chunksArray[chunkIterator].getChunkTypeText() == 'iTXt'):
            decode_iTXt(chunksArray[chunkIterator])

        if(chunksArray[chunkIterator].getChunkTypeText() == 'IDAT'):
            merge_IDATs(mergedIdatChunkData, chunksArray[chunkIterator])

        if(chunksArray[chunkIterator].getChunkTypeText() == 'IEND'):
            decode_IDAT(mergedIdatChunkData, imageAtributes)    
        
        if(chunksArray[chunkIterator].getChunkTypeText() == 'PLTE'):
            decode_PLTE(chunksArray[chunkIterator])

        if(chunksArray[chunkIterator].getChunkTypeText() == 'eXIf'):
            decode_eXIf(chunksArray[chunkIterator])

        if(chunksArray[chunkIterator].getChunkTypeText() == 'tIME'):
            decode_tIME(chunksArray[chunkIterator])
        
        chunkIterator += 1

##### IHDR Chunk #####
def decode_IHDR(ihdrChunk):

    print("\nIHDR: ")

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

    return (imageAtributes.ImageAtributes(width, height, bitDepth, colorType, compressionMethod, filterMethod, interlaceMethod))

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
def merge_IDATs(mergedIdatChunkData, idatChunk):
    mergedIdatChunkData += idatChunk.dataArray

def decode_IDAT(idatChunk, imageAtributes):

    print("\nIDAT: ")

    shouldHaveBytes = int(imageAtributes.width * imageAtributes.height * (imageAtributes.bitDepth / 8) + imageAtributes.height)
    decompressedByteArray = deflateDecompresser.decompress_text(idatChunk)

    #if(len(decompressedByteArray) > shouldHaveBytes):
    #    print("Redundant bytes: " + str(len(decompressedByteArray[shouldHaveBytes::])) + " ---> " + str(binascii.hexlify(decompressedByteArray[shouldHaveBytes::])))
    #else:
    #    print("No redundant bytes in IDAT chunk")
   
##### PLTE Chunk #####
def decode_PLTE(plteChunk):

    print("\nPLTE: ")

    length = int(plteChunk.getChunkLength()/3)
    print(str(length) + " palette(s) present.")

    for palette in range(length):
        print("Palette " + str(palette+1) + ":")
        r = plteChunk.dataArray[0+palette]
        g = plteChunk.dataArray[1+palette]
        b = plteChunk.dataArray[2+palette]
        print("R: " + str(r) + " G: " + str(g) + " B: " + str(b))

##### tEXt Chunk #####
def decode_tEXt(textualChunk):

    print("\ntEXt: ")

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

    print("\nzTXt: ")

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

    print("\niTXt: ")

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

##### tIME Chunk #####
def decode_tIME(timeChunk):

    print("\ntIME: ")

    year = timeChunk.dataArray[1] | (timeChunk.dataArray[0]<<8)
    month = timeChunk.dataArray[2]
    day = timeChunk.dataArray[3]

    hour = timeChunk.dataArray[4]
    minute = timeChunk.dataArray[5]
    secod = timeChunk.dataArray[6]

    date = str(day) + "/" + str(month) + "/" + str(year)
    time = str(hour) + ":" + str(minute) + ":" + str(secod)

    print("Last modification: " + date + " " + time)

##### eXIf Chunk #####
def decode_eXIf(exifChunk):

    print("\neXIf: ")

    header = []
    IFDsArray = []

    # We need that lists to return elements by arguments in function
    isNextIFDPasser = [True]
    chunkIteratorPasser = [0]

    # Read header
    chunkIterator = 0
    while chunkIterator < 8:
        header.append(exifChunk.dataArray[chunkIterator])
        chunkIterator += 1

    # Offset is defined in bits so devidy by 8 to get byte
    offset_to_ifd0 = int((header[7] | (header[6]<<8) | (header[5]<<16) | (header[4]<<24)) / 8)
    chunkIterator += offset_to_ifd0

    # Call that function again if offset to next IFD != 0
    # And get correct value of chunkIterator 
    while isNextIFDPasser[0] == True:
        IFDsArray.append(read_IFD(exifChunk, chunkIterator, isNextIFDPasser, chunkIteratorPasser))
        chunkIterator = chunkIteratorPasser[0]
    
    readDatafromIFD(IFDsArray, exifChunk)
    
def read_IFD(exifChunk, chunkIterator, isNextIFDPasser, chunkIteratorPasser):
    ifd = []

    # Read amount of DE
    ifd_number_of_directory_entries = exifChunk.dataArray[chunkIterator]
    chunkIterator += 1

    deIterator = 0
    while deIterator < ifd_number_of_directory_entries:
        tagId = []
        tagType = []
        count = []
        offset = []

        # Read tagID
        tagIdIterator = 0
        while tagIdIterator < 2:
            tagId.append(exifChunk.dataArray[chunkIterator])
            chunkIterator += 1
            tagIdIterator += 1

        # Read tagType
        tagTypeIterator = 0
        while tagTypeIterator < 2:
            tagType.append(exifChunk.dataArray[chunkIterator])
            chunkIterator += 1
            tagTypeIterator += 1

        # Read tag's count
        countIterator = 0
        while countIterator < 4:
            count.append(exifChunk.dataArray[chunkIterator])
            chunkIterator += 1
            countIterator += 1

        # Read offset to data
        offsetIterator = 0
        while offsetIterator < 4:
            offset.append(exifChunk.dataArray[chunkIterator])
            chunkIterator +=1
            offsetIterator += 1
        
        # Save DE to IFD list
        ifd.append(directoryEntry.DirectoryEntry(tagId, tagType, count, offset))
        deIterator += 1

    # Read offset to next IFD
    offset_to_next_IFDArray = []
    offsetIterator = 0
    while offsetIterator < 4:
        offset_to_next_IFDArray.append(exifChunk.dataArray[chunkIterator])
        chunkIterator +=1 
        offsetIterator += 1
    offset_to_next_IFD = offset_to_next_IFDArray[3] | (offset_to_next_IFDArray[2]<<8) | (offset_to_next_IFDArray[1]<<16) | (offset_to_next_IFDArray[0]<<24)

    # If offset == 0 there is not more IFD in exif
    if(offset_to_next_IFD == 0):
        isNextIFDPasser[0] = False
    else:
        chunkIterator += offset_to_next_IFD
        isNextIFDPasser[0] = True

    chunkIteratorPasser[0] = chunkIterator

    # Return IFD that contain n DE
    return ifd

def readDatafromIFD(IFDsArray, exifChunk):
    numberOfIFD = 0
    while numberOfIFD < len(IFDsArray):
        numberOfDE = 0
        while numberOfDE < len(IFDsArray[numberOfIFD]):
            directoryEntry = IFDsArray[numberOfIFD][numberOfDE]
            print()
            print("TagId = " +  tagTypes.getTagTypeString(directoryEntry.getTagIdNumber()))

            data = []
            dataIterator = 0
            while dataIterator < directoryEntry.getDataLength():

                # Data can fit into offset field
                if(directoryEntry.getDataLength() <= 4):
                    dataIndex = dataIterator
                    data.append(directoryEntry.offsetArray[dataIndex])
                else:
                    dataIndex = directoryEntry.getOffset() + dataIterator
                    data.append(exifChunk.dataArray[dataIndex])

                dataIterator += 1

            if(directoryEntry.getTagTypeNumber() == 2):
                decodedText = bytearray(data).decode('utf-8')
                print(decodedText)
            elif(directoryEntry.getTagTypeNumber() == 3):
                countIterator = 0
                while countIterator < directoryEntry.getCount():
                    number = data[1 + (countIterator * 2)] | (data[0 + (countIterator * 2)]<<8)
                    print(number)
                    countIterator += 1
            elif(directoryEntry.getTagTypeNumber() == 4):
                countIterator = 0
                while countIterator < directoryEntry.getCount():
                    number = data[3 + (countIterator * 2)] | (data[2 + (countIterator * 2)]<<8) | (data[1 + (countIterator * 2)]<<16) | (data[0 + (countIterator * 2)]<<24)
                    print(number)
                    countIterator += 1
            elif(directoryEntry.getTagTypeNumber() == 5):
                countIterator = 0
                while countIterator < directoryEntry.getCount():
                    numerator = data[3 + (countIterator * 2)] | (data[2 + (countIterator * 2)]<<8) | (data[1 + (countIterator * 2)]<<16) | (data[0 + (countIterator * 2)]<<24)
                    denumerator = data[7 + (countIterator * 2)] | (data[6 + (countIterator * 2)]<<8) | (data[5 + (countIterator * 2)]<<16) | (data[4 + (countIterator * 2)]<<24)
                    print(str(numerator) + "/" + str(denumerator))
                    countIterator += 1
            else:
                print(data)



            numberOfDE += 1
        numberOfIFD += 1

