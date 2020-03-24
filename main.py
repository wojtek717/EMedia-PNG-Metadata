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
    compressionMethon = ihdrChunk.dataArray[10]
    filterMethod = ihdrChunk.dataArray[11]
    interlaceMethod = ihdrChunk.dataArray[12]

    print("Width = " + str(width))
    print("Height = " + str(height))
    #TODO for Maciej -> Print remaining atributes

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

    #Read and decode text
    text = []
    decodedText = ''

    while chunkIterator < len(textualChunk.dataArray):
        text.append(textualChunk.dataArray[chunkIterator])
        chunkIterator += 1
    decodedText = bytearray(text).decode('latin1')
    print('Text = ' + decodedText)

def decode_chunks(chunksArray):
    chunkIterator = 0
    while chunkIterator < len(chunksArray):
        if(chunksArray[chunkIterator].getChunkTypeText() == 'IHDR'):
            decode_IHDR(chunksArray[chunkIterator])
        
        if(chunksArray[chunkIterator].getChunkTypeText() == 'tEXt'):
            decode_tEXt(chunksArray[chunkIterator])
        
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
