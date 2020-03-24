import binascii

class Chunk:
    def __init__(self, lengthArray, typeArray, dataArray, crcArray, nextChunkIndex):
        self.lengthArray = lengthArray
        self.typeArray = typeArray
        self.dataArray = dataArray
        self.crcArray = crcArray
        self.nextChunkIndex = nextChunkIndex

        self.calculateNextChunkIndex(self.nextChunkIndex)

        print('Chunk type ->' + self.getChunkTypeText())

    # IEND chunk is the last one so we need to point out that 
    def calculateNextChunkIndex(self, nextChunkIndex):
        if(bytearray(self.typeArray).decode('utf-8') == 'IEND'):
            self.nextChunkIndex = -1    
    
    # Returns chunkType as String
    def getChunkTypeText(self):
        return bytearray(self.typeArray).decode('utf-8')

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


def decode_chunks(chunksArray):
    chunkIterator = 0
    while chunkIterator < len(chunksArray):
        if(chunksArray[chunkIterator].getChunkTypeText() == 'IHDR'):
            decode_IHDR(chunksArray[chunkIterator])
        
        #TODO add if statements for other chunks then handle their decode methods
        
        chunkIterator += 1

def read_chunk(bArray, startIndex):
    chunkIterator = startIndex
    lengthArray = []
    typeArray = []
    dataArray = []
    crcArray = []
    
    # Read and merge size Bytes
    lengthByte = 0
    while lengthByte < 4:
        lengthArray.append(bArray[chunkIterator])
        lengthByte += 1
        chunkIterator += 1
    
    # Merge 4*Byte into one 32binary number
    chunkLength = lengthArray[3] | (lengthArray[2]<<8) | (lengthArray[1]<<16) | (lengthArray[0]<<24)

    # Read chunk type
    typeByte = 0
    while typeByte < 4:
        typeArray.append(bArray[chunkIterator])
        typeByte += 1
        chunkIterator += 1

    # Read chunk data
    dataByte = 0
    while dataByte < chunkLength:
        dataArray.append(bArray[chunkIterator])
        dataByte += 1
        chunkIterator += 1

    # Read chunk CRC
    crcByte = 0
    while crcByte < 4:
        crcArray.append(bArray[chunkIterator])
        crcByte += 1
        chunkIterator += 1

    # Return chunk object
    return(Chunk(lengthArray, typeArray, dataArray, crcArray, chunkIterator))

def check_sygnature(bArray):
    sygnature = [137, 80, 78, 71, 13, 10, 26, 10]
    sygnature_byte = 0

    while sygnature_byte < 8:
        if sygnature[sygnature_byte] != bArray[sygnature_byte]:
            return False  

        sygnature_byte += 1
    print("Valid sygnature")
    return True        


def main():
    filename = 'ex1_color.png'
    fileChunks = []

    # Open and read file into byte array
    with open(filename, 'rb') as f:
        byteArray = f.read()
    #print(binascii.hexlify(byteArray))

    if(check_sygnature(byteArray) != True):
        return False

    chunkIndex = 8
    while chunkIndex != (-1):
        fileChunks.append(read_chunk(byteArray, chunkIndex))
        chunkIndex = fileChunks[-1].nextChunkIndex

    #decode_IHDR(fileChunks[0])
    decode_chunks(fileChunks)

if __name__ == "__main__":
    main()
