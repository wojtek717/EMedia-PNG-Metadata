import binascii
import chunk as PNGChunk
import chunksDecoder as CDecoder

# Function that checks if PNG sygnature is valid
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
    filename = 'images/ex1.png'
    fileChunks = []

    # Open and read file into byte array
    with open(filename, 'rb') as f:
        byteArray = f.read()

    if(check_sygnature(byteArray) != True):
        return False

    chunkIndex = 8
    while chunkIndex != (-1):
        fileChunks.append(PNGChunk.read_chunk(byteArray, chunkIndex))
        chunkIndex = fileChunks[-1].nextChunkIndex

    CDecoder.decode_chunks(fileChunks)

if __name__ == "__main__":
    main()
