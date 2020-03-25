import binascii
import zlib

# PNG Chunk representation
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

# Function that provides reading chunk from PNG file and returns chunk object
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
