import binascii

def read_chunk(bArray, startIndex):
    chunkIterator = startIndex
    
    # Read and merge size Bytes
    sizeArray = [0,0,0,0]
    
    sizeByte = 0
    while sizeByte < 4:
        sizeArray[sizeByte] = bArray[chunkIterator]
        sizeByte += 1
        chunkIterator += 1
    
    chunkSize = sizeArray[3] | (sizeArray[2]<<8) | (sizeArray[1]<<16) | (sizeArray[0]<<24)
    print(chunkSize)

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
    filename = 'ex1.png'
    with open(filename, 'rb') as f:
        byteArray = f.read()
    #print(binascii.hexlify(byteArray))

    check_sygnature(byteArray)
    read_chunk(byteArray, 8)


if __name__ == "__main__":
    main()
